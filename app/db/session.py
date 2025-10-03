from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de SQLite para dev
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Si usas PostgreSQL en el futuro sería:
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost:5432/nomascartera"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Solo necesario en SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para inyectar la sesión en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
