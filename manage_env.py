#!/usr/bin/env python3
"""
Gestionnaire d'environnements GESTIA
====================================

Script principal pour gérer les environnements de développement, test et production.
"""

import os
import sys
import argparse
from datetime import datetime

def afficher_environnement_actuel():
    """Affiche l'environnement actuel"""
    env = os.getenv('GESTIA_ENV', 'development')
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
    """Change l'environnement actuel"""
    os.environ['GESTIA_ENV'] = env
    print(f"🔄 Environnement changé vers : {env}")
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
    
    # Importer et exécuter le script de génération
    sys.path.insert(0, 'src')
    try:
        from data.scripts.generate_test_data import generer_donnees_test
        generer_donnees_test()
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
   python manage_env.py status

2. Changer d'environnement :
   python manage_env.py switch --env development
   python manage_env.py switch --env production
   python manage_env.py switch --env test

3. Initialiser un nouvel environnement :
   python manage_env.py init --env development
   python manage_env.py init --env production
   python manage_env.py init --env test

4. Générer des données de test :
   python manage_env.py generate

5. Lancer l'application :
   python manage_env.py run

6. Afficher cette aide :
   python manage_env.py help

📁 STRUCTURE DES DONNÉES :
- data/gestia_dev.db     : Base de développement
- data/gestia_prod.db    : Base de production
- data/gestia_test.db    : Base de test
- data/backups/          : Sauvegardes
- data/scripts/          : Scripts utilitaires
- data/samples/          : Données d'exemple

⚠️ RECOMMANDATIONS :
- Utilisez 'development' pour vos tests et développements
- Utilisez 'production' uniquement pour les vraies données
- Faites des sauvegardes régulières de la production
- Ne commitez jamais les fichiers .db dans Git
""")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Gestionnaire d'environnements GESTIA")
    parser.add_argument('action', choices=['status', 'switch', 'init', 'generate', 'run', 'help'],
                       help='Action à effectuer')
    parser.add_argument('--env', choices=['development', 'production', 'test'],
                       help='Environnement cible')
    
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
    
    elif args.action == 'generate':
        generer_donnees_test()
    
    elif args.action == 'run':
        lancer_application()
    
    elif args.action == 'help':
        afficher_aide()

if __name__ == "__main__":
    main() 