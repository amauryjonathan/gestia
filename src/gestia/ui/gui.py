#!/usr/bin/env python3
"""
Interface Graphique GESTIA
==========================

Interface graphique moderne pour le système de gestion d'appareils
utilisant Tkinter avec un design moderne et intuitif.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date
from ..core.database import db_manager, init_database
from ..core.services import (
    AppareilService, TechnicienService, SessionDeTestService,
    ProgrammeDeTestService, CritereDeTestService, DiagnosticReparationService
)
from ..core.models import (
    EtatAppareil, ResultatSession, NomProgramme, StatutExecution,
    NomCritere, ResultatReparation
)
import threading

class GestiaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GESTIA - Système de Gestion d'Appareils")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration du style
        self.setup_styles()
        
        # Initialisation de la base de données
        self.db = db_manager.get_session()
        init_database()
        
        # Variables
        self.current_frame = None
        
        # Création de l'interface
        self.create_widgets()
        
    def setup_styles(self):
        """Configure les styles de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des couleurs
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TButton', background='#27ae60', foreground='white')
        style.configure('Warning.TButton', background='#e74c3c', foreground='white')
        style.configure('Info.TButton', background='#3498db', foreground='white')
        
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Titre principal
        title_label = ttk.Label(main_frame, text="🎯 GESTIA - Système de Gestion d'Appareils", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame de navigation (gauche)
        nav_frame = ttk.Frame(main_frame, relief='raised', borderwidth=2)
        nav_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        nav_frame.columnconfigure(0, weight=1)
        
        # Boutons de navigation
        nav_buttons = [
            ("🏠 Tableau de Bord", self.show_dashboard),
            ("📱 Gestion des Appareils", self.show_appareils),
            ("👨‍🔧 Gestion des Techniciens", self.show_techniciens),
            ("🧪 Sessions de Test", self.show_sessions),
            ("⚙️ Programmes de Test", self.show_programmes),
            ("✅ Critères de Test", self.show_criteres),
            ("🔧 Diagnostics", self.show_diagnostics),
            ("📊 Statistiques", self.show_statistiques),
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = ttk.Button(nav_frame, text=text, command=command, 
                           style='Info.TButton', width=25)
            btn.grid(row=i, column=0, pady=5, padx=10, sticky=(tk.W, tk.E))
        
        # Frame de contenu (droite)
        self.content_frame = ttk.Frame(main_frame, relief='sunken', borderwidth=2)
        self.content_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        
        # Afficher le tableau de bord par défaut
        self.show_dashboard()
        
    def clear_content(self):
        """Efface le contenu actuel"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Affiche le tableau de bord"""
        self.clear_content()
        
        # Titre
        title = ttk.Label(self.content_frame, text="📊 Tableau de Bord", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Frame pour les statistiques
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        # Récupération des statistiques
        try:
            appareils = AppareilService.lister_appareils(self.db)
            techniciens = TechnicienService.lister_techniciens(self.db)
            
            # Statistiques des appareils
            stats_app = ttk.LabelFrame(stats_frame, text="📱 Appareils", padding="10")
            stats_app.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            ttk.Label(stats_app, text=f"Total: {len(appareils)}", font=('Arial', 14, 'bold')).pack()
            
            if appareils:
                etats = {}
                for app in appareils:
                    etat = app.Etat.value
                    etats[etat] = etats.get(etat, 0) + 1
                
                for etat, count in etats.items():
                    ttk.Label(stats_app, text=f"{etat}: {count}").pack()
            
            # Statistiques des techniciens
            stats_tech = ttk.LabelFrame(stats_frame, text="👨‍🔧 Techniciens", padding="10")
            stats_tech.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            ttk.Label(stats_tech, text=f"Total: {len(techniciens)}", font=('Arial', 14, 'bold')).pack()
            
            if techniciens:
                for tech in techniciens[:5]:  # Afficher les 5 premiers
                    ttk.Label(stats_tech, text=f"{tech.Nom} {tech.Prenom}").pack()
                if len(techniciens) > 5:
                    ttk.Label(stats_tech, text=f"... et {len(techniciens) - 5} autres").pack()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des statistiques: {e}")
    
    def show_appareils(self):
        """Affiche la gestion des appareils"""
        self.clear_content()
        
        # Titre
        title = ttk.Label(self.content_frame, text="📱 Gestion des Appareils", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Frame pour les boutons d'action
        action_frame = ttk.Frame(self.content_frame)
        action_frame.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        
        ttk.Button(action_frame, text="➕ Nouvel Appareil", 
                  command=self.creer_appareil_gui, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🔄 Actualiser", 
                  command=self.refresh_appareils, style='Info.TButton').pack(side=tk.LEFT, padx=5)
        
        # Treeview pour la liste des appareils
        columns = ('ID', 'Marque', 'Modèle', 'Date Réception', 'État', 'Date Vente')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
        
        # Stocker la référence pour l'actualisation
        self.appareils_tree = tree
        
        # Charger les données
        self.refresh_appareils()
        
        # Double-clic pour consulter
        tree.bind('<Double-1>', self.consulter_appareil_gui)
    
    def refresh_appareils(self):
        """Actualise la liste des appareils"""
        if hasattr(self, 'appareils_tree'):
            # Effacer les données existantes
            for item in self.appareils_tree.get_children():
                self.appareils_tree.delete(item)
            
            # Charger les nouvelles données
            try:
                appareils = AppareilService.lister_appareils(self.db)
                for app in appareils:
                    self.appareils_tree.insert('', tk.END, values=(
                        app.ID_Appareil,
                        app.Marque,
                        app.Modele,
                        app.DateReception.strftime('%d/%m/%Y'),
                        app.Etat.value,
                        app.DateMiseEnVente.strftime('%d/%m/%Y') if app.DateMiseEnVente else '-'
                    ))
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
    
    def creer_appareil_gui(self):
        """Interface pour créer un nouvel appareil"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouvel Appareil")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Variables
        marque_var = tk.StringVar()
        modele_var = tk.StringVar()
        date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        
        # Interface
        ttk.Label(dialog, text="Marque:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=marque_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Modèle:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=modele_var, width=30).grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Date de réception:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=date_var, width=30).grid(row=2, column=1, padx=10, pady=10)
        
        def valider():
            try:
                date_rec = date.fromisoformat(date_var.get())
                appareil = AppareilService.creer_appareil(self.db, marque_var.get(), modele_var.get(), date_rec)
                messagebox.showinfo("Succès", f"Appareil créé avec l'ID: {appareil.ID_Appareil}")
                self.refresh_appareils()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")
        
        ttk.Button(dialog, text="Créer", command=valider, style='Success.TButton').grid(row=3, column=0, columnspan=2, pady=20)
    
    def consulter_appareil_gui(self, event):
        """Interface pour consulter un appareil"""
        selection = self.appareils_tree.selection()
        if not selection:
            return
        
        item = self.appareils_tree.item(selection[0])
        id_appareil = item['values'][0]
        
        try:
            appareil = AppareilService.obtenir_appareil(self.db, id_appareil)
            if appareil:
                # Créer une fenêtre de détails
                dialog = tk.Toplevel(self.root)
                dialog.title(f"Détails - {id_appareil}")
                dialog.geometry("500x400")
                dialog.transient(self.root)
                dialog.grab_set()
                
                # Afficher les détails
                details_frame = ttk.Frame(dialog, padding="20")
                details_frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(details_frame, text=f"ID: {appareil.ID_Appareil}", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
                ttk.Label(details_frame, text=f"Marque: {appareil.Marque}").pack(anchor=tk.W, pady=5)
                ttk.Label(details_frame, text=f"Modèle: {appareil.Modele}").pack(anchor=tk.W, pady=5)
                ttk.Label(details_frame, text=f"Date de réception: {appareil.DateReception}").pack(anchor=tk.W, pady=5)
                ttk.Label(details_frame, text=f"État: {appareil.Etat.value}").pack(anchor=tk.W, pady=5)
                if appareil.DateMiseEnVente:
                    ttk.Label(details_frame, text=f"Date de mise en vente: {appareil.DateMiseEnVente}").pack(anchor=tk.W, pady=5)
                
                # Bouton pour modifier l'état
                ttk.Button(details_frame, text="Modifier l'état", 
                          command=lambda: self.modifier_etat_appareil_gui(appareil.ID_Appareil, dialog),
                          style='Info.TButton').pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la consultation: {e}")
    
    def modifier_etat_appareil_gui(self, id_appareil, parent_dialog):
        """Interface pour modifier l'état d'un appareil"""
        dialog = tk.Toplevel(parent_dialog)
        dialog.title("Modifier l'état")
        dialog.geometry("300x250")
        dialog.transient(parent_dialog)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nouvel état:").pack(pady=20)
        
        # Variable pour l'état sélectionné
        etat_var = tk.StringVar()
        
        # Liste des états
        for etat in EtatAppareil:
            ttk.Radiobutton(dialog, text=etat.value, variable=etat_var, value=etat.value).pack(anchor=tk.W, padx=20)
        
        def valider():
            try:
                nouvel_etat = next(etat for etat in EtatAppareil if etat.value == etat_var.get())
                if AppareilService.modifier_etat_appareil(self.db, id_appareil, nouvel_etat):
                    messagebox.showinfo("Succès", "État modifié avec succès!")
                    self.refresh_appareils()
                    dialog.destroy()
                    parent_dialog.destroy()
                else:
                    messagebox.showerror("Erreur", "Appareil non trouvé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")
        
        ttk.Button(dialog, text="Modifier", command=valider, style='Success.TButton').pack(pady=20)
    
    def show_techniciens(self):
        """Affiche la gestion des techniciens"""
        self.clear_content()
        
        # Titre
        title = ttk.Label(self.content_frame, text="👨‍🔧 Gestion des Techniciens", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Frame pour les boutons d'action
        action_frame = ttk.Frame(self.content_frame)
        action_frame.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        
        ttk.Button(action_frame, text="➕ Nouveau Technicien", 
                  command=self.creer_technicien_gui, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🔄 Actualiser", 
                  command=self.refresh_techniciens, style='Info.TButton').pack(side=tk.LEFT, padx=5)
        
        # Treeview pour la liste des techniciens
        columns = ('ID', 'Nom', 'Prénom')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
        
        # Stocker la référence
        self.techniciens_tree = tree
        
        # Charger les données
        self.refresh_techniciens()
    
    def refresh_techniciens(self):
        """Actualise la liste des techniciens"""
        if hasattr(self, 'techniciens_tree'):
            for item in self.techniciens_tree.get_children():
                self.techniciens_tree.delete(item)
            
            try:
                techniciens = TechnicienService.lister_techniciens(self.db)
                for tech in techniciens:
                    self.techniciens_tree.insert('', tk.END, values=(
                        tech.ID_Technicien,
                        tech.Nom,
                        tech.Prenom
                    ))
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
    
    def creer_technicien_gui(self):
        """Interface pour créer un nouveau technicien"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouveau Technicien")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Variables
        nom_var = tk.StringVar()
        prenom_var = tk.StringVar()
        
        # Interface
        ttk.Label(dialog, text="Nom:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=nom_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Prénom:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=prenom_var, width=30).grid(row=1, column=1, padx=10, pady=10)
        
        def valider():
            try:
                technicien = TechnicienService.creer_technicien(self.db, nom_var.get(), prenom_var.get())
                messagebox.showinfo("Succès", f"Technicien créé avec l'ID: {technicien.ID_Technicien}")
                self.refresh_techniciens()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")
        
        ttk.Button(dialog, text="Créer", command=valider, style='Success.TButton').grid(row=2, column=0, columnspan=2, pady=20)
    
    def show_sessions(self):
        """Affiche la gestion des sessions de test"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="🧪 Sessions de Test", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Placeholder pour l'interface des sessions
        ttk.Label(self.content_frame, text="Interface des sessions en cours de développement...").grid(row=1, column=0, pady=50)
    
    def show_programmes(self):
        """Affiche la gestion des programmes de test"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="⚙️ Programmes de Test", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Placeholder pour l'interface des programmes
        ttk.Label(self.content_frame, text="Interface des programmes en cours de développement...").grid(row=1, column=0, pady=50)
    
    def show_criteres(self):
        """Affiche la gestion des critères de test"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="✅ Critères de Test", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Placeholder pour l'interface des critères
        ttk.Label(self.content_frame, text="Interface des critères en cours de développement...").grid(row=1, column=0, pady=50)
    
    def show_diagnostics(self):
        """Affiche la gestion des diagnostics"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="🔧 Diagnostics et Réparations", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Placeholder pour l'interface des diagnostics
        ttk.Label(self.content_frame, text="Interface des diagnostics en cours de développement...").grid(row=1, column=0, pady=50)
    
    def show_statistiques(self):
        """Affiche les statistiques détaillées"""
        self.clear_content()
        
        title = ttk.Label(self.content_frame, text="📊 Statistiques Détaillées", style='Header.TLabel')
        title.grid(row=0, column=0, pady=(20, 20), sticky=tk.W)
        
        # Placeholder pour les statistiques détaillées
        ttk.Label(self.content_frame, text="Statistiques détaillées en cours de développement...").grid(row=1, column=0, pady=50)
    
    def run(self):
        """Lance l'application"""
        try:
            self.root.mainloop()
        finally:
            if hasattr(self, 'db'):
                self.db.close()

def main():
    """Point d'entrée principal"""
    app = GestiaGUI()
    app.run()

if __name__ == "__main__":
    main() 