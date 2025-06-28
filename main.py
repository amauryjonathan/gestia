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

def main():
    """Point d'entrée principal de l'application"""
    print("🎯 SYSTÈME DE GESTION D'APPAREILS - GESTIA")
    print("=" * 50)
    print("Initialisation en cours...")
    
    # Vérifier si tkinter est disponible
    try:
        import tkinter
        tkinter_available = True
    except ImportError:
        tkinter_available = False
    
    # Proposer le choix de l'interface
    if tkinter_available:
        print("\nChoisissez votre interface :")
        print("1. Interface Graphique (Tkinter)")
        print("2. Interface Console")
        print("3. Démonstration automatique")
        
        while True:
            try:
                choix = input("\nVotre choix (1-3) : ").strip()
                if choix in ['1', '2', '3']:
                    break
                else:
                    print("❌ Veuillez choisir 1, 2 ou 3")
            except KeyboardInterrupt:
                print("\n\n👋 Arrêt demandé par l'utilisateur.")
                return
        
        if choix == '1':
            # Interface graphique
            try:
                from gestia.ui.gui import main as gui_main
                gui_main()
            except Exception as e:
                print(f"\n❌ Erreur lors du lancement de l'interface graphique : {e}")
                print("Falling back to console interface...")
                choix = '2'
        
        if choix == '2':
            # Interface console
            try:
                from gestia.ui.console import InterfaceConsole
                interface = InterfaceConsole()
                interface.executer()
            except Exception as e:
                print(f"\n❌ Erreur fatale : {e}")
                print("Veuillez vérifier la configuration de la base de données.")
        
        elif choix == '3':
            # Démonstration
            try:
                # Utiliser le script de génération de données de test
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data', 'scripts'))
                from generate_test_data import generer_donnees_test
                generer_donnees_test()
                print("\n✅ Démonstration terminée !")
            except Exception as e:
                print(f"\n❌ Erreur lors de la démonstration : {e}")
    
    else:
        # Tkinter non disponible, utiliser l'interface console
        print("⚠️  Tkinter non disponible, utilisation de l'interface console")
        try:
            from gestia.ui.console import InterfaceConsole
            interface = InterfaceConsole()
            interface.executer()
        except Exception as e:
            print(f"\n❌ Erreur fatale : {e}")
            print("Veuillez vérifier la configuration de la base de données.")

if __name__ == "__main__":
    main() 