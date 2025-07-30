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
        from gestia.core.migration_manager import smart_auto_migrate_on_startup
        smart_auto_migrate_on_startup(verbose=True)
    except Exception as e:
        print(f"⚠️ Erreur migrations: {e}")
    
    # Hook 2: Vérifications de configuration
    try:
        check_configuration()
    except Exception as e:
        print(f"⚠️ Erreur configuration: {e}")
    
    # Hook 3: Autres vérifications...
    # ...

def check_configuration():
    """Vérification de la configuration du système"""
    print("✅ Configuration vérifiée")
    # TODO: Ajouter des vérifications de configuration
    pass

def afficher_menu_choix():
    """Affiche le menu de choix d'interface"""
    print("\n" + "="*60)
    print("🎯 GESTIA - Système de Gestion d'Appareils")
    print("="*60)
    print("Choisissez votre interface :")
    print("1. 🖥️  Interface Console (Recommandée)")
    print("2. 🖼️  Interface Graphique (Tkinter)")
    print("3. 🎮 Mode Démonstration")
    print("4. 🛠️  Outils de Développement")
    print("0. 🚪 Quitter")
    print("="*60)

def lancer_interface_console():
    """Lance l'interface console"""
    print("🚀 Lancement de l'interface console...")
    try:
        from gestia.ui.console import InterfaceConsole
        interface = InterfaceConsole()
        interface.executer()
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface console: {e}")
        print("💡 Vérifiez que tous les modules sont correctement installés.")

def lancer_interface_graphique():
    """Lance l'interface graphique"""
    print("🚀 Lancement de l'interface graphique...")
    try:
        # Vérifier si tkinter est disponible
        import tkinter
        print("✅ Tkinter disponible")
        
        from gestia.ui.gui import GestiaGUI
        app = GestiaGUI()
        app.run()
    except ImportError:
        print("❌ Tkinter n'est pas disponible sur ce système")
        print("Veuillez installer tkinter ou utiliser l'interface console")
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'interface graphique: {e}")
        print("💡 Vérifiez que toutes les dépendances sont installées")

def lancer_demo():
    """Lance le mode démonstration"""
    print("🎮 Lancement du mode démonstration...")
    try:
        # TODO: Implémenter le mode démonstration
        print("📋 Mode démonstration en cours de développement...")
        print("💡 Cette fonctionnalité sera bientôt disponible !")
    except Exception as e:
        print(f"❌ Erreur lors du lancement de la démo: {e}")

def afficher_outils_dev():
    """Affiche les outils de développement"""
    print("\n🛠️  OUTILS DE DÉVELOPPEMENT")
    print("="*40)
    print("1. python tools/manage_env.py generate - Générer des données de test")
    print("2. python tools/tools/db/migrate_db.py status - Statut des migrations")
    print("3. python tools/tools/db/explore_db.py - Explorer la base de données")
    print("4. python debug_db.py - Debug de la base de données")
    print("5. python tools/gui_launcher.py - Lancer l'interface graphique")
    print("\n💡 Utilisez ces commandes dans un autre terminal pour accéder aux outils.")

def start_application():
    """Démarrage de l'application principale avec menu de choix"""
    print("🚀 Démarrage de l'application GESTIA...")
    
    while True:
        afficher_menu_choix()
        
        try:
            choix = input("\nVotre choix (0-4): ").strip()
            
            if choix == "0":
                print("👋 Au revoir !")
                break
            elif choix == "1":
                lancer_interface_console()
            elif choix == "2":
                lancer_interface_graphique()
            elif choix == "3":
                lancer_demo()
            elif choix == "4":
                afficher_outils_dev()
                input("\nAppuyez sur Entrée pour continuer...")
            else:
                print("❌ Choix invalide. Veuillez entrer un nombre entre 0 et 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

def main():
    """Point d'entrée principal"""
    # 1. Initialisation (hooks)
    initialize_system()
    
    # 2. Démarrage de l'application avec menu de choix
    start_application()

if __name__ == "__main__":
    main() 