#!/usr/bin/env python3
"""
Initialisation de base de données
=================================

Script pour initialiser proprement la base de données avec le bon schéma.
"""

import sys
import os
import shutil

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import init_database, set_environment
from gestia.core.services import AppareilService, TechnicienService

def init_environment(environment='development', force=False):
    """Initialise un environnement complet"""
    print(f"🚀 Initialisation de l'environnement: {environment}")
    print("=" * 50)
    
    # Définir l'environnement
    set_environment(environment)
    
    # Chemin de la base de données
    db_path = f"data/{environment}/gestia.db"
    
    # Vérifier si la base existe déjà
    if os.path.exists(db_path) and not force:
        print(f"⚠️  La base de données existe déjà: {db_path}")
        response = input("Voulez-vous la recréer ? (y/N): ")
        if response.lower() != 'y':
            print("❌ Initialisation annulée")
            return False
    
    # Supprimer l'ancienne base si elle existe
    if os.path.exists(db_path):
        print(f"🗑️  Suppression de l'ancienne base: {db_path}")
        os.remove(db_path)
    
    # Créer le dossier si nécessaire
    os.makedirs(f"data/{environment}", exist_ok=True)
    
    # Initialiser la base de données
    print("🔧 Initialisation de la base de données...")
    init_database()
    
    # Exécuter les migrations
    print("🔄 Application des migrations...")
    from migrate_db import DatabaseMigrator
    migrator = DatabaseMigrator(environment)
    migrator.migrate()
    
    # Générer des données de test
    print("📊 Génération de données de test...")
    generate_test_data(environment)
    
    print("✅ Initialisation terminée avec succès !")
    return True

def generate_test_data(environment):
    """Génère des données de test"""
    from gestia.core.database import db_manager
    from gestia.core.models import EtatAppareil
    from datetime import date, timedelta
    import random
    
    db = db_manager.get_session()
    
    try:
        # Créer quelques techniciens
        techniciens = [
            ("Dupont", "Jean"),
            ("Martin", "Marie"),
            ("Bernard", "Pierre"),
            ("Petit", "Sophie"),
            ("Robert", "Lucas")
        ]
        
        for nom, prenom in techniciens:
            TechnicienService.creer_technicien(db, nom, prenom)
        
        # Créer quelques appareils avec les nouveaux champs
        appareils_data = [
            {
                'marque': 'Samsung',
                'modele': 'WW90T534DAW',
                'serie': 'EcoBubble',
                'capacite': '9kg',
                'technologie': 'Inverter',
                'variante': 'A',
                'reference_complete': 'Samsung WW90T534DAW-EcoBubble-9kg-Inverter-A'
            },
            {
                'marque': 'LG',
                'modele': 'F4WV510S0E',
                'serie': 'Steam',
                'capacite': '10.5kg',
                'technologie': 'Direct Drive',
                'variante': 'C',
                'reference_complete': 'LG F4WV510S0E-Steam-10.5kg-DirectDrive-C'
            },
            {
                'marque': 'Bosch',
                'modele': 'WAT28441FF',
                'serie': 'EcoSilence',
                'capacite': '8kg',
                'technologie': 'Brushless',
                'variante': 'B',
                'reference_complete': 'Bosch WAT28441FF-EcoSilence-8kg-Brushless-B'
            }
        ]
        
        for data in appareils_data:
            date_reception = date.today() - timedelta(days=random.randint(1, 30))
            appareil = AppareilService.creer_appareil(
                db, 
                data['marque'], 
                data['modele'], 
                date_reception
            )
            
            # Mettre à jour avec les nouveaux champs
            appareil.Serie = data['serie']
            appareil.Capacite = data['capacite']
            appareil.Technologie = data['technologie']
            appareil.Variante = data['variante']
            appareil.ReferenceComplete = data['reference_complete']
            
            # Assigner un état aléatoire
            appareil.Etat = random.choice(list(EtatAppareil))
            
            db.commit()
        
        print(f"✅ {len(techniciens)} techniciens et {len(appareils_data)} appareils créés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des données: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialisation de base de données GESTIA")
    parser.add_argument('--env', default='development', 
                       choices=['development', 'test', 'production'],
                       help='Environnement à initialiser')
    parser.add_argument('--force', action='store_true',
                       help='Forcer la recréation de la base')
    
    args = parser.parse_args()
    
    init_environment(args.env, args.force)

if __name__ == "__main__":
    main() 