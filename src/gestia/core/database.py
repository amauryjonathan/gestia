from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

class DatabaseManager:
    def __init__(self, db_url="sqlite:///gestia.db"):
        self.engine = create_engine(db_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Crée toutes les tables de la base de données"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Retourne une session de base de données"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Ferme une session de base de données"""
        session.close()

# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager()

def init_database():
    """Initialise la base de données"""
    db_manager.create_tables()
    print("Base de données initialisée avec succès!")

def get_db():
    """Générateur pour obtenir une session de base de données"""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db_manager.close_session(db) 