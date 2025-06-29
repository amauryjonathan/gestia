#!/usr/bin/env python3
"""
Démonstration de la fonctionnalité de tri
=========================================

Interface graphique simple pour démontrer le tri des colonnes.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.ui.gui import TreeviewSortable
from gestia.core.database import init_database, db_manager, set_environment
from gestia.core.services import AppareilService

class DemoTri:
    """Démonstration de la fonctionnalité de tri"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Démonstration - Tri des colonnes")
        self.root.geometry("800x600")
        
        # Initialiser la base de données
        set_environment('development')
        init_database()
        self.db = db_manager.get_session()
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title = ttk.Label(self.root, text="🧪 Démonstration - Tri des colonnes", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # Instructions
        instructions = ttk.Label(self.root, 
                               text="Double-cliquez sur les en-têtes de colonnes pour trier\n" +
                                    "Les flèches ↑/↓ indiquent l'ordre de tri",
                               font=('Arial', 10), foreground='blue')
        instructions.pack(pady=10)
        
        # Frame pour le Treeview
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview avec tri
        columns = ('ID', 'Marque', 'Modèle', 'Date Réception', 'État', 'Date Vente')
        self.tree = TreeviewSortable(frame, columns=columns, show='headings', height=20)
        
        # Configuration des colonnes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton de rafraîchissement
        ttk.Button(self.root, text="🔄 Rafraîchir les données", 
                  command=self.load_data).pack(pady=10)
        
        # Bouton de fermeture
        ttk.Button(self.root, text="❌ Fermer", 
                  command=self.root.destroy).pack(pady=10)
    
    def load_data(self):
        """Charge les données dans le Treeview"""
        # Effacer les données existantes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Charger les appareils
            appareils = AppareilService.lister_appareils(self.db)
            
            for app in appareils:
                self.tree.insert('', tk.END, values=(
                    app.ID_Appareil,
                    app.Marque,
                    app.Modele,
                    app.DateReception.strftime('%d/%m/%Y'),
                    app.Etat.value,
                    app.DateMiseEnVente.strftime('%d/%m/%Y') if app.DateMiseEnVente else '-'
                ))
            
            # Afficher le nombre d'éléments
            count_label = ttk.Label(self.root, 
                                  text=f"📊 {len(appareils)} appareils chargés",
                                  font=('Arial', 10, 'bold'))
            count_label.pack(pady=5)
            
        except Exception as e:
            error_label = ttk.Label(self.root, 
                                  text=f"❌ Erreur: {e}",
                                  font=('Arial', 10), foreground='red')
            error_label.pack(pady=5)
    
    def run(self):
        """Lance la démonstration"""
        self.root.mainloop()
        self.db.close()

def main():
    """Fonction principale"""
    print("🚀 Lancement de la démonstration de tri...")
    print("💡 Double-cliquez sur les en-têtes pour trier les colonnes")
    
    demo = DemoTri()
    demo.run()

if __name__ == "__main__":
    main() 