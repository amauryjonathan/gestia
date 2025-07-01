#!/usr/bin/env python3
"""
Script pour explorer la base de données GESTIA
"""

import sqlite3
import os

def explorer_base_donnees():
    """Explore et affiche le contenu de la base de données"""
    
    if not os.path.exists('gestia.db'):
        print("❌ Fichier gestia.db non trouvé!")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('gestia.db')
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