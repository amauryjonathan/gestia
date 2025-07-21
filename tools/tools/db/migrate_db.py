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
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..', '..')
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

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
    
    def mark_applied(self, version):
        """Marque manuellement une migration comme appliquée"""
        all_migrations = self.get_all_migrations()
        migration = next((m for m in all_migrations if m['version'] == version), None)
        
        if not migration:
            print(f"❌ Migration {version} non trouvée")
            return False
        
        print(f"✅ Marquage de la migration {version} comme appliquée")
        self.mark_migration_applied(version, migration['description'])
        return True
    
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
    
    def get_all_migrations(self):
        """Retourne toutes les migrations définies dans l'ordre"""
        return [
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
            },
            {
                'version': '003_add_test_diagnostic_fields',
                'description': 'Ajout des champs pour tests et diagnostics',
                'sql': [
                    'ALTER TABLE appareils ADD COLUMN ActionsAFaire TEXT',
                    'ALTER TABLE appareils ADD COLUMN SoucisMachine TEXT'
                ]
            },
            {
                'version': '004_add_numero_serie_field',
                'description': 'Ajout du champ NumeroSerie obligatoire',
                'sql': [
                    'ALTER TABLE appareils ADD COLUMN NumeroSerie TEXT'
                ]
            },
            # 🚀 POUR AJOUTER UNE NOUVELLE MIGRATION :
            # Ajoutez ici un nouveau dictionnaire avec :
            # - version: '005_nom_de_la_migration'
            # - description: 'Description claire de ce que fait la migration'
            # - sql: [liste des commandes SQL à exécuter]
        ]
    
    def migrate(self):
        """Exécute toutes les migrations nécessaires"""
        print(f"🚀 Début des migrations pour l'environnement: {self.environment}")
        print("=" * 60)
        
        applied_migrations = self.get_applied_migrations()
        all_migrations = self.get_all_migrations()
        
        # Exécuter les migrations non appliquées
        for migration in all_migrations:
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
        all_migrations = self.get_all_migrations()
        
        print("Migrations disponibles:")
        for migration in all_migrations:
            status = "✅" if migration['version'] in applied_migrations else "⏳"
            print(f"  {status} {migration['version']}: {migration['description']}")
        
        print(f"\nBase de données: {self.db_path}")
        print(f"Existe: {'✅' if os.path.exists(self.db_path) else '❌'}")
    
    def create_migration(self, version, description, sql_commands):
        """Crée une nouvelle migration (utilitaire pour développeurs)"""
        print(f"📝 Création d'une nouvelle migration: {version}")
        print(f"Description: {description}")
        print("Commandes SQL:")
        for cmd in sql_commands:
            print(f"  - {cmd}")
        
        # Ajouter la migration à la liste
        new_migration = {
            'version': version,
            'description': description,
            'sql': sql_commands
        }
        
        print("\n⚠️  Pour appliquer cette migration, ajoutez-la dans la méthode get_all_migrations()")
        print("   puis exécutez: python tools/tools/db/migrate_db.py migrate")

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionnaire de migrations GESTIA")
    parser.add_argument('action', choices=['migrate', 'status', 'create', 'mark-applied'], 
                       help='Action à effectuer')
    parser.add_argument('--env', default='development', 
                       choices=['development', 'test', 'production'],
                       help='Environnement cible')
    parser.add_argument('--version', help='Version de la migration (pour create ou mark-applied)')
    parser.add_argument('--description', help='Description de la migration (pour create)')
    parser.add_argument('--sql', nargs='+', help='Commandes SQL (pour create)')
    
    args = parser.parse_args()
    
    migrator = DatabaseMigrator(args.env)
    
    if args.action == 'migrate':
        migrator.migrate()
    elif args.action == 'status':
        migrator.show_status()
    elif args.action == 'create':
        if not all([args.version, args.description, args.sql]):
            print("❌ Pour créer une migration, spécifiez --version, --description et --sql")
            return
        migrator.create_migration(args.version, args.description, args.sql)
    elif args.action == 'mark-applied':
        if not args.version:
            print("❌ Pour marquer une migration comme appliquée, spécifiez --version")
            return
        migrator.mark_applied(args.version)

if __name__ == "__main__":
    main() 