import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("secret_key", "supersecretkey")
algorithm = "HS256"
access_token_expires_in = int(os.getenv("access_token_expires_in", 30))

BASE_DIR = Path(__file__).resolve().parent  

db_name = os.getenv("database_url", "finance.db").replace("sqlite:///", "")

DB_PATH = BASE_DIR / db_name

database_url = f"sqlite:///{DB_PATH}"
