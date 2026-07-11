from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
import loggers

load_dotenv()

try:
    # --- SQLAlchemy ---
    engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}", pool_size=5, pool_pre_ping=True)

    with engine.connect() as conn:
        conn.execute(text('select 1'))

except Exception as e:
    loggers.app_logger.critical(f'{e}')
    raise
