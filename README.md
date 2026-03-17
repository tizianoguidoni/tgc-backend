# ⚙️ RipPack Backend: Secure Card Trading API

This is the robust FastAPI backend for RipPack, managing users, inventories, card generation, and secure Stripe checkout flows.

## ✨ Features
- **FastAPI Driven**: High-performance asynchronous API endpoints.
- **JWT Authentication**: Secure user sessions and protocol-based access control.
- **Rarity Engine**: Weighted randomization for card pulls (Common, Rare, Epic, Legendary).
- **Stripe Integration**: Checkout session creation and webhook logic for MVP monetization.
- **SQLite + SQLAlchemy**: Lightweight but scalable database schema.

## 🚀 Tech Stack
- **Framework**: FastAPI (Python 3.9+)
- **ORM**: SQLAlchemy
- **Database**: SQLite (rippack.db)
- **Security**: Passlib (bcrypt) + JWT Tokens
- **Payments**: Stripe Python Library

## 🛠️ Getting Started

### Prerequisites
- Python 3.9+

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tizianoguidoni/tgc-backend.git
   cd tgc-backend
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database & Seed Cards**:
   ```bash
   python seed.py
   ```

5. **Start the API Server**:
   ```bash
   python main.py
   ```

## 📜 API Documentation
- `POST /auth/register`: Create a new user.
- `POST /auth/token`: Login and get JWT access key.
- `POST /packs/open`: Rip a pack (consumes credits).
- `GET /packs/inventory`: View your personal vault.
- `POST /shop/checkout/{package_id}`: Initialize Stripe payment.

---
**Maintained by**: [tizianoguidoni](https://github.com/tizianoguidoni)
