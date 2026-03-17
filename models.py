from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    packs = Column(Integer, default=1)  # 1 free pack on signup
    streak = Column(Integer, default=0)
    last_login = Column(DateTime, default=datetime.utcnow)
    
    cards = relationship("UserCard", back_populates="user")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    rarity = Column(String, index=True) # Common, Rare, Epic, Legendary
    image_url = Column(String)
    flavor = Column(String, default="")
    power = Column(Integer, default=0)
    sigma = Column(Integer, default=0)
    based = Column(Integer, default=0)

class UserCard(Base):
    __tablename__ = "user_cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    count = Column(Integer, default=1)

    user = relationship("User", back_populates="cards")
    card = relationship("Card")
