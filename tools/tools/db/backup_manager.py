#!/usr/bin/env python3
"""
Gestionnaire de sauvegardes GESTIA
==================================

Script pour gérer les sauvegardes de base de données de manière professionnelle.
"""

import sys
import os
import shutil
import sqlite3
from datetime import datetime
import json

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import set_environment

class BackupManager:
    """Gestionnaire de sauvegardes de base de données"""
    
    def __init__(self):
        self.backup_dir = "data/backups"
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Crée le dossier de sauvegardes s'il n'existe pas"""
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, environment='development', description=""):
        """Crée une sauvegarde d'un environnement"""
        print(f"🔄 Création d'une sauvegarde pour l'environnement: {environment}")
        
        # Chemin de la base source
        source_db = f"data/{environment}/gestia.db"
        
        if not os.path.exists(source_db):
            print(f"❌ Base de données source non trouvée: {source_db}")
            return False
        
        # Nom du fichier de sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"gestia_{environment}_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            # Copier la base de données
            shutil.copy2(source_db, backup_path)
            
            # Créer un fichier de métadonnées
            metadata = {
                'environment': environment,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'source_size': os.path.getsize(source_db),
                'backup_size': os.path.getsize(backup_path)
            }
            
            metadata_path = backup_path.replace('.db', '.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Sauvegarde créée: {backup_name}")
            print(f"📁 Taille: {metadata['backup_size'] / (1024*1024):.1f} MB")
            print(f"📝 Description: {description}")
            
            return backup_path
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def list_backups(self):
        """Liste toutes les sauvegardes disponibles"""
        print("📋 Sauvegardes disponibles:")
        print("=" * 60)
        
        if not os.path.exists(self.backup_dir):
            print("❌ Aucun dossier de sauvegardes trouvé")
            return
        
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.db'):
                backup_path = os.path.join(self.backup_dir, file)
                metadata_path = backup_path.replace('.db', '.json')
                
                # Récupérer les métadonnées
                metadata = {}
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                backups.append({
                    'file': file,
                    'path': backup_path,
                    'size': os.path.getsize(backup_path),
                    'created': metadata.get('created_at', 'Inconnu'),
                    'environment': metadata.get('environment', 'Inconnu'),
                    'description': metadata.get('description', '')
                })
        
        # Trier par date de création (plus récent en premier)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        if not backups:
            print("📭 Aucune sauvegarde trouvée")
            return
        
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup['file']}")
            print(f"   📊 Taille: {backup['size'] / (1024*1024):.1f} MB")
            print(f"   🌍 Environnement: {backup['environment']}")
            print(f"   📅 Créée: {backup['created']}")
            if backup['description']:
                print(f"   📝 Description: {backup['description']}")
            print()
    
    def restore_backup(self, backup_file, environment='development', force=False):
        """Restaure une sauvegarde"""
        print(f"🔄 Restauration de la sauvegarde: {backup_file}")
        
        backup_path = os.path.join(self.backup_dir, backup_file)
        
        if not os.path.exists(backup_path):
            print(f"❌ Sauvegarde non trouvée: {backup_path}")
            return False
        
        # Chemin de destination
        target_db = f"data/{environment}/gestia.db"
        target_dir = os.path.dirname(target_db)
        
        # Créer le dossier de destination si nécessaire
        os.makedirs(target_dir, exist_ok=True)
        
        # Vérifier si la base de destination existe
        if os.path.exists(target_db) and not force:
            print(f"⚠️  La base de données de destination existe déjà: {target_db}")
            response = input("Voulez-vous la remplacer ? (y/N): ")
            if response.lower() != 'y':
                print("❌ Restauration annulée")
                return False
        
        try:
            # Créer une sauvegarde de la base actuelle (si elle existe)
            if os.path.exists(target_db):
                print("🔄 Création d'une sauvegarde de la base actuelle...")
                self.create_backup(environment, "Sauvegarde avant restauration")
            
            # Restaurer la sauvegarde
            shutil.copy2(backup_path, target_db)
            
            print(f"✅ Restauration terminée: {target_db}")
            print(f"📊 Taille restaurée: {os.path.getsize(target_db) / (1024*1024):.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la restauration: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count=5):
        """Nettoie les anciennes sauvegardes (garde les plus récentes)"""
        print(f"🧹 Nettoyage des sauvegardes (garde les {keep_count} plus récentes)")
        
        if not os.path.exists(self.backup_dir):
            print("❌ Aucun dossier de sauvegardes trouvé")
            return
        
        # Récupérer toutes les sauvegardes
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.db'):
                backup_path = os.path.join(self.backup_dir, file)
                metadata_path = backup_path.replace('.db', '.json')
                
                created = "1970-01-01T00:00:00"
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            created = metadata.get('created_at', created)
                    except:
                        pass
                
                backups.append({
                    'file': file,
                    'path': backup_path,
                    'metadata_path': metadata_path,
                    'created': created
                })
        
        # Trier par date de création
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        # Supprimer les anciennes sauvegardes
        to_delete = backups[keep_count:]
        
        if not to_delete:
            print("✅ Aucune sauvegarde à supprimer")
            return
        
        print(f"🗑️  Suppression de {len(to_delete)} sauvegardes anciennes:")
        for backup in to_delete:
            print(f"  - {backup['file']}")
            try:
                os.remove(backup['path'])
                if os.path.exists(backup['metadata_path']):
                    os.remove(backup['metadata_path'])
            except Exception as e:
                print(f"    ❌ Erreur: {e}")
        
        print(f"✅ Nettoyage terminé. {len(backups) - len(to_delete)} sauvegardes conservées.")

def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionnaire de sauvegardes GESTIA")
    parser.add_argument('action', 
                       choices=['create', 'list', 'restore', 'cleanup'],
                       help='Action à effectuer')
    parser.add_argument('--env', default='development',
                       choices=['development', 'test', 'production'],
                       help='Environnement cible')
    parser.add_argument('--description', default='',
                       help='Description de la sauvegarde')
    parser.add_argument('--backup-file', default='',
                       help='Fichier de sauvegarde à restaurer')
    parser.add_argument('--force', action='store_true',
                       help='Forcer la restauration')
    parser.add_argument('--keep', type=int, default=5,
                       help='Nombre de sauvegardes à conserver')
    
    args = parser.parse_args()
    
    manager = BackupManager()
    
    if args.action == 'create':
        manager.create_backup(args.env, args.description)
    
    elif args.action == 'list':
        manager.list_backups()
    
    elif args.action == 'restore':
        if not args.backup_file:
            print("❌ Veuillez spécifier le fichier de sauvegarde avec --backup-file")
            return
        manager.restore_backup(args.backup_file, args.env, args.force)
    
    elif args.action == 'cleanup':
        manager.cleanup_old_backups(args.keep)

if __name__ == "__main__":
    main() 