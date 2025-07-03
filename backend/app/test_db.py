from app.db.session import engine
from sqlalchemy import text

try: 
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("DB connection successful", result.scalar())
        
except Exception as e:
    print("Error connecting to DB...\n", str(e))
        