#!/usr/bin/env python3
"""
Lanceur Interface Graphique GESTIA
==================================

Script pour lancer directement l'interface graphique de GESTIA.
"""

import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Lance l'interface graphique"""
    print("🎯 GESTIA - Interface Graphique")
    print("=" * 30)
    
    try:
        # Vérifier si tkinter est disponible
        import tkinter
        print("✅ Tkinter disponible")
    except ImportError:
        print("❌ Tkinter n'est pas disponible sur ce système")
        print("Veuillez installer tkinter ou utiliser l'interface console")
        print("Lancez 'python main.py' et choisissez l'option 2")
        return
    
    try:
        # Importer et lancer l'interface graphique
        from gestia.ui.gui import main as gui_main
        print("🚀 Lancement de l'interface graphique...")
        gui_main()
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        print("Veuillez vérifier que toutes les dépendances sont installées")
        print("Essayez : pip install -r requirements.txt")

if __name__ == "__main__":
    main() 