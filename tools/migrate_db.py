#!/usr/bin/env python3
"""
Script de migration de base de données
======================================

Gère les migrations de schéma de manière professionnelle.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import db_manager, set_environment

class DatabaseMigrator:
    """Gestionnaire de migrations de base de données"""
    
    def __init__(self, environment='development'):
        self.environment = environment
        set_environment(environment)
        self.db_path = f"data/{environment}/gestia.db"
        self.migrations_table = "schema_migrations"
    
    def ensure_migrations_table(self):
        """Crée la table de suivi des migrations si elle n'existe pas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.migrations_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL,
                description TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_applied_migrations(self):
        """Récupère la liste des migrations déjà appliquées"""
        self.ensure_migrations_table()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT version FROM {self.migrations_table}")
        applied = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return applied
    
    def mark_migration_applied(self, version, description):
        """Marque une migration comme appliquée"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            INSERT INTO {self.migrations_table} (version, description)
            VALUES (?, ?)
        """, (version, description))
        
        conn.commit()
        conn.close()
    
    def run_migration(self, version, description, sql_commands):
        """Exécute une migration"""
        print(f"🔄 Migration {version}: {description}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for command in sql_commands:
                print(f"  Exécution: {command[:50]}...")
                cursor.execute(command)
            
            conn.commit()
            self.mark_migration_applied(version, description)
            print(f"✅ Migration {version} appliquée avec succès")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Erreur lors de la migration {version}: {e}")
            raise
        finally:
            conn.close()
    
    def migrate(self):
        """Exécute toutes les migrations nécessaires"""
        print(f"🚀 Début des migrations pour l'environnement: {self.environment}")
        print("=" * 60)
        
        applied_migrations = self.get_applied_migrations()
        
        # Définir toutes les migrations
        migrations = [
            {
                'version': '001_add_samsung_fields',
                'description': 'Ajout des champs pour références Samsung',
                'sql': [
                    'ALTER TABLE appareils ADD COLUMN Serie TEXT',
                    'ALTER TABLE appareils ADD COLUMN Capacite TEXT',
                    'ALTER TABLE appareils ADD COLUMN Technologie TEXT',
                    'ALTER TABLE appareils ADD COLUMN Variante TEXT',
                    'ALTER TABLE appareils ADD COLUMN ReferenceComplete TEXT'
                ]
            },
            {
                'version': '002_add_label_field',
                'description': 'Ajout du champ Label pour les fonctionnalités marketing',
                'sql': [
                    'ALTER TABLE appareils ADD COLUMN Label TEXT'
                ]
            }
        ]
        
        # Exécuter les migrations non appliquées
        for migration in migrations:
            if migration['version'] not in applied_migrations:
                self.run_migration(
                    migration['version'],
                    migration['description'],
                    migration['sql']
                )
            else:
                print(f"⏭️  Migration {migration['version']} déjà appliquée")
        
        print("=" * 60)
        print("✅ Toutes les migrations sont à jour !")
    
    def show_status(self):
        """Affiche le statut des migrations"""
        print(f"📊 Statut des migrations - Environnement: {self.environment}")
        print("=" * 60)
        
        applied_migrations = self.get_applied_migrations()
        
        if applied_migrations:
            print("Migrations appliquées:")
            for migration in applied_migrations:
                print(f"  ✅ {migration}")
        else:
            print("Aucune migration appliquée")
        
        print(f"\nBase de données: {self.db_path}")
        print(f"Existe: {'✅' if os.path.exists(self.db_path) else '❌'}")

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionnaire de migrations GESTIA")
    parser.add_argument('action', choices=['migrate', 'status'], 
                       help='Action à effectuer')
    parser.add_argument('--env', default='development', 
                       choices=['development', 'test', 'production'],
                       help='Environnement cible')
    
    args = parser.parse_args()
    
    migrator = DatabaseMigrator(args.env)
    
    if args.action == 'migrate':
        migrator.migrate()
    elif args.action == 'status':
        migrator.show_status()

if __name__ == "__main__":
    main() 