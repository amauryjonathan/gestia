#!/usr/bin/env python3
"""
Créateur de migrations GESTIA
============================

Script pour créer facilement de nouvelles migrations.
"""

import sys
import os
from datetime import datetime

def create_migration():
    """Crée une nouvelle migration"""
    print("🆕 Création d'une nouvelle migration")
    print("=" * 40)
    
    # Demander les informations
    version = input("Version de la migration (ex: 005_add_champ): ")
    description = input("Description (ex: Ajout du champ Prix): ")
    
    print("\n📝 Commandes SQL à exécuter:")
    print("(Tapez 'fin' quand vous avez terminé)")
    
    sql_commands = []
    while True:
        command = input(f"SQL {len(sql_commands) + 1}: ")
        if command.lower() == 'fin':
            break
        sql_commands.append(command)
    
    if not sql_commands:
        print("❌ Aucune commande SQL fournie")
        return
    
    # Afficher la migration à ajouter
    print("\n📋 Migration à ajouter dans migrate_db.py:")
    print("-" * 40)
    print(f"{{")
    print(f"    'version': '{version}',")
    print(f"    'description': '{description}',")
    print(f"    'sql': [")
    for cmd in sql_commands:
        print(f"        '{cmd}',")
    print(f"    ]")
    print(f"}},")
    
    # Demander confirmation
    confirm = input("\n✅ Ajouter cette migration ? (y/N): ")
    if confirm.lower() == 'y':
        add_migration_to_file(version, description, sql_commands)
        print("✅ Migration ajoutée !")
        print("🔄 N'oubliez pas de lancer: python tools/tools/db/migrate_db.py migrate --env production")
    else:
        print("❌ Migration annulée")

def add_migration_to_file(version, description, sql_commands):
    """Ajoute la migration au fichier migrate_db.py"""
    migrate_file = "tools/tools/db/migrate_db.py"
    
    # Lire le fichier
    with open(migrate_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la position pour insérer
    insert_pos = content.find("# 🚀 POUR AJOUTER UNE NOUVELLE MIGRATION")
    if insert_pos == -1:
        print("❌ Impossible de trouver la position d'insertion")
        return
    
    # Créer la nouvelle migration
    new_migration = f"""
            {{
                'version': '{version}',
                'description': '{description}',
                'sql': ["""
    
    for cmd in sql_commands:
        new_migration += f"\n                    '{cmd}',"
    
    new_migration += """
                ]
            },"""
    
    # Insérer avant le commentaire
    new_content = content[:insert_pos] + new_migration + "\n            " + content[insert_pos:]
    
    # Écrire le fichier
    with open(migrate_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

def show_existing_migrations():
    """Affiche les migrations existantes"""
    print("📋 Migrations existantes:")
    print("=" * 40)
    
    try:
        from migrate_db import DatabaseMigrator
        migrator = DatabaseMigrator('development')
        migrations = migrator.get_all_migrations()
        
        for i, migration in enumerate(migrations, 1):
            print(f"{i}. {migration['version']}: {migration['description']}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Point d'entrée principal"""
    print("🛠️  Créateur de migrations GESTIA")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Créer une nouvelle migration")
        print("2. Voir les migrations existantes")
        print("3. Quitter")
        
        choice = input("\nVotre choix: ")
        
        if choice == "1":
            create_migration()
        elif choice == "2":
            show_existing_migrations()
        elif choice == "3":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main() 