from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes import auth, packs, shop
import uvicorn

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RipPack API", description="MVP Backend for RipPack Game")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://tgc-frontend-three.vercel.app", "https://tgc-frontend-git-main-tizianoguidonis-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(packs.router)
app.include_router(shop.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to RipPack API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
