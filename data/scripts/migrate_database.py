#!/usr/bin/env python3
"""
Script de migration de la base de données GESTIA
===============================================

Ajoute les nouvelles colonnes ActionsAFaire et SoucisMachine à la table appareils.
"""

import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from gestia.core.database import db_manager, init_database
from sqlalchemy import text

def migrer_base_donnees():
    """Effectue la migration de la base de données"""
    print("🔄 Migration de la base de données GESTIA...")
    
    try:
        # Initialiser la base de données
        init_database()
        
        # Obtenir une session
        db = db_manager.get_session()
        
        # Vérifier si les colonnes existent déjà
        result = db.execute(text("PRAGMA table_info(appareils)"))
        colonnes_existantes = [row[1] for row in result.fetchall()]
        
        print(f"Colonnes existantes: {colonnes_existantes}")
        
        # Ajouter la colonne ActionsAFaire si elle n'existe pas
        if 'ActionsAFaire' not in colonnes_existantes:
            print("➕ Ajout de la colonne ActionsAFaire...")
            db.execute(text("ALTER TABLE appareils ADD COLUMN ActionsAFaire TEXT"))
            print("✅ Colonne ActionsAFaire ajoutée avec succès")
        else:
            print("ℹ️  Colonne ActionsAFaire existe déjà")
        
        # Ajouter la colonne SoucisMachine si elle n'existe pas
        if 'SoucisMachine' not in colonnes_existantes:
            print("➕ Ajout de la colonne SoucisMachine...")
            db.execute(text("ALTER TABLE appareils ADD COLUMN SoucisMachine TEXT"))
            print("✅ Colonne SoucisMachine ajoutée avec succès")
        else:
            print("ℹ️  Colonne SoucisMachine existe déjà")
        
        # Valider les changements
        db.commit()
        
        # Vérifier le résultat final
        result = db.execute(text("PRAGMA table_info(appareils)"))
        colonnes_finales = [row[1] for row in result.fetchall()]
        print(f"Colonnes finales: {colonnes_finales}")
        
        print("✅ Migration terminée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    migrer_base_donnees() 