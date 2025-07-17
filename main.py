#!/usr/bin/env python3
"""
Système de Gestion d'Appareils - GESTIA
=======================================

Ce programme implémente un système complet de gestion d'appareils
avec tests, diagnostics et réparations basé sur le diagramme de classe fourni.

Fonctionnalités :
- Gestion des appareils (création, consultation, modification d'état)
- Gestion des techniciens
- Sessions de test avec programmes multiples
- Critères de validation
- Diagnostics et réparations
- Statistiques et rapports

Auteur : Assistant IA
Date : 2024
"""

import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def initialize_system():
    """Hook d'initialisation du système"""
    print("🔧 Initialisation du système...")
    
    # Hook 1: Vérifications de base de données
    try:
        from gestia.core.migration_manager import auto_migrate_on_startup
        auto_migrate_on_startup(verbose=True)
    except Exception as e:
        print(f"⚠️ Erreur migrations: {e}")
    
    # Hook 2: Vérifications de configuration
    try:
        check_configuration()
    except Exception as e:
        print(f"⚠️ Erreur configuration: {e}")
    
    # Hook 3: Autres vérifications...
    # ...

def main():
    """Point d'entrée principal"""
    # 1. Initialisation (hooks)
    initialize_system()
    
    # 2. Démarrage de l'application
    start_application()

if __name__ == "__main__":
    main() 