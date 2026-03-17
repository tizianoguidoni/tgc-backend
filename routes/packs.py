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
