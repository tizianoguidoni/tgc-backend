from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

MEME_CARDS = [
    {"name": "Pepe the Frog", "rarity": "Common", "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a7/Pepe_the_frog_by_Matt_Furie.jpg", "flavor": "Feels good man.", "power": 12, "sigma": 44, "based": 67},
    {"name": "Wojak", "rarity": "Common", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Sad_Wojak.jpg/220px-Sad_Wojak.jpg", "flavor": "I just feel so...", "power": 8, "sigma": 22, "based": 41},
    {"name": "Troll Face", "rarity": "Common", "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png", "flavor": "Problem?", "power": 15, "sigma": 55, "based": 30},
    {"name": "Is This a Pigeon?", "rarity": "Common", "image_url": "https://i.imgflip.com/1o00in.jpg", "flavor": "Is this a rare card?", "power": 9, "sigma": 18, "based": 52},
    {"name": "Success Kid", "rarity": "Common", "image_url": "https://i.imgflip.com/1bhk.jpg", "flavor": "Nailed it.", "power": 18, "sigma": 61, "based": 78},
    {"name": "Hide the Pain Harold", "rarity": "Common", "image_url": "https://i.imgflip.com/gk5el.jpg", "flavor": "Everything is fine.", "power": 11, "sigma": 33, "based": 59},
    {"name": "Distracted Boyfriend", "rarity": "Common", "image_url": "https://i.imgflip.com/1ur9b0.jpg", "flavor": "New framework dropped.", "power": 13, "sigma": 29, "based": 45},
    {"name": "Mocking SpongeBob", "rarity": "Common", "image_url": "https://i.imgflip.com/1otk96.jpg", "flavor": "mOcKiNg SpOnGeBoB.", "power": 14, "sigma": 37, "based": 63},
    {"name": "Woman Yelling at Cat", "rarity": "Common", "image_url": "https://i.imgflip.com/345v97.jpg", "flavor": "Smudge does not care.", "power": 10, "sigma": 41, "based": 55},
    {"name": "Grumpy Cat", "rarity": "Common", "image_url": "https://i.imgflip.com/8p0a.jpg", "flavor": "No.", "power": 16, "sigma": 48, "based": 71},
    {"name": "Doge", "rarity": "Rare", "image_url": "https://upload.wikimedia.org/wikipedia/en/5/5f/Original_Doge_meme.jpg", "flavor": "Much wow. Very rare.", "power": 44, "sigma": 77, "based": 88},
    {"name": "Stonks Man", "rarity": "Rare", "image_url": "https://i.imgflip.com/3si4b6.jpg", "flavor": "Line go up. Always.", "power": 51, "sigma": 69, "based": 82},
    {"name": "Disaster Girl", "rarity": "Rare", "image_url": "https://i.imgflip.com/23ls.jpg", "flavor": "She planned this.", "power": 48, "sigma": 83, "based": 91},
    {"name": "Nyan Cat", "rarity": "Rare", "image_url": "https://upload.wikimedia.org/wikipedia/en/f/fd/Nyan_cat_250px_frame.PNG", "flavor": "nyan nyan nyan nyan", "power": 39, "sigma": 72, "based": 84},
    {"name": "Cyber Doge", "rarity": "Epic", "image_url": "https://i.imgflip.com/4t0m5.jpg", "flavor": "Such future. Very cyber. Wow.", "power": 78, "sigma": 91, "based": 95},
    {"name": "Gigachad", "rarity": "Epic", "image_url": "https://i.imgflip.com/5cilum.jpg", "flavor": "Power: 9000 | Sigma: MAX | Weakness: feelings", "power": 95, "sigma": 99, "based": 100},
    {"name": "Illuminati Triangle", "rarity": "Legendary", "image_url": "https://i.imgflip.com/1e7ql7.jpg", "flavor": "They knew you would pull this.", "power": 999, "sigma": 999, "based": 999},
]

def seed_db():
    print("Database seeding started...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    db.query(models.UserCard).delete()
    db.query(models.Card).delete()
    db.commit()
    for card_data in MEME_CARDS:
        card = models.Card(
            name=card_data["name"],
            rarity=card_data["rarity"],
            image_url=card_data["image_url"],
            flavor=card_data.get("flavor", ""),
            power=card_data.get("power", 0),
            sigma=card_data.get("sigma", 0),
            based=card_data.get("based", 0)
        )
        db.add(card)
    db.commit()
    print(f"Successfully seeded {len(MEME_CARDS)} cards.")
    db.close()

if __name__ == "__main__":
    seed_db()
