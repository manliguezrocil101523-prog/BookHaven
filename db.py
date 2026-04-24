import os
import sys
from urllib.parse import urlparse, quote, urlunparse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set.")
    print("Please set it before running the application.")
    sys.exit(1)

# SQLAlchemy defaults to psycopg2 for 'postgresql://' URLs.
# If we only have psycopg3 installed, force the correct dialect.
if DATABASE_URL.startswith('postgresql://') and not DATABASE_URL.startswith('postgresql+'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

# Robustly fix any special characters in the password using urllib.parse.
# This preserves the full hostname (e.g., aws-1-ap-southeast-1.pooler.supabase.com)
# and only encodes the password portion, preventing "Name or service not known" errors.
_parsed = urlparse(DATABASE_URL)
if _parsed.password:
    # URL-encode special characters like @ : / etc. in the password
    safe_password = quote(_parsed.password, safe='')
    # Rebuild netloc with encoded password
    if _parsed.port:
        new_netloc = f"{_parsed.username}:{safe_password}@{_parsed.hostname}:{_parsed.port}"
    else:
        new_netloc = f"{_parsed.username}:{safe_password}@{_parsed.hostname}"
    DATABASE_URL = urlunparse(_parsed._replace(netloc=new_netloc))

# Create engine with sensible production settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=5000"
    }
)

# Validate connection on startup so deployment issues surface immediately
try:
    with engine.connect() as conn:
        print("[DB] Database connection established successfully.")
except Exception as exc:
    print(f"[DB] FATAL: Could not connect to database: {exc}")
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

