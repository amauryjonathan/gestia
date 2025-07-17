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

    def smart_migrate(self, verbose=True):
        """
        Migration intelligente qui vérifie l'état actuel de la base de données
        et marque automatiquement les migrations comme appliquées si les colonnes existent déjà.
        
        Args:
            verbose (bool): Afficher les messages de progression
            
        Returns:
            bool: True si des migrations ont été appliquées, False sinon
        """
        if verbose:
            print("🧠 Migration intelligente - Vérification de l'état actuel...")
        
        try:
            # 1. Vérifier quelles colonnes existent déjà dans la table appareils
            existing_columns = self._get_existing_columns()
            
            if verbose:
                print(f"📊 Colonnes existantes dans 'appareils': {existing_columns}")
            
            # 2. Récupérer toutes les migrations
            all_migrations = self.migrator.get_all_migrations()
            applied_migrations = self.migrator.get_applied_migrations()
            
            # 3. Analyser chaque migration
            migrations_to_mark = []
            migrations_to_apply = []
            
            for migration in all_migrations:
                if migration['version'] in applied_migrations:
                    if verbose:
                        print(f"✅ {migration['version']}: Déjà appliquée")
                    continue
                
                # Vérifier si les colonnes de cette migration existent déjà
                if self._migration_columns_exist(migration, existing_columns):
                    migrations_to_mark.append(migration)
                    if verbose:
                        print(f"🎯 {migration['version']}: Colonnes existent, marquage comme appliquée")
                else:
                    migrations_to_apply.append(migration)
                    if verbose:
                        print(f"🔄 {migration['version']}: Colonnes manquantes, application nécessaire")
            
            # 4. Marquer les migrations comme appliquées si les colonnes existent
            for migration in migrations_to_mark:
                self.migrator.mark_migration_applied(migration['version'], migration['description'])
                if verbose:
                    print(f"✅ Marquage: {migration['version']} comme appliquée")
            
            # 5. Appliquer les migrations manquantes
            if migrations_to_apply:
                if verbose:
                    print(f"🚀 Application de {len(migrations_to_apply)} migration(s)...")
                
                for migration in migrations_to_apply:
                    self.migrator.run_migration(
                        migration['version'],
                        migration['description'],
                        migration['sql']
                    )
                
                if verbose:
                    print("✅ Migrations appliquées avec succès !")
                return True
            else:
                if verbose:
                    print("✅ Toutes les migrations sont à jour !")
                return False
                
        except Exception as e:
            if verbose:
                print(f"❌ Erreur lors de la migration intelligente: {e}")
            raise
    
    def _get_existing_columns(self):
        """
        Récupère la liste des colonnes existantes dans la table appareils.
        
        Returns:
            list: Liste des noms de colonnes
        """
        try:
            conn = sqlite3.connect(self.migrator.db_path)
            cursor = conn.cursor()
            
            # Récupérer les informations de la table appareils
            cursor.execute("PRAGMA table_info(appareils)")
            columns_info = cursor.fetchall()
            
            # Extraire les noms des colonnes
            existing_columns = [col[1] for col in columns_info]
            
            conn.close()
            return existing_columns
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération des colonnes: {e}")
            return []
    
    def _migration_columns_exist(self, migration, existing_columns):
        """
        Vérifie si les colonnes d'une migration existent déjà.
        
        Args:
            migration (dict): Migration à vérifier
            existing_columns (list): Colonnes existantes
            
        Returns:
            bool: True si toutes les colonnes de la migration existent
        """
        migration_columns = []
        
        # Extraire les noms de colonnes des commandes SQL
        for sql_command in migration['sql']:
            if 'ADD COLUMN' in sql_command.upper():
                # Exemple: "ALTER TABLE appareils ADD COLUMN Serie TEXT"
                parts = sql_command.split()
                for i, part in enumerate(parts):
                    if part.upper() == 'COLUMN' and i + 1 < len(parts):
                        column_name = parts[i + 1]
                        migration_columns.append(column_name)
                        break
        
        # Vérifier si toutes les colonnes de la migration existent
        existing_count = 0
        for column in migration_columns:
            if column in existing_columns:
                existing_count += 1
        
        # Si au moins 50% des colonnes existent, considérer la migration comme appliquée
        if len(migration_columns) > 0:
            percentage_existing = existing_count / len(migration_columns)
            return percentage_existing >= 0.5  # Au moins 50% des colonnes existent
        
        return False

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

def smart_auto_migrate_on_startup(environment='development', verbose=True):
    """
    Fonction utilitaire pour migrer intelligemment au démarrage.
    Vérifie l'état actuel de la base et marque automatiquement les migrations
    comme appliquées si les colonnes existent déjà.
    
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
    
    return migration_manager.smart_migrate(verbose) 