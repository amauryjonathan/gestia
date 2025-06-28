#!/usr/bin/env python3
"""
Script d'import CSV pour GESTIA
===============================

Ce script permet d'importer des données depuis des fichiers CSV.
"""

import sys
import os
import csv
from datetime import datetime
import argparse

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from gestia.core.database import init_database, db_manager, set_environment
from gestia.core.services import AppareilService, TechnicienService
from gestia.core.models import EtatAppareil

def importer_appareils(csv_file, env='development'):
    """Importe des appareils depuis un fichier CSV"""
    print(f"📱 Import d'appareils depuis {csv_file}...")
    
    # Définir l'environnement
    set_environment(env)
    init_database()
    db = db_manager.get_session()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Parser les données
                    id_appareil = row.get('ID_Appareil', '').strip()
                    marque = row.get('Marque', '').strip()
                    modele = row.get('Modele', '').strip()
                    date_reception_str = row.get('DateReception', '').strip()
                    etat_str = row.get('Etat', 'EN_TEST').strip()
                    date_vente_str = row.get('DateMiseEnVente', '').strip()
                    
                    # Validation des données obligatoires
                    if not marque or not modele or not date_reception_str:
                        print(f"  ⚠️ Ligne ignorée : données manquantes")
                        continue
                    
                    # Parser les dates
                    try:
                        date_reception = datetime.strptime(date_reception_str, '%Y-%m-%d').date()
                    except ValueError:
                        print(f"  ⚠️ Date de réception invalide : {date_reception_str}")
                        continue
                    
                    # Parser l'état
                    try:
                        etat = EtatAppareil(etat_str)
                    except ValueError:
                        print(f"  ⚠️ État invalide : {etat_str}, utilisation de EN_TEST")
                        etat = EtatAppareil.EN_TEST
                    
                    # Créer l'appareil
                    if id_appareil and id_appareil.startswith('APP_'):
                        # Utiliser l'ID fourni
                        appareil = AppareilService.creer_appareil(db, marque, modele, date_reception)
                        # Modifier l'ID si nécessaire
                        if appareil.ID_Appareil != id_appareil:
                            print(f"  ⚠️ ID modifié : {appareil.ID_Appareil} -> {id_appareil}")
                    else:
                        appareil = AppareilService.creer_appareil(db, marque, modele, date_reception)
                    
                    # Modifier l'état si différent de EN_TEST
                    if etat != EtatAppareil.EN_TEST:
                        AppareilService.modifier_etat_appareil(db, appareil.ID_Appareil, etat)
                    
                    # Ajouter la date de mise en vente si fournie
                    if date_vente_str:
                        try:
                            date_vente = datetime.strptime(date_vente_str, '%Y-%m-%d').date()
                            appareil.DateMiseEnVente = date_vente
                            db.commit()
                        except ValueError:
                            print(f"  ⚠️ Date de vente invalide : {date_vente_str}")
                    
                    print(f"  ✅ {marque} {modele} importé (ID: {appareil.ID_Appareil})")
                    
                except Exception as e:
                    print(f"  ❌ Erreur lors de l'import de la ligne : {e}")
                    continue
        
        print("✅ Import des appareils terminé !")
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {csv_file}")
    except Exception as e:
        print(f"❌ Erreur lors de l'import : {e}")
    finally:
        db.close()

def importer_techniciens(csv_file, env='development'):
    """Importe des techniciens depuis un fichier CSV"""
    print(f"👨‍🔧 Import de techniciens depuis {csv_file}...")
    
    # Définir l'environnement
    set_environment(env)
    init_database()
    db = db_manager.get_session()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # Parser les données
                    id_technicien = row.get('ID_Technicien', '').strip()
                    nom = row.get('Nom', '').strip()
                    prenom = row.get('Prenom', '').strip()
                    
                    # Validation des données obligatoires
                    if not nom or not prenom:
                        print(f"  ⚠️ Ligne ignorée : nom ou prénom manquant")
                        continue
                    
                    # Créer le technicien
                    technicien = TechnicienService.creer_technicien(db, nom, prenom)
                    
                    print(f"  ✅ {prenom} {nom} importé (ID: {technicien.ID_Technicien})")
                    
                except Exception as e:
                    print(f"  ❌ Erreur lors de l'import de la ligne : {e}")
                    continue
        
        print("✅ Import des techniciens terminé !")
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {csv_file}")
    except Exception as e:
        print(f"❌ Erreur lors de l'import : {e}")
    finally:
        db.close()

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Import CSV pour GESTIA")
    parser.add_argument('type', choices=['appareils', 'techniciens'], 
                       help='Type de données à importer')
    parser.add_argument('fichier', help='Fichier CSV à importer')
    parser.add_argument('--env', choices=['development', 'production', 'test'], 
                       default='development', help='Environnement (défaut: development)')
    
    args = parser.parse_args()
    
    if args.type == 'appareils':
        importer_appareils(args.fichier, args.env)
    elif args.type == 'techniciens':
        importer_techniciens(args.fichier, args.env)

if __name__ == "__main__":
    main() 