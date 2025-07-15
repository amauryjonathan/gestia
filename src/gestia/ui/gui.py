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

class TreeviewSortable(ttk.Treeview):
    """Treeview avec fonctionnalité de tri par colonnes"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.sort_column = None
        self.sort_reverse = False
        
        # Bind le double-clic sur les en-têtes pour le tri
        self.bind('<Double-1>', self._on_double_click_header)
    
    def _on_double_click_header(self, event):
        """Gère le double-clic sur les en-têtes pour trier"""
        region = self.identify_region(event.x, event.y)
        if region == "heading":
            column = self.identify_column(event.x)
            column_id = self.heading(column)['text']
            self.sort_by_column(column_id)
    
    def sort_by_column(self, column_id):
        """Trie le Treeview par la colonne spécifiée"""
        # Récupérer tous les éléments
        items = [(self.set(item, column_id), item) for item in self.get_children('')]
        
        # Déterminer si on inverse le tri
        if self.sort_column == column_id:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        
        self.sort_column = column_id
        
        # Trier les éléments
        items.sort(reverse=self.sort_reverse)
        
        # Réorganiser les éléments dans le Treeview
        for index, (val, item) in enumerate(items):
            self.move(item, '', index)
        
        # Mettre à jour l'apparence de l'en-tête pour indiquer le tri
        self._update_header_appearance(column_id)
    
    def _update_header_appearance(self, column_id):
        """Met à jour l'apparence des en-têtes pour indiquer le tri"""
        # Réinitialiser tous les en-têtes
        for col in self['columns']:
            current_text = self.heading(col)['text']
            # Enlever les indicateurs de tri existants
            if current_text.endswith(' ↑') or current_text.endswith(' ↓'):
                current_text = current_text[:-2]
            self.heading(col, text=current_text)
        
        # Ajouter l'indicateur de tri à la colonne active
        current_text = self.heading(column_id)['text']
        if self.sort_reverse:
            self.heading(column_id, text=f"{current_text} ↓")
        else:
            self.heading(column_id, text=f"{current_text} ↑")

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
        columns = ('ID', 'Marque', 'Modèle', 'N° Série', 'Date Réception', 'État', 'Date Vente')
        tree = TreeviewSortable(self.content_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Ajuster la largeur de certaines colonnes
        tree.column('ID', width=100)
        tree.column('Marque', width=100)
        tree.column('Modèle', width=150)
        tree.column('N° Série', width=120)
        tree.column('Date Réception', width=100)
        tree.column('État', width=100)
        tree.column('Date Vente', width=100)
        
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
                        app.NumSerie,
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
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Variables
        marque_var = tk.StringVar()
        modele_var = tk.StringVar()
        num_serie_var = tk.StringVar()
        date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        
        # Récupérer les marques existantes
        try:
            marques_existantes = AppareilService.lister_marques(self.db)
        except Exception as e:
            marques_existantes = []
            print(f"Erreur lors du chargement des marques: {e}")
        
        # Ajouter une option pour nouvelle marque
        marques_combobox = [''] + marques_existantes + ['--- Nouvelle marque ---']
        
        # Interface
        ttk.Label(dialog, text="Marque:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        # Combobox pour les marques
        marque_combobox = ttk.Combobox(dialog, textvariable=marque_var, values=marques_combobox, width=27, state="readonly")
        marque_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Entry pour nouvelle marque (caché par défaut)
        nouvelle_marque_entry = ttk.Entry(dialog, width=30)
        nouvelle_marque_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        nouvelle_marque_entry.grid_remove()  # Caché par défaut
        
        def on_marque_change(event):
            """Gère le changement de sélection dans le combobox"""
            selection = marque_var.get()
            if selection == '--- Nouvelle marque ---':
                # Afficher l'entry pour nouvelle marque
                marque_combobox.grid_remove()
                nouvelle_marque_entry.grid()
                nouvelle_marque_entry.focus()
                marque_var.set('')  # Vider la variable
            elif selection == '':
                # Retour au combobox normal
                nouvelle_marque_entry.grid_remove()
                marque_combobox.grid()
        
        marque_combobox.bind('<<ComboboxSelected>>', on_marque_change)
        
        # Label pour expliquer
        ttk.Label(dialog, text="💡 Sélectionnez une marque existante ou 'Nouvelle marque'", 
                 font=('Arial', 8), foreground='gray').grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky=tk.W)
        
        ttk.Label(dialog, text="Modèle:", font=('Arial', 10, 'bold')).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=modele_var, width=30).grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Numéro de série:", font=('Arial', 10, 'bold')).grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=num_serie_var, width=30).grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Date de réception:", font=('Arial', 10, 'bold')).grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        ttk.Entry(dialog, textvariable=date_var, width=30).grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        
        def valider():
            try:
                # Récupérer la marque (depuis combobox ou entry)
                marque = marque_var.get()
                if marque == '--- Nouvelle marque ---' or marque == '':
                    marque = nouvelle_marque_entry.get().strip()
                
                # Validation
                if not marque:
                    messagebox.showerror("Erreur", "Veuillez saisir une marque")
                    return
                
                if not modele_var.get().strip():
                    messagebox.showerror("Erreur", "Veuillez saisir un modèle")
                    return
                
                if not num_serie_var.get().strip():
                    messagebox.showerror("Erreur", "Veuillez saisir un numéro de série")
                    return
                
                # Créer l'appareil
                date_rec = date.fromisoformat(date_var.get())
                appareil = AppareilService.creer_appareil(self.db, marque, modele_var.get().strip(), num_serie_var.get().strip(), date_rec)
                
                messagebox.showinfo("Succès", f"Appareil créé avec l'ID: {appareil.ID_Appareil}")
                self.refresh_appareils()
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Erreur", f"Date invalide. Format attendu: YYYY-MM-DD")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")
        
        # Frame pour les boutons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Créer", command=valider, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annuler", command=dialog.destroy, style='Info.TButton').pack(side=tk.LEFT, padx=5)
    
    def consulter_appareil_gui(self, event):
        """Interface pour consulter un appareil"""
        selection = self.appareils_tree.selection()
        if not selection:
            return
        
        item = self.appareils_tree.item(selection[0])
        id_appareil = item['values'][0]
        
        try:
            # Récupérer le récapitulatif complet de l'appareil
            recapitulatif = AppareilService.obtenir_recapitulatif_appareil(self.db, id_appareil)
            if not recapitulatif:
                messagebox.showerror("Erreur", "Appareil non trouvé")
                return
            
            appareil = recapitulatif['appareil']
            sessions = recapitulatif['sessions']
            diagnostics = recapitulatif['diagnostics']
            stats = recapitulatif['statistiques']
            
            # Créer une fenêtre de détails avec onglets
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Détails - {id_appareil}")
            dialog.geometry("800x600")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Créer un notebook pour les onglets
            notebook = ttk.Notebook(dialog)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Onglet 1: Informations générales
            tab_general = ttk.Frame(notebook)
            notebook.add(tab_general, text="📋 Informations Générales")
            
            # Informations de base
            info_frame = ttk.LabelFrame(tab_general, text="Informations de l'appareil", padding="10")
            info_frame.pack(fill=tk.X, padx=10, pady=10)
            
            ttk.Label(info_frame, text=f"ID: {appareil.ID_Appareil}", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Marque: {appareil.Marque}").pack(anchor=tk.W, pady=2)
            ttk.Label(info_frame, text=f"Modèle: {appareil.Modele}").pack(anchor=tk.W, pady=2)
            ttk.Label(info_frame, text=f"Numéro de série: {appareil.NumSerie}").pack(anchor=tk.W, pady=2)
            ttk.Label(info_frame, text=f"Capacité: {appareil.Capacite or 'Non spécifiée'}").pack(anchor=tk.W, pady=2)
            ttk.Label(info_frame, text=f"Technologie: {appareil.Technologie.value if appareil.Technologie else 'Non spécifiée'}").pack(anchor=tk.W, pady=2)
            ttk.Label(info_frame, text=f"Date de réception: {appareil.DateReception}").pack(anchor=tk.W, pady=2)
            ttk.Label(info_frame, text=f"État actuel: {appareil.Etat.value}", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
            if appareil.DateMiseEnVente:
                ttk.Label(info_frame, text=f"Date de mise en vente: {appareil.DateMiseEnVente}").pack(anchor=tk.W, pady=2)
            
            # Bouton pour modifier l'état
            ttk.Button(info_frame, text="Modifier l'état", 
                      command=lambda: self.modifier_etat_appareil_gui(appareil.ID_Appareil, dialog),
                      style='Info.TButton').pack(pady=10)
            
            # Onglet 2: Récapitulatif des tests et diagnostics
            tab_recap = ttk.Frame(notebook)
            notebook.add(tab_recap, text="📊 Récapitulatif Tests & Diagnostics")
            
            # Statistiques générales
            stats_frame = ttk.LabelFrame(tab_recap, text="Statistiques générales", padding="10")
            stats_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Frame pour les statistiques des sessions
            sessions_stats_frame = ttk.Frame(stats_frame)
            sessions_stats_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(sessions_stats_frame, text="🧪 Sessions de Test:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(sessions_stats_frame, text=f"  • Total: {stats['sessions']['total']}").pack(anchor=tk.W)
            ttk.Label(sessions_stats_frame, text=f"  • Réussies: {stats['sessions']['reussies']} ✅").pack(anchor=tk.W)
            ttk.Label(sessions_stats_frame, text=f"  • Échouées: {stats['sessions']['echouees']} ❌").pack(anchor=tk.W)
            ttk.Label(sessions_stats_frame, text=f"  • En cours: {stats['sessions']['en_cours']} ⏳").pack(anchor=tk.W)
            
            # Frame pour les statistiques des diagnostics
            diag_stats_frame = ttk.Frame(stats_frame)
            diag_stats_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(diag_stats_frame, text="🔧 Diagnostics et Réparations:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(diag_stats_frame, text=f"  • Total: {stats['diagnostics']['total']}").pack(anchor=tk.W)
            ttk.Label(diag_stats_frame, text=f"  • Réussis: {stats['diagnostics']['reussis']} ✅").pack(anchor=tk.W)
            ttk.Label(diag_stats_frame, text=f"  • Échoués: {stats['diagnostics']['echoues']} ❌").pack(anchor=tk.W)
            ttk.Label(diag_stats_frame, text=f"  • En cours: {stats['diagnostics']['en_cours']} ⏳").pack(anchor=tk.W)
            
            # Actions à faire
            actions_frame = ttk.LabelFrame(tab_recap, text="📋 Actions à faire", padding="10")
            actions_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Zone de texte éditable pour les actions
            actions_text = tk.Text(actions_frame, height=6, wrap=tk.WORD)
            actions_text.pack(fill=tk.X, pady=(0, 10))
            
            # Charger les actions existantes
            if appareil.ActionsAFaire:
                actions_text.insert(tk.END, appareil.ActionsAFaire)
            else:
                # Actions suggérées automatiquement
                actions_suggestions = []
                if stats['sessions']['en_cours'] > 0:
                    actions_suggestions.append(f"• {stats['sessions']['en_cours']} session(s) de test en cours - Terminer les tests")
                
                if stats['diagnostics']['en_cours'] > 0:
                    actions_suggestions.append(f"• {stats['diagnostics']['en_cours']} diagnostic(s) en cours - Finaliser les réparations")
                
                if stats['sessions']['echouees'] > 0 and stats['diagnostics']['total'] == 0:
                    actions_suggestions.append("• Sessions échouées sans diagnostic - Créer un diagnostic")
                
                if appareil.Etat == EtatAppareil.EN_TEST and stats['sessions']['reussies'] > 0:
                    actions_suggestions.append("• Tests réussis - Passer à l'état 'Reconditionné'")
                
                if appareil.Etat == EtatAppareil.EN_REPARATION and stats['diagnostics']['reussis'] > 0:
                    actions_suggestions.append("• Réparations réussies - Passer à l'état 'Reconditionné'")
                
                if appareil.Etat == EtatAppareil.RECONDITIONNE:
                    actions_suggestions.append("• Machine reconditionnée - Passer à l'état 'En Vente'")
                
                if not actions_suggestions:
                    actions_suggestions.append("• Aucune action urgente requise")
                
                actions_text.insert(tk.END, "\n".join(actions_suggestions))
            
            # Bouton pour sauvegarder les actions
            def sauvegarder_actions():
                try:
                    actions = actions_text.get("1.0", tk.END).strip()
                    if AppareilService.mettre_a_jour_actions_a_faire(self.db, appareil.ID_Appareil, actions):
                        messagebox.showinfo("Succès", "Actions à faire sauvegardées !")
                    else:
                        messagebox.showerror("Erreur", "Impossible de sauvegarder les actions")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
            
            ttk.Button(actions_frame, text="💾 Sauvegarder les actions", 
                      command=sauvegarder_actions, style='Success.TButton').pack(pady=5)
            
            # Section des problèmes identifiés
            problemes_frame = ttk.LabelFrame(tab_recap, text="🔍 Problèmes identifiés", padding="10")
            problemes_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Zone de texte éditable pour les problèmes
            problemes_text = tk.Text(problemes_frame, height=6, wrap=tk.WORD)
            problemes_text.pack(fill=tk.X, pady=(0, 10))
            
            # Charger les problèmes existants
            if appareil.SoucisMachine:
                problemes_text.insert(tk.END, appareil.SoucisMachine)
            else:
                # Problèmes suggérés automatiquement basés sur les diagnostics
                problemes_suggestions = []
                if stats['sessions']['echouees'] > 0:
                    problemes_suggestions.append("• Tests échoués - Problèmes détectés lors des tests")
                
                if stats['diagnostics']['echoues'] > 0:
                    problemes_suggestions.append("• Réparations échouées - Problèmes irréparables identifiés")
                
                if stats['diagnostics']['en_cours'] > 0:
                    problemes_suggestions.append("• Diagnostics en cours - Problèmes en cours d'analyse")
                
                if not problemes_suggestions:
                    problemes_suggestions.append("• Aucun problème majeur identifié pour le moment")
                
                problemes_text.insert(tk.END, "\n".join(problemes_suggestions))
            
            # Bouton pour sauvegarder les problèmes
            def sauvegarder_problemes():
                try:
                    problemes = problemes_text.get("1.0", tk.END).strip()
                    if AppareilService.mettre_a_jour_problemes_identifies(self.db, appareil.ID_Appareil, problemes):
                        messagebox.showinfo("Succès", "Problèmes identifiés sauvegardés !")
                    else:
                        messagebox.showerror("Erreur", "Impossible de sauvegarder les problèmes")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
            
            ttk.Button(problemes_frame, text="💾 Sauvegarder les problèmes", 
                      command=sauvegarder_problemes, style='Warning.TButton').pack(pady=5)
            
            # Onglet 3: Détail des sessions de test
            tab_sessions = ttk.Frame(notebook)
            notebook.add(tab_sessions, text="🧪 Sessions de Test")
            
            if sessions:
                # Treeview pour les sessions
                columns_sessions = ('ID', 'Date Début', 'Date Fin', 'Technicien', 'Résultat', 'Commentaires')
                tree_sessions = ttk.Treeview(tab_sessions, columns=columns_sessions, show='headings', height=8)
                
                for col in columns_sessions:
                    tree_sessions.heading(col, text=col)
                    tree_sessions.column(col, width=100)
                
                tree_sessions.column('ID', width=80)
                tree_sessions.column('Date Début', width=100)
                tree_sessions.column('Date Fin', width=100)
                tree_sessions.column('Technicien', width=120)
                tree_sessions.column('Résultat', width=100)
                tree_sessions.column('Commentaires', width=200)
                
                # Scrollbar pour les sessions
                scrollbar_sessions = ttk.Scrollbar(tab_sessions, orient=tk.VERTICAL, command=tree_sessions.yview)
                tree_sessions.configure(yscrollcommand=scrollbar_sessions.set)
                
                tree_sessions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
                scrollbar_sessions.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
                
                # Remplir les données des sessions
                for session in sessions:
                    technicien = TechnicienService.obtenir_technicien(self.db, session.ID_Technicien)
                    nom_tech = f"{technicien.Nom} {technicien.Prenom}" if technicien else "Inconnu"
                    
                    tree_sessions.insert('', tk.END, values=(
                        session.ID_Session,
                        session.DateDebut.strftime('%d/%m/%Y'),
                        session.DateFin.strftime('%d/%m/%Y') if session.DateFin else '-',
                        nom_tech,
                        session.ResultatFinal.value,
                        session.Commentaires or '-'
                    ))
            else:
                ttk.Label(tab_sessions, text="Aucune session de test trouvée pour cet appareil.", 
                         font=('Arial', 12)).pack(pady=50)
            
            # Onglet 4: Détail des diagnostics
            tab_diagnostics = ttk.Frame(notebook)
            notebook.add(tab_diagnostics, text="🔧 Diagnostics & Réparations")
            
            if diagnostics:
                # Treeview pour les diagnostics
                columns_diag = ('ID', 'Date Début', 'Date Fin', 'Technicien', 'Problème', 'Actions', 'Résultat')
                tree_diag = ttk.Treeview(tab_diagnostics, columns=columns_diag, show='headings', height=8)
                
                for col in columns_diag:
                    tree_diag.heading(col, text=col)
                    tree_diag.column(col, width=100)
                
                tree_diag.column('ID', width=80)
                tree_diag.column('Date Début', width=100)
                tree_diag.column('Date Fin', width=100)
                tree_diag.column('Technicien', width=120)
                tree_diag.column('Problème', width=150)
                tree_diag.column('Actions', width=150)
                tree_diag.column('Résultat', width=100)
                
                # Scrollbar pour les diagnostics
                scrollbar_diag = ttk.Scrollbar(tab_diagnostics, orient=tk.VERTICAL, command=tree_diag.yview)
                tree_diag.configure(yscrollcommand=scrollbar_diag.set)
                
                tree_diag.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
                scrollbar_diag.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
                
                # Remplir les données des diagnostics
                for diag in diagnostics:
                    technicien = TechnicienService.obtenir_technicien(self.db, diag.ID_Technicien)
                    nom_tech = f"{technicien.Nom} {technicien.Prenom}" if technicien else "Inconnu"
                    
                    # Tronquer le problème et les actions pour l'affichage
                    probleme = diag.DescriptionProbleme[:50] + "..." if len(diag.DescriptionProbleme) > 50 else diag.DescriptionProbleme
                    actions = diag.ActionsReparation[:50] + "..." if diag.ActionsReparation and len(diag.ActionsReparation) > 50 else (diag.ActionsReparation or '-')
                    
                    tree_diag.insert('', tk.END, values=(
                        diag.ID_DiagRep,
                        diag.DateDebut.strftime('%d/%m/%Y'),
                        diag.DateFin.strftime('%d/%m/%Y') if diag.DateFin else '-',
                        nom_tech,
                        probleme,
                        actions,
                        diag.ResultatReparation.value if diag.ResultatReparation else 'En cours'
                    ))
            else:
                ttk.Label(tab_diagnostics, text="Aucun diagnostic trouvé pour cet appareil.", 
                         font=('Arial', 12)).pack(pady=50)
                
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
        tree = TreeviewSortable(self.content_frame, columns=columns, show='headings', height=15)
        
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