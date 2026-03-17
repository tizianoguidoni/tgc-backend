from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, auth_utils
import random, json
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/battle", tags=["battle"])

RARITY_BONUS = {"Common": 0, "Rare": 10, "Epic": 25, "Legendary": 50}

def calc_attack(card):
    return round(card.power + (card.sigma * 0.5) + (card.based * 0.3) + RARITY_BONUS.get(card.rarity, 0))

def calc_attack_dict(card):
    return round(card["power"] + (card["sigma"] * 0.5) + (card["based"] * 0.3) + RARITY_BONUS.get(card["rarity"], 0))

class StartBattle(BaseModel):
    card_ids: List[int]

class PlayRound(BaseModel):
    battle_id: int
    card_id: int

def get_bot_cards(db, level):
    """Bot gets stronger cards based on level"""
    all_cards = db.query(models.Card).all()
    if level <= 2:
        pool = [c for c in all_cards if c.rarity in ["Common", "Rare"]] or all_cards
    elif level <= 4:
        pool = [c for c in all_cards if c.rarity in ["Common", "Rare", "Epic"]] or all_cards
    else:
        pool = all_cards
    return random.sample(pool, min(3, len(pool)))

@router.get("/my-level")
def get_my_level(current_user: models.User = Depends(auth_utils.get_current_user)):
    level = getattr(current_user, 'battle_level', 1) or 1
    streak = getattr(current_user, 'battle_wins_streak', 0) or 0
    return {
        "level": level,
        "wins_streak": streak,
        "wins_needed": level,
        "progress": f"{streak}/{level}"
    }

@router.post("/start")
def start_battle(data: StartBattle, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    if len(data.card_ids) != 3:
        raise HTTPException(status_code=400, detail="Choose exactly 3 cards")

    player_cards = []
    for cid in data.card_ids:
        uc = db.query(models.UserCard).filter(
            models.UserCard.user_id == current_user.id,
            models.UserCard.card_id == cid
        ).first()
        if not uc:
            raise HTTPException(status_code=404, detail=f"Card {cid} not in inventory")
        card = db.query(models.Card).filter(models.Card.id == cid).first()
        player_cards.append({
            "id": card.id, "name": card.name, "rarity": card.rarity,
            "image_url": card.image_url, "power": card.power,
            "sigma": card.sigma, "based": card.based,
            "flavor": card.flavor or "",
            "attack": calc_attack(card)
        })

    level = getattr(current_user, 'battle_level', 1) or 1
    bot_card_objs = get_bot_cards(db, level)
    bot_cards = [{
        "id": c.id, "name": c.name, "rarity": c.rarity,
        "image_url": c.image_url, "power": c.power,
        "sigma": c.sigma, "based": c.based,
        "flavor": c.flavor or "",
        "attack": calc_attack(c)
    } for c in bot_card_objs]

    battle = models.Battle(
        user_id=current_user.id,
        player_cards=json.dumps(player_cards),
        bot_cards=json.dumps(bot_cards),
        current_round=0,
        player_score=0,
        bot_score=0,
        status="active"
    )
    db.add(battle)
    db.commit()
    db.refresh(battle)

    streak = getattr(current_user, 'battle_wins_streak', 0) or 0
    return {
        "battle_id": battle.id,
        "bot_cards": bot_cards,
        "player_cards": player_cards,
        "level": level,
        "wins_streak": streak,
        "wins_needed": level
    }

@router.post("/play")
def play_round(data: PlayRound, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    battle = db.query(models.Battle).filter(
        models.Battle.id == data.battle_id,
        models.Battle.user_id == current_user.id
    ).first()
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    if battle.status != "active":
        raise HTTPException(status_code=400, detail="Battle already ended")

    player_cards = json.loads(battle.player_cards)
    bot_cards = json.loads(battle.bot_cards)

    player_card = next((c for c in player_cards if c["id"] == data.card_id), None)
    if not player_card:
        raise HTTPException(status_code=400, detail="Card not in your battle deck")

    bot_card = bot_cards[battle.current_round]
    player_wins_round = calc_attack_dict(player_card) >= calc_attack_dict(bot_card)

    if player_wins_round:
        battle.player_score += 1
    else:
        battle.bot_score += 1

    battle.current_round += 1

    packs_earned = 0
    level = getattr(current_user, 'battle_level', 1) or 1
    streak = getattr(current_user, 'battle_wins_streak', 0) or 0

    if battle.current_round >= 3:
        if battle.player_score > battle.bot_score:
            battle.status = "player_won"
            streak += 1
            if streak >= level:
                # Give pack and level up
                current_user.packs += 1
                packs_earned = 1
                streak = 0
                if level < 5:
                    level += 1
        else:
            battle.status = "bot_won"
            streak = 0  # Reset streak on loss, no pack lost

        current_user.battle_level = level
        current_user.battle_wins_streak = streak

    db.commit()

    return {
        "round": battle.current_round,
        "player_card": player_card,
        "bot_card": bot_card,
        "player_wins_round": player_wins_round,
        "player_score": battle.player_score,
        "bot_score": battle.bot_score,
        "battle_status": battle.status,
        "packs_earned": packs_earned,
        "level": level,
        "wins_streak": streak,
        "wins_needed": level
    }
