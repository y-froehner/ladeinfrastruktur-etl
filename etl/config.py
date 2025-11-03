import os
from dotenv import load_dotenv
load_dotenv()

CSV_PATH = "data/Ladesaeulenregister_BNetzA_2025-10-23.csv"
PROCESSED_CSV = "data/processed_ladesaeulen.csv"

PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PWD  = os.getenv("POSTGRES_PASSWORD", "postgres")
PG_DB   = os.getenv("POSTGRES_DB", "ladeinfra")
PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = int(os.getenv("POSTGRES_PORT", "5432"))  # will become 5433 via .env

SQLALCHEMY_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}"