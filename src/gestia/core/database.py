from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

class DatabaseManager:
    def __init__(self, db_url=None):
        if db_url is None:
            # Détecter l'environnement
            env = os.getenv('GESTIA_ENV', 'development')
            
            # Créer le dossier data s'il n'existe pas
            os.makedirs('data', exist_ok=True)
            
            # CORRECTION : Utiliser la même structure de chemins que les migrations
            if env == 'development':
                db_url = "sqlite:///data/development/gestia.db"
            elif env == 'production':
                db_url = "sqlite:///data/production/gestia.db"
            elif env == 'test':
                db_url = "sqlite:///data/test/gestia.db"
            else:
                db_url = "sqlite:///data/development/gestia.db"
        
        self.engine = create_engine(db_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db_url = db_url
    
    def create_tables(self):
        """Crée toutes les tables de la base de données"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Retourne une session de base de données"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Ferme une session de base de données"""
        session.close()
    
    def get_database_path(self):
        """Retourne le chemin du fichier de base de données"""
        if self.db_url.startswith('sqlite:///'):
            return self.db_url.replace('sqlite:///', '')
        return None
    
    def backup_database(self, backup_name=None):
        """Sauvegarde la base de données"""
        import shutil
        from datetime import datetime
        
        db_path = self.get_database_path()
        if not db_path or not os.path.exists(db_path):
            print("❌ Base de données non trouvée pour la sauvegarde")
            return False
        
        # Créer le dossier backups s'il n'existe pas
        os.makedirs('data/backups', exist_ok=True)
        
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"gestia_backup_{timestamp}.db"
        
        backup_path = f"data/backups/{backup_name}"
        
        try:
            shutil.copy2(db_path, backup_path)
            print(f"✅ Sauvegarde créée : {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")
            return False

# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager()

def init_database():
    """Initialise la base de données"""
    db_manager.create_tables()
    env = os.getenv('GESTIA_ENV', 'development')
    print(f"✅ Base de données initialisée avec succès! (Environnement: {env})")

def get_db():
    """Générateur pour obtenir une session de base de données"""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db_manager.close_session(db)

def get_current_environment():
    """Retourne l'environnement actuel"""
    return os.getenv('GESTIA_ENV', 'development')

def set_environment(env):
    """Définit l'environnement"""
    os.environ['GESTIA_ENV'] = env
    global db_manager
    db_manager = DatabaseManager()
    print(f"🔄 Environnement changé vers : {env}") 