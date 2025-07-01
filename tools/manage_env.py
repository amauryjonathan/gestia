#!/usr/bin/env python3
"""
Gestionnaire d'environnements GESTIA
====================================

Script principal pour gérer les environnements de développement, test et production.
"""

import os
import sys
import argparse
import json
from datetime import datetime

CONFIG_FILE = "data/.env_config.json"

def charger_environnement():
    """Charge l'environnement depuis le fichier de configuration"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                env = config.get('environment', 'development')
                os.environ['GESTIA_ENV'] = env
                return env
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement de la configuration : {e}")
    return 'development'

def sauvegarder_environnement(env):
    """Sauvegarde l'environnement dans le fichier de configuration"""
    try:
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)
        
        config = {'environment': env}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"⚠️ Erreur lors de la sauvegarde de la configuration : {e}")

def afficher_environnement_actuel():
    """Affiche l'environnement actuel"""
    # Charger l'environnement depuis la configuration
    env = charger_environnement()
    print(f"🎯 Environnement actuel : {env}")
    
    # Afficher le chemin de la base de données
    if env == 'development':
        db_path = "data/gestia_dev.db"
    elif env == 'production':
        db_path = "data/gestia_prod.db"
    elif env == 'test':
        db_path = "data/gestia_test.db"
    else:
        db_path = "data/gestia_dev.db"
    
    if os.path.exists(db_path):
        taille = os.path.getsize(db_path) / (1024 * 1024)
        date_modif = datetime.fromtimestamp(os.path.getmtime(db_path))
        print(f"📁 Base de données : {db_path}")
        print(f"📊 Taille : {taille:.1f} MB")
        print(f"🕒 Dernière modification : {date_modif.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"📁 Base de données : {db_path} (n'existe pas encore)")

def changer_environnement(env):
    """Change l'environnement actuel et le sauvegarde"""
    os.environ['GESTIA_ENV'] = env
    sauvegarder_environnement(env)
    print(f"🔄 Environnement changé vers : {env}")
    print(f"💾 Configuration sauvegardée dans : {CONFIG_FILE}")
    afficher_environnement_actuel()

def initialiser_environnement(env):
    """Initialise un nouvel environnement"""
    print(f"🚀 Initialisation de l'environnement '{env}'...")
    
    # Changer l'environnement
    changer_environnement(env)
    
    # Importer et initialiser la base de données
    sys.path.insert(0, 'src')
    from gestia.core.database import init_database
    
    try:
        init_database()
        print(f"✅ Environnement '{env}' initialisé avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")

def generer_donnees_test():
    """Génère des données de test pour l'environnement actuel"""
    print("🎲 Génération de données de test...")
    
    # Exécuter le script de génération directement
    try:
        import subprocess
        import os
        
        # Obtenir le chemin du script de génération
        script_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scripts', 'generate_test_data.py')
        
        # Exécuter le script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Erreur lors de la génération : {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")

def lancer_application():
    """Lance l'application GESTIA"""
    print("🚀 Lancement de l'application GESTIA...")
    
    # Importer et lancer l'application
    try:
        from main import main
        main()
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")

def afficher_aide():
    """Affiche l'aide détaillée"""
    print("""
🎯 GESTIONNAIRE D'ENVIRONNEMENTS GESTIA
=======================================

Ce script vous permet de gérer facilement les différents environnements
de votre application GESTIA.

📋 ENVIRONNEMENTS DISPONIBLES :
- development : Pour le développement (données virtuelles)
- production  : Pour la production (données réelles)
- test        : Pour les tests (copie des données réelles)

🛠️ COMMANDES DISPONIBLES :

1. Afficher l'environnement actuel :
   python tools/manage_env.py status

2. Changer d'environnement :
   python tools/manage_env.py switch --env development
   python tools/manage_env.py switch --env production
   python tools/manage_env.py switch --env test

3. Initialiser un nouvel environnement :
   python tools/manage_env.py init --env development
   python tools/manage_env.py init --env production
   python tools/manage_env.py init --env test

4. Migrer la base de données :
   python tools/manage_env.py migrate --env development
   python tools/manage_env.py migrate --env production

5. Vérifier le statut des migrations :
   python tools/manage_env.py migrate-status --env development

6. Réinitialiser complètement un environnement :
   python tools/manage_env.py reset --env development --force

7. Générer des données de test :
   python tools/manage_env.py generate

8. Lancer l'application :
   python tools/manage_env.py run

9. Afficher cette aide :
   python tools/manage_env.py help

📁 STRUCTURE DES DONNÉES :
- data/development/gestia.db  : Base de développement
- data/production/gestia.db   : Base de production
- data/test/gestia.db         : Base de test
- data/backups/               : Sauvegardes
- data/scripts/               : Scripts utilitaires
- data/samples/               : Données d'exemple

⚠️ RECOMMANDATIONS :
- Utilisez 'development' pour vos tests et développements
- Utilisez 'production' uniquement pour les vraies données
- Faites des sauvegardes régulières de la production
- Ne commitez jamais les fichiers .db dans Git
- Utilisez 'migrate' pour mettre à jour le schéma de base
- Utilisez 'reset' avec précaution (supprime toutes les données)
""")

def migrer_base_donnees(env):
    """Migre la base de données vers le schéma le plus récent"""
    print(f"🔄 Migration de la base de données pour l'environnement '{env}'...")
    
    try:
        from migrate_db import DatabaseMigrator
        migrator = DatabaseMigrator(env)
        migrator.migrate()
        print(f"✅ Migration terminée avec succès pour l'environnement '{env}'")
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")

def afficher_statut_migrations(env):
    """Affiche le statut des migrations"""
    try:
        from migrate_db import DatabaseMigrator
        migrator = DatabaseMigrator(env)
        migrator.show_status()
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du statut : {e}")

def reinitialiser_environnement(env, force=False):
    """Réinitialise complètement un environnement"""
    print(f"🔄 Réinitialisation complète de l'environnement '{env}'...")
    
    try:
        from init_db import init_environment
        if init_environment(env, force):
            print(f"✅ Environnement '{env}' réinitialisé avec succès !")
        else:
            print(f"❌ Réinitialisation annulée pour l'environnement '{env}'")
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation : {e}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Gestionnaire d'environnements GESTIA")
    parser.add_argument('action', 
                       choices=['status', 'switch', 'init', 'migrate', 'migrate-status', 
                               'reset', 'generate', 'run', 'help'],
                       help='Action à effectuer')
    parser.add_argument('--env', choices=['development', 'production', 'test'],
                       help='Environnement cible')
    parser.add_argument('--force', action='store_true',
                       help='Forcer l\'action (pour reset)')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        afficher_environnement_actuel()
    
    elif args.action == 'switch':
        if not args.env:
            print("❌ Veuillez spécifier l'environnement avec --env")
            return
        changer_environnement(args.env)
    
    elif args.action == 'init':
        if not args.env:
            print("❌ Veuillez spécifier l'environnement avec --env")
            return
        initialiser_environnement(args.env)
    
    elif args.action == 'migrate':
        if not args.env:
            print("❌ Veuillez spécifier l'environnement avec --env")
            return
        migrer_base_donnees(args.env)
    
    elif args.action == 'migrate-status':
        if not args.env:
            print("❌ Veuillez spécifier l'environnement avec --env")
            return
        afficher_statut_migrations(args.env)
    
    elif args.action == 'reset':
        if not args.env:
            print("❌ Veuillez spécifier l'environnement avec --env")
            return
        reinitialiser_environnement(args.env, args.force)
    
    elif args.action == 'generate':
        generer_donnees_test()
    
    elif args.action == 'run':
        lancer_application()
    
    elif args.action == 'help':
        afficher_aide()

if __name__ == "__main__":
    main() 