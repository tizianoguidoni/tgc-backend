from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# 17 Meme Cards definition
MEME_CARDS = [
    # Common
    {"name": "Pepe the Frog", "rarity": "Common", "image_url": "/cards/pepe.png", "flavor": "Feels good man.", "power": 12, "sigma": 44, "based": 67},
    {"name": "Wojak", "rarity": "Common", "image_url": "/cards/wojak.png", "flavor": "I just feel so...", "power": 8, "sigma": 22, "based": 41},
    {"name": "Troll Face", "rarity": "Common", "image_url": "/cards/troll.png", "flavor": "Problem?", "power": 15, "sigma": 55, "based": 30},
    {"name": "Is This a Pigeon?", "rarity": "Common", "image_url": "/cards/pigeon.png", "flavor": "Is this a rare card?", "power": 9, "sigma": 18, "based": 52},
    {"name": "Success Kid", "rarity": "Common", "image_url": "/cards/success.png", "flavor": "Nailed it.", "power": 18, "sigma": 61, "based": 78},
    {"name": "Hide the Pain Harold", "rarity": "Common", "image_url": "/cards/harold.png", "flavor": "Everything is fine.", "power": 11, "sigma": 33, "based": 59},
    {"name": "Distracted Boyfriend", "rarity": "Common", "image_url": "/cards/boyfriend.png", "flavor": "New framework dropped.", "power": 13, "sigma": 29, "based": 45},
    {"name": "Mocking SpongeBob", "rarity": "Common", "image_url": "/cards/spongebob.png", "flavor": "mOcKiNg SpOnGeBoB.", "power": 14, "sigma": 37, "based": 63},
    {"name": "Woman Yelling at Cat", "rarity": "Common", "image_url": "/cards/yellingcat.png", "flavor": "Smudge does not care.", "power": 10, "sigma": 41, "based": 55},
    {"name": "Grumpy Cat", "rarity": "Common", "image_url": "/cards/grumpycat.png", "flavor": "No.", "power": 16, "sigma": 48, "based": 71},
    # Rare
    {"name": "Doge", "rarity": "Rare", "image_url": "/cards/doge.png", "flavor": "Much wow. Very rare.", "power": 44, "sigma": 77, "based": 88},
    {"name": "Stonks Man", "rarity": "Rare", "image_url": "/cards/stonks.png", "flavor": "Line go up. Always.", "power": 51, "sigma": 69, "based": 82},
    {"name": "Disaster Girl", "rarity": "Rare", "image_url": "/cards/disastergirl.png", "flavor": "She planned this.", "power": 48, "sigma": 83, "based": 91},
    {"name": "Nyan Cat", "rarity": "Rare", "image_url": "/cards/nyancat.png", "flavor": "nyan nyan nyan nyan", "power": 39, "sigma": 72, "based": 84},
    # Epic
    {"name": "Cyber Doge", "rarity": "Epic", "image_url": "/cards/cyberdoge.png", "flavor": "Such future. Very cyber. Wow.", "power": 78, "sigma": 91, "based": 95},
    {"name": "Gigachad", "rarity": "Epic", "image_url": "/cards/gigachad.png", "flavor": "Power: 9000 | Sigma: MAX | Weakness: feelings", "power": 95, "sigma": 99, "based": 100},
    # Legendary
    {"name": "Illuminati Triangle", "rarity": "Legendary", "image_url": "/cards/illuminati.png", "flavor": "They knew you would pull this.", "power": 999, "sigma": 999, "based": 999},
]

def seed_db():
    print("Database seeding started...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    # Check if cards exist
    existing_cards = db.query(models.Card).count()
    db.query(models.Card).delete()
db.commit()
if True:
        for card_data in MEME_CARDS:
            card = models.Card(name=card_data["name"], rarity=card_data["rarity"], image_url=card_data["image_url"], flavor=card_data.get("flavor",""), power=card_data.get("power",0), sigma=card_data.get("sigma",0), based=card_data.get("based",0))
            db.add(card)
        db.commit()
        print(f"Successfully seeded {len(MEME_CARDS)} meme cards.")
    else:
        print(f"Database already seeded with {existing_cards} cards.")
        
    db.close()

if __name__ == "__main__":
    seed_db()
