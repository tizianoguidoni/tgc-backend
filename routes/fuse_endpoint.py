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
