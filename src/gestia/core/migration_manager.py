#!/usr/bin/env python3
"""
Gestionnaire de migrations automatique
=====================================

Module pour gérer automatiquement les migrations de base de données
au démarrage de l'application.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Ajouter le répertoire tools au path pour importer le migrator
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..', '..')
tools_path = os.path.join(project_root, 'tools', 'tools', 'db')
sys.path.insert(0, tools_path)

try:
    from migrate_db import DatabaseMigrator
except ImportError as e:
    print(f"❌ Erreur d'import du module de migration: {e}")
    print(f"   Chemin recherché: {tools_path}")
    print("   Vérifiez que le fichier migrate_db.py existe dans tools/tools/db/")
    raise

class MigrationManager:
    """Gestionnaire de migrations automatique pour GESTIA"""
    
    def __init__(self, environment='development'):
        self.environment = environment
        self.migrator = DatabaseMigrator(environment)
    
    def check_and_migrate_if_needed(self, verbose=True):
        """
        Vérifie s'il y a des migrations en attente et les applique si nécessaire.
        
        Args:
            verbose (bool): Afficher les messages de progression
            
        Returns:
            bool: True si des migrations ont été appliquées, False sinon
        """
        if verbose:
            print("🔍 Vérification des migrations de base de données...")
        
        try:
            # Récupérer les migrations appliquées et disponibles
            applied_migrations = self.migrator.get_applied_migrations()
            all_migrations = self.migrator.get_all_migrations()
            
            # Identifier les migrations en attente
            pending_migrations = [
                migration for migration in all_migrations 
                if migration['version'] not in applied_migrations
            ]
            
            if pending_migrations:
                if verbose:
                    print(f"🔄 {len(pending_migrations)} migration(s) en attente détectée(s)")
                    for migration in pending_migrations:
                        print(f"   - {migration['version']}: {migration['description']}")
                    print("🚀 Application des migrations...")
                
                # Appliquer les migrations
                self.migrator.migrate()
                
                if verbose:
                    print("✅ Migrations appliquées avec succès !")
                
                return True
            else:
                if verbose:
                    print("✅ Base de données à jour - aucune migration nécessaire")
                
                return False
                
        except Exception as e:
            if verbose:
                print(f"❌ Erreur lors de la vérification des migrations: {e}")
            raise
    
    def get_migration_status(self):
        """
        Retourne le statut détaillé des migrations.
        
        Returns:
            dict: Statut des migrations
        """
        try:
            applied_migrations = self.migrator.get_applied_migrations()
            all_migrations = self.migrator.get_all_migrations()
            
            pending_migrations = [
                migration for migration in all_migrations 
                if migration['version'] not in applied_migrations
            ]
            
            return {
                'environment': self.environment,
                'total_migrations': len(all_migrations),
                'applied_migrations': len(applied_migrations),
                'pending_migrations': len(pending_migrations),
                'pending_details': pending_migrations,
                'is_up_to_date': len(pending_migrations) == 0
            }
        except Exception as e:
            return {
                'error': str(e),
                'is_up_to_date': False
            }
    
    def force_migrate(self, verbose=True):
        """
        Force l'application de toutes les migrations (même déjà appliquées).
        
        Args:
            verbose (bool): Afficher les messages de progression
        """
        if verbose:
            print("🔄 Application forcée de toutes les migrations...")
        
        self.migrator.migrate()
        
        if verbose:
            print("✅ Toutes les migrations ont été appliquées !")

# Instance globale pour faciliter l'utilisation
migration_manager = MigrationManager()

def auto_migrate_on_startup(environment='development', verbose=True):
    """
    Fonction utilitaire pour migrer automatiquement au démarrage.
    
    Args:
        environment (str): Environnement cible
        verbose (bool): Afficher les messages de progression
        
    Returns:
        bool: True si des migrations ont été appliquées, False sinon
    """
    global migration_manager
    
    # Mettre à jour l'environnement si nécessaire
    if migration_manager.environment != environment:
        migration_manager = MigrationManager(environment)
    
    return migration_manager.check_and_migrate_if_needed(verbose)

def get_migration_status(environment='development'):
    """
    Fonction utilitaire pour obtenir le statut des migrations.
    
    Args:
        environment (str): Environnement cible
        
    Returns:
        dict: Statut des migrations
    """
    global migration_manager
    
    # Mettre à jour l'environnement si nécessaire
    if migration_manager.environment != environment:
        migration_manager = MigrationManager(environment)
    
    return migration_manager.get_migration_status() 