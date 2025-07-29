#!/usr/bin/env python3
"""
Script pour explorer la base de données GESTIA
"""

import sqlite3
import os
import json
import sys

def get_current_environment():
    """Lit l'environnement actuel depuis le fichier de configuration"""
    try:
        config_file = "data/.env_config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('environment', 'development')
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture de la configuration: {e}")
    return 'development'

def get_database_path(environment=None):
    """Retourne le chemin de la base de données pour l'environnement"""
    if environment is None:
        environment = get_current_environment()
    
    return f"data/{environment}/gestia.db"

def explorer_base_donnees():
    """Explore et affiche le contenu de la base de données"""
    
    # Obtenir l'environnement et le chemin de la base
    environment = get_current_environment()
    db_path = get_database_path(environment)
    
    print(f"🔍 Exploration de la base de données GESTIA")
    print(f"📁 Environnement: {environment}")
    print(f"📁 Chemin: {db_path}")
    print("=" * 50)
    
    if not os.path.exists(db_path):
        print(f"❌ Fichier {db_path} non trouvé!")
        print(f"💡 Vérifiez que l'environnement '{environment}' est correctement configuré")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🗄️ EXPLORATION DE LA BASE DE DONNÉES GESTIA")
        print("=" * 50)
        
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 Tables trouvées ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "=" * 50)
        
        # Explorer chaque table
        for table in tables:
            table_name = table[0]
            print(f"\n📊 TABLE: {table_name}")
            print("-" * 30)
            
            # Compter les lignes
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Nombre d'enregistrements: {count}")
            
            if count > 0:
                # Afficher la structure
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print("Colonnes:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
                
                # Afficher quelques exemples
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                print("Exemples de données:")
                for i, row in enumerate(rows, 1):
                    print(f"  {i}. {row}")
                
                if count > 3:
                    print(f"  ... et {count - 3} autres enregistrements")
            
            print()
        
        conn.close()
        print("✅ Exploration terminée!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exploration: {e}")

if __name__ == "__main__":
    explorer_base_donnees() 