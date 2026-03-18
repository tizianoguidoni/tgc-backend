from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth_utils
import random
from typing import List

router = APIRouter(prefix="/packs", tags=["packs"])

# Probabilities for MVP: Common (70%), Rare (20%), Epic (8.5%), Legendary (1.5%)
RARITY_WEIGHTS = {
    "Common": 70.0,
    "Rare": 20.0,
    "Epic": 8.5,
    "Legendary": 1.5
}

def get_random_card(db: Session):
    # Determine rarity
    rarities = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    chosen_rarity = random.choices(rarities, weights=weights, k=1)[0]
    
    # Get all cards of chosen rarity
    cards = db.query(models.Card).filter(models.Card.rarity == chosen_rarity).all()
    if not cards:
        # Fallback if no cards of that rarity exist in DB
        cards = db.query(models.Card).all()
        
    if not cards:
        raise HTTPException(status_code=500, detail="No cards available in the database")
        
    return random.choice(cards)

@router.post("/open", response_model=List[schemas.CardResponse])
def open_pack(current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    if current_user.packs < 1:
        raise HTTPException(status_code=400, detail="Not enough packs")
    
    current_user.packs -= 1
    
    # Generate 5 cards
    pulled_cards = []
    for _ in range(5):
        card = get_random_card(db)
        pulled_cards.append(card)
        
        # Add to inventory
        user_card = db.query(models.UserCard).filter(
            models.UserCard.user_id == current_user.id,
            models.UserCard.card_id == card.id
        ).first()
        
        if user_card:
            user_card.count += 1
        else:
            new_user_card = models.UserCard(user_id=current_user.id, card_id=card.id, count=1)
            db.add(new_user_card)
            
    db.commit()
    return pulled_cards

@router.get("/inventory", response_model=List[schemas.UserCardResponse])
def get_inventory(current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    user_cards = db.query(models.UserCard).filter(models.UserCard.user_id == current_user.id).all()
    # Eager load the card relationship to avoid N+1 queries manually or just let SQLAlchemy handle it if configured
    return [{"card": uc.card, "count": uc.count} for uc in user_cards]
# ─── AGGIUNGI QUESTO IN FONDO A routes/packs.py ──────────────────────────────
# (copia e incolla dopo l'ultimo endpoint esistente)

from pydantic import BaseModel as PydanticBase

class FuseRequest(PydanticBase):
    card_name: str

FUSION_RULES = {
    "Common":    {"needed": 3, "next": "Rare"},
    "Rare":      {"needed": 5, "next": "Epic"},
    "Epic":      {"needed": 8, "next": "Legendary"},
}

@router.post("/fuse")
def fuse_cards(
    req: FuseRequest,
    current_user: models.User = Depends(auth_utils.get_current_user),
    db: Session = Depends(get_db)
):
    # Trova la carta
    card = db.query(models.Card).filter(models.Card.name == req.card_name).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    rule = FUSION_RULES.get(card.rarity)
    if not rule:
        raise HTTPException(status_code=400, detail="Cannot fuse Legendary cards")

    # Controlla che l'utente abbia abbastanza copie
    user_card = db.query(models.UserCard).filter(
        models.UserCard.user_id == current_user.id,
        models.UserCard.card_id == card.id
    ).first()

    if not user_card or user_card.count < rule["needed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Need {rule['needed']}x {card.rarity}, you have {user_card.count if user_card else 0}"
        )

    # Rimuovi le carte usate
    user_card.count -= rule["needed"]
    if user_card.count <= 0:
        db.delete(user_card)

    # Pesca una carta casuale della rarità superiore
    next_cards = db.query(models.Card).filter(models.Card.rarity == rule["next"]).all()
    if not next_cards:
        raise HTTPException(status_code=500, detail="No cards of next rarity available")

    new_card = random.choice(next_cards)

    # Aggiungi la nuova carta all'inventario
    existing = db.query(models.UserCard).filter(
        models.UserCard.user_id == current_user.id,
        models.UserCard.card_id == new_card.id
    ).first()

    if existing:
        existing.count += 1
    else:
        db.add(models.UserCard(user_id=current_user.id, card_id=new_card.id, count=1))

    db.commit()

    # Ritorna la nuova carta
    return {
        "id": new_card.id,
        "name": new_card.name,
        "rarity": new_card.rarity,
        "image_url": new_card.image_url,
        "flavor": new_card.flavor,
        "power": new_card.power,
        "sigma": new_card.sigma,
        "based": new_card.based,
    }
