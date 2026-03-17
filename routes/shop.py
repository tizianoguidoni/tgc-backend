from fastapi import APIRouter, Depends, HTTPException
import stripe
import os
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth_utils
from typing import Dict

router = APIRouter(prefix="/shop", tags=["shop"])

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_mvp_stub")
DOMAIN = os.environ.get("DOMAIN", "http://localhost:5173")

# Prices configuration (Stripe Price IDs or custom logical mapping for MVP)
PACK_PRICES = {
    "3_packs": {"amount": 299, "currency": "usd", "name": "3 MVP Packs"},
    "10_packs": {"amount": 799, "currency": "usd", "name": "10 MVP Packs"}
}

@router.post("/checkout/{package_id}")
async def create_checkout_session(package_id: str, current_user: models.User = Depends(auth_utils.get_current_user)):
    if package_id not in PACK_PRICES:
        raise HTTPException(status_code=400, detail="Invalid package ID")
        
    price_info = PACK_PRICES[package_id]
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': price_info['currency'],
                    'product_data': {
                        'name': price_info['name'],
                    },
                    'unit_amount': price_info['amount'],
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{DOMAIN}/shop/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/shop",
            # We can pass user_id in client_reference_id to fulfill later via webhook
            client_reference_id=str(current_user.id),
            metadata={'package_id': package_id}
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook():
    # In a full app, verify stripe signature here.
    # For MVP, we will assume a simple ping for demo purposes
    return {"status": "success"}
