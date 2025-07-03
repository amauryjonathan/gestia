#!/usr/bin/env python3
"""
Utilitaire de création de migrations
===================================

Script pour créer facilement de nouvelles migrations de base de données.
"""

import sys
import os
import argparse
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def create_migration_template(version, description, sql_commands):
    """Crée un template de migration"""
    
    template = f'''{{
    'version': '{version}',
    'description': '{description}',
    'sql': [
'''
    
    for cmd in sql_commands:
        template += f"        '{cmd}',\n"
    
    template += '''    ]
}'''
    
    return template

def get_next_version():
    """Génère automatiquement le prochain numéro de version"""
    # Lire le fichier migrate_db.py pour trouver la dernière version
    migrate_file = os.path.join(os.path.dirname(__file__), 'migrate_db.py')
    
    if not os.path.exists(migrate_file):
        return '001'
    
    with open(migrate_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher les versions existantes
    import re
    versions = re.findall(r"'(\d{3}_[^']+)'", content)
    
    if not versions:
        return '001'
    
    # Extraire les numéros et trouver le plus grand
    numbers = [int(v.split('_')[0]) for v in versions]
    next_num = max(numbers) + 1
    
    return f"{next_num:03d}"

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Créateur de migrations GESTIA")
    parser.add_argument('--name', required=True, 
                       help='Nom de la migration (ex: add_user_table)')
    parser.add_argument('--description', required=True,
                       help='Description de la migration')
    parser.add_argument('--sql', nargs='+', required=True,
                       help='Commandes SQL à exécuter')
    parser.add_argument('--version', 
                       help='Version manuelle (ex: 004) - auto-générée si non spécifiée')
    parser.add_argument('--preview', action='store_true',
                       help='Afficher seulement le template sans l\'ajouter')
    
    args = parser.parse_args()
    
    # Générer la version si non spécifiée
    if not args.version:
        version_num = get_next_version()
    else:
        version_num = args.version.zfill(3)
    
    version = f"{version_num}_{args.name}"
    
    print(f"🚀 Création de migration: {version}")
    print(f"📝 Description: {args.description}")
    print(f"🔧 Commandes SQL:")
    for cmd in args.sql:
        print(f"   - {cmd}")
    print()
    
    # Générer le template
    template = create_migration_template(version, args.description, args.sql)
    
    if args.preview:
        print("📋 Template généré:")
        print("=" * 50)
        print(template)
        print("=" * 50)
        print("\n💡 Pour l'ajouter manuellement, copiez ce template dans la méthode get_all_migrations()")
        return
    
    # Ajouter automatiquement au fichier migrate_db.py
    migrate_file = os.path.join(os.path.dirname(__file__), 'migrate_db.py')
    
    if not os.path.exists(migrate_file):
        print(f"❌ Fichier {migrate_file} non trouvé")
        return
    
    # Lire le fichier
    with open(migrate_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la position pour insérer la nouvelle migration
    # Chercher la fin de la liste des migrations
    import re
    
    # Pattern pour trouver la fin de la liste des migrations
    pattern = r'(\s+)\]\s+# 🚀 POUR AJOUTER UNE NOUVELLE MIGRATION'
    
    match = re.search(pattern, content)
    if not match:
        print("❌ Impossible de trouver la position d'insertion dans le fichier")
        return
    
    # Préparer la nouvelle migration
    indent = match.group(1)
    new_migration = f"{indent}{template},\n{indent}"
    
    # Insérer la migration
    new_content = re.sub(pattern, f"{new_migration}]\\1# 🚀 POUR AJOUTER UNE NOUVELLE MIGRATION", content)
    
    # Sauvegarder le fichier
    with open(migrate_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Migration ajoutée avec succès !")
    print(f"📁 Fichier modifié: {migrate_file}")
    print()
    print("🔄 Pour appliquer la migration:")
    print(f"   python tools/tools/db/migrate_db.py migrate --env development")
    print()
    print("📊 Pour vérifier le statut:")
    print(f"   python tools/tools/db/migrate_db.py status --env development")

if __name__ == "__main__":
    main() 