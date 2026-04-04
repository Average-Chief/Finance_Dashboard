import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("secret_key", "supersecretkey")
algorithm = "HS256"
access_token_expires_in = int(os.getenv("access_token_expires_in", 30))
database_url = os.getenv("database_url", "sqlite:///./finance.db")
