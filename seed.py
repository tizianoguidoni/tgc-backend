from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# 17 Meme Cards definition
MEME_CARDS = [
    # Common (10)
    {"name": "Pepe the Frog", "rarity": "Common", "image_url": "/cards/pepe.png"},
    {"name": "Wojak", "rarity": "Common", "image_url": "/cards/wojak.png"},
    {"name": "Troll Face", "rarity": "Common", "image_url": "/cards/troll.png"},
    {"name": "Is This a Pigeon?", "rarity": "Common", "image_url": "/cards/pigeon.png"},
    {"name": "Success Kid", "rarity": "Common", "image_url": "/cards/success.png"},
    {"name": "Hide the Pain Harold", "rarity": "Common", "image_url": "/cards/harold.png"},
    {"name": "Distracted Boyfriend", "rarity": "Common", "image_url": "/cards/boyfriend.png"},
    {"name": "Mocking SpongeBob", "rarity": "Common", "image_url": "/cards/spongebob.png"},
    {"name": "Woman Yelling at Cat", "rarity": "Common", "image_url": "/cards/yellingcat.png"},
    {"name": "Grumpy Cat", "rarity": "Common", "image_url": "/cards/grumpycat.png"},
    
    # Rare (4)
    {"name": "Doge", "rarity": "Rare", "image_url": "/cards/doge.png"},
    {"name": "Stonks Man", "rarity": "Rare", "image_url": "/cards/stonks.png"},
    {"name": "Disaster Girl", "rarity": "Rare", "image_url": "/cards/disastergirl.png"},
    {"name": "Nyan Cat", "rarity": "Rare", "image_url": "/cards/nyancat.png"},
    
    # Epic (2)
    {"name": "Cyber Doge", "rarity": "Epic", "image_url": "/cards/cyberdoge.png"},
    {"name": "Gigachad", "rarity": "Epic", "image_url": "/cards/gigachad.png"},
    
    # Legendary (1)
    {"name": "Illuminati Triangle", "rarity": "Legendary", "image_url": "/cards/illuminati.png"}
]

def seed_db():
    print("Database seeding started...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    # Check if cards exist
    existing_cards = db.query(models.Card).count()
    if existing_cards == 0:
        for card_data in MEME_CARDS:
            card = models.Card(**card_data)
            db.add(card)
        db.commit()
        print(f"Successfully seeded {len(MEME_CARDS)} meme cards.")
    else:
        print(f"Database already seeded with {existing_cards} cards.")
        
    db.close()

if __name__ == "__main__":
    seed_db()
