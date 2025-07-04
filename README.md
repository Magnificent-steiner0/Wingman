# Wingman

---

## Features (So Far)
- User Registration & Login with JWT Auth
- Secure password hashing with bcrypt
- Email Verification via Sendgrid

---

## Getting Started
### 1. Clone the repository

```bash
git clone https://github.com/Magnificent-steiner0/Wingman.git
cd Wingman
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a .env file in the project root with the following:

```bash
DATABASE_URL=postgresql+psycopg2://user:password@localhost/dbname
JWT_SECRET_KEY=secret_key
JWT_ALGORITHM=algorithm
JWT_ACCESS_TOKEN_EXPIRES=x_minutes

SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_sender@gmail.com
```

### 4. Run the backend
```
cd backend
uvicorn app.main:app --reload
```