import os
from sqlalchemy import create_engine

def get_engine():
    user     = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host     = os.getenv('DB_HOST')
    port     = os.getenv('DB_PORT')
    dbname   = os.getenv('DB_NAME')

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url, connect_args={"sslmode": "require"})
