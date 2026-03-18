from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from routes import auth, packs, shop, battle
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RipPack API", description="MVP Backend for RipPack Game")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(packs.router)
app.include_router(shop.router)
app.include_router(battle.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to RipPack API"}

@app.post("/admin/seed")
def seed_cards(db: Session = Depends(get_db)):
    cards_data = [
        {"name": "Corrupted_404",  "rarity": "Common",    "image_url": "/cards/avatar 1.png",  "flavor": "Il primo errore che ha dato vita al caos.",     "power": 40,  "sigma": 20,  "based": 10},
        {"name": "Stackflow",      "rarity": "Rare",      "image_url": "/cards/avatar 2.png",  "flavor": "Si moltiplica ogni volta che viene sconfitta.", "power": 55,  "sigma": 35,  "based": 20},
        {"name": "NullPointer",    "rarity": "Epic",      "image_url": "/cards/avatar 3.png",  "flavor": "Non esiste. Eppure e qui.",                     "power": 70,  "sigma": 50,  "based": 30},
        {"name": "The_Last_Bug",   "rarity": "Legendary", "image_url": "/cards/avatar 4.png",  "flavor": "Se la elimini, tutto smette di funzionare.",    "power": 95,  "sigma": 80,  "based": 60},
        {"name": "Binary_Ghost",   "rarity": "Common",    "image_url": "/cards/avatar 5.png",  "flavor": "Esiste solo in 0 e 1.",                         "power": 38,  "sigma": 18,  "based": 12},
        {"name": "Encrypted_Wolf", "rarity": "Rare",      "image_url": "/cards/avatar 6.png",  "flavor": "Nessuno conosce la sua forma reale.",           "power": 58,  "sigma": 38,  "based": 22},
        {"name": "Hash_Titan",     "rarity": "Epic",      "image_url": "/cards/avatar 7.png",  "flavor": "Ogni sua mossa e irreversibile.",               "power": 72,  "sigma": 48,  "based": 35},
        {"name": "Quantum_Lock",   "rarity": "Legendary", "image_url": "/cards/avatar 8.png",  "flavor": "Osservarlo cambia il risultato.",               "power": 90,  "sigma": 75,  "based": 55},
        {"name": "Ping",           "rarity": "Common",    "image_url": "/cards/avatar 9.png",  "flavor": "Piccolo. Veloce. Ovunque.",                     "power": 30,  "sigma": 15,  "based": 25},
        {"name": "Broadcast",      "rarity": "Rare",      "image_url": "/cards/avatar 10.png", "flavor": "La sua voce raggiunge tutti i fronti.",         "power": 52,  "sigma": 30,  "based": 28},
        {"name": "Frequency",      "rarity": "Epic",      "image_url": "/cards/avatar 11.png", "flavor": "Vibra a una lunghezza d onda che distrugge.",   "power": 68,  "sigma": 45,  "based": 40},
        {"name": "The_Carrier",    "rarity": "Legendary", "image_url": "/cards/avatar 12.png", "flavor": "Trasporta messaggi tra i mondi.",               "power": 88,  "sigma": 70,  "based": 50},
        {"name": "Empty_Packet",   "rarity": "Common",    "image_url": "/cards/avatar 13.png", "flavor": "Non contiene niente. Per questo e pericoloso.", "power": 35,  "sigma": 10,  "based": 15},
        {"name": "Silent_Process", "rarity": "Rare",      "image_url": "/cards/avatar 14.png", "flavor": "Gira in background. Sempre.",                   "power": 50,  "sigma": 32,  "based": 18},
        {"name": "Deadzone",       "rarity": "Epic",      "image_url": "/cards/avatar 15.png", "flavor": "Dove arriva lui, niente funziona piu.",         "power": 75,  "sigma": 55,  "based": 38},
        {"name": "The_Architect",  "rarity": "Legendary", "image_url": "/cards/avatar 16.png", "flavor": "Ha costruito il Void. Ora lo abita.",           "power": 92,  "sigma": 78,  "based": 58},
        {"name": "ROOT",           "rarity": "Legendary", "image_url": "/cards/avatar 17.png", "flavor": "Ha accesso a tutto. E il boss finale.",         "power": 100, "sigma": 100, "based": 100},
    ]
    db.query(models.Card).delete()
    db.commit()
    for data in cards_data:
        db.add(models.Card(**data))
    db.commit()
    return {"message": "17 carte VOIDBORN inserite"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)