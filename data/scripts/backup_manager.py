#!/usr/bin/env python3
"""
Gestionnaire de sauvegardes pour GESTIA
=======================================

Ce script permet de sauvegarder et restaurer les bases de données.
"""

import sys
import os
import shutil
from datetime import datetime, timedelta
import argparse

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from gestia.core.database import db_manager, set_environment

def lister_sauvegardes():
    """Liste toutes les sauvegardes disponibles"""
    backup_dir = "data/backups"
    if not os.path.exists(backup_dir):
        print("❌ Aucune sauvegarde trouvée")
        return []
    
    sauvegardes = []
    for fichier in os.listdir(backup_dir):
        if fichier.endswith('.db'):
            chemin = os.path.join(backup_dir, fichier)
            stat = os.stat(chemin)
            taille = stat.st_size
            date_modif = datetime.fromtimestamp(stat.st_mtime)
            
            sauvegardes.append({
                'nom': fichier,
                'chemin': chemin,
                'taille': taille,
                'date': date_modif
            })
    
    # Trier par date (plus récent en premier)
    sauvegardes.sort(key=lambda x: x['date'], reverse=True)
    
    return sauvegardes

def afficher_sauvegardes():
    """Affiche la liste des sauvegardes"""
    sauvegardes = lister_sauvegardes()
    
    if not sauvegardes:
        print("📋 Aucune sauvegarde disponible")
        return
    
    print("📋 Sauvegardes disponibles :")
    print("-" * 80)
    print(f"{'N°':<3} {'Nom':<30} {'Taille':<10} {'Date':<20} {'Heure':<10}")
    print("-" * 80)
    
    for i, sauvegarde in enumerate(sauvegardes, 1):
        taille_mb = sauvegarde['taille'] / (1024 * 1024)
        date_str = sauvegarde['date'].strftime('%Y-%m-%d')
        heure_str = sauvegarde['date'].strftime('%H:%M:%S')
        
        print(f"{i:<3} {sauvegarde['nom']:<30} {taille_mb:.1f} MB {date_str:<20} {heure_str:<10}")

def creer_sauvegarde(env='development', nom_personnalise=None):
    """Crée une sauvegarde de la base de données"""
    print(f"💾 Création d'une sauvegarde de l'environnement '{env}'...")
    
    # Définir l'environnement
    set_environment(env)
    
    # Créer la sauvegarde
    if db_manager.backup_database(nom_personnalise):
        print("✅ Sauvegarde créée avec succès !")
    else:
        print("❌ Échec de la création de la sauvegarde")

def restaurer_sauvegarde(numero_sauvegarde):
    """Restaure une sauvegarde"""
    sauvegardes = lister_sauvegardes()
    
    if not sauvegardes:
        print("❌ Aucune sauvegarde disponible")
        return
    
    try:
        numero = int(numero_sauvegarde) - 1
        if numero < 0 or numero >= len(sauvegardes):
            print(f"❌ Numéro de sauvegarde invalide. Choisissez entre 1 et {len(sauvegardes)}")
            return
        
        sauvegarde = sauvegardes[numero]
        
        # Demander confirmation
        print(f"⚠️ ATTENTION : Vous allez restaurer la sauvegarde :")
        print(f"   Nom : {sauvegarde['nom']}")
        print(f"   Date : {sauvegarde['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Taille : {sauvegarde['taille'] / (1024 * 1024):.1f} MB")
        
        reponse = input("\n❓ Êtes-vous sûr ? (oui/non) : ").lower().strip()
        if reponse not in ['oui', 'o', 'yes', 'y']:
            print("❌ Restauration annulée")
            return
        
        # Déterminer l'environnement cible
        env = input("🎯 Environnement cible (development/production/test) : ").strip()
        if env not in ['development', 'production', 'test']:
            print("❌ Environnement invalide")
            return
        
        # Créer une sauvegarde de l'état actuel
        print("💾 Création d'une sauvegarde de l'état actuel...")
        set_environment(env)
        db_manager.backup_database(f"avant_restauration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        
        # Restaurer
        db_path = db_manager.get_database_path()
        if db_path:
            try:
                shutil.copy2(sauvegarde['chemin'], db_path)
                print(f"✅ Sauvegarde restaurée avec succès dans l'environnement '{env}' !")
            except Exception as e:
                print(f"❌ Erreur lors de la restauration : {e}")
        else:
            print("❌ Impossible de déterminer le chemin de la base de données")
    
    except ValueError:
        print("❌ Numéro de sauvegarde invalide")

def nettoyer_anciennes_sauvegardes(jours=30):
    """Supprime les sauvegardes plus anciennes que X jours"""
    sauvegardes = lister_sauvegardes()
    date_limite = datetime.now() - timedelta(days=jours)
    
    a_supprimer = [s for s in sauvegardes if s['date'] < date_limite]
    
    if not a_supprimer:
        print(f"✅ Aucune sauvegarde à supprimer (plus récentes que {jours} jours)")
        return
    
    print(f"🗑️ Suppression des sauvegardes plus anciennes que {jours} jours...")
    
    for sauvegarde in a_supprimer:
        try:
            os.remove(sauvegarde['chemin'])
            print(f"  ✅ Supprimé : {sauvegarde['nom']}")
        except Exception as e:
            print(f"  ❌ Erreur lors de la suppression de {sauvegarde['nom']} : {e}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Gestionnaire de sauvegardes GESTIA")
    parser.add_argument('action', choices=['list', 'backup', 'restore', 'clean'], 
                       help='Action à effectuer')
    parser.add_argument('--env', choices=['development', 'production', 'test'], 
                       default='development', help='Environnement (défaut: development)')
    parser.add_argument('--nom', help='Nom personnalisé pour la sauvegarde')
    parser.add_argument('--numero', type=int, help='Numéro de la sauvegarde à restaurer')
    parser.add_argument('--jours', type=int, default=30, 
                       help='Nombre de jours pour le nettoyage (défaut: 30)')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        afficher_sauvegardes()
    
    elif args.action == 'backup':
        creer_sauvegarde(args.env, args.nom)
    
    elif args.action == 'restore':
        if args.numero is None:
            print("❌ Veuillez spécifier le numéro de sauvegarde avec --numero")
            return
        restaurer_sauvegarde(args.numero)
    
    elif args.action == 'clean':
        nettoyer_anciennes_sauvegardes(args.jours)

if __name__ == "__main__":
    main() 