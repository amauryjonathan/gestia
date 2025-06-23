#!/usr/bin/env python3
"""
Interface Console GESTIA
========================

Interface console interactive pour le système de gestion d'appareils.
"""

import sys
from datetime import date
from typing import Optional

from ..core.database import db_manager, init_database
from ..core.services import (
    AppareilService, TechnicienService, SessionDeTestService,
    ProgrammeDeTestService, CritereDeTestService, DiagnosticReparationService
)
from ..core.models import (
    EtatAppareil, ResultatSession, NomProgramme, StatutExecution,
    NomCritere, ResultatReparation
)

class InterfaceConsole:
    def __init__(self):
        self.db = db_manager.get_session()
    
    def afficher_menu_principal(self):
        print("\n" + "="*50)
        print("SYSTÈME DE GESTION D'APPAREILS - GESTIA")
        print("="*50)
        print("1. Gestion des Appareils")
        print("2. Gestion des Techniciens")
        print("3. Sessions de Test")
        print("4. Programmes de Test")
        print("5. Critères de Test")
        print("6. Diagnostics et Réparations")
        print("7. Rapports et Statistiques")
        print("0. Quitter")
        print("-"*50)
    
    def menu_appareils(self):
        while True:
            print("\n--- GESTION DES APPAREILS ---")
            print("1. Créer un nouvel appareil")
            print("2. Lister tous les appareils")
            print("3. Consulter un appareil")
            print("4. Modifier l'état d'un appareil")
            print("0. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.creer_appareil()
            elif choix == "2":
                self.lister_appareils()
            elif choix == "3":
                self.consulter_appareil()
            elif choix == "4":
                self.modifier_etat_appareil()
            elif choix == "0":
                break
    
    def creer_appareil(self):
        print("\n--- CRÉATION D'UN NOUVEL APPAREIL ---")
        marque = input("Marque : ")
        modele = input("Modèle : ")
        date_reception = input("Date de réception (YYYY-MM-DD) : ")
        
        try:
            date_rec = date.fromisoformat(date_reception)
            appareil = AppareilService.creer_appareil(self.db, marque, modele, date_rec)
            print(f"✅ Appareil créé avec succès ! ID: {appareil.ID_Appareil}")
        except Exception as e:
            print(f"❌ Erreur lors de la création : {e}")
    
    def lister_appareils(self):
        print("\n--- LISTE DES APPAREILS ---")
        appareils = AppareilService.lister_appareils(self.db)
        if appareils:
            for app in appareils:
                print(f"ID: {app.ID_Appareil} | {app.Marque} {app.Modele} | État: {app.Etat.value}")
        else:
            print("Aucun appareil trouvé.")
    
    def consulter_appareil(self):
        id_app = input("ID de l'appareil : ")
        appareil = AppareilService.obtenir_appareil(self.db, id_app)
        if appareil:
            print(f"\n--- DÉTAILS DE L'APPAREIL {id_app} ---")
            print(f"Marque: {appareil.Marque}")
            print(f"Modèle: {appareil.Modele}")
            print(f"Date de réception: {appareil.DateReception}")
            print(f"État: {appareil.Etat.value}")
            if appareil.DateMiseEnVente:
                print(f"Date de mise en vente: {appareil.DateMiseEnVente}")
        else:
            print("❌ Appareil non trouvé.")
    
    def modifier_etat_appareil(self):
        id_app = input("ID de l'appareil : ")
        print("Nouveaux états disponibles:")
        for i, etat in enumerate(EtatAppareil, 1):
            print(f"{i}. {etat.value}")
        
        try:
            choix = int(input("Choisissez le nouvel état : ")) - 1
            nouvel_etat = list(EtatAppareil)[choix]
            if AppareilService.modifier_etat_appareil(self.db, id_app, nouvel_etat):
                print("✅ État modifié avec succès !")
            else:
                print("❌ Appareil non trouvé.")
        except (ValueError, IndexError):
            print("❌ Choix invalide.")
    
    def menu_techniciens(self):
        while True:
            print("\n--- GESTION DES TECHNICIENS ---")
            print("1. Créer un nouveau technicien")
            print("2. Lister tous les techniciens")
            print("3. Consulter un technicien")
            print("0. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.creer_technicien()
            elif choix == "2":
                self.lister_techniciens()
            elif choix == "3":
                self.consulter_technicien()
            elif choix == "0":
                break
    
    def creer_technicien(self):
        print("\n--- CRÉATION D'UN NOUVEAU TECHNICIEN ---")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        
        try:
            technicien = TechnicienService.creer_technicien(self.db, nom, prenom)
            print(f"✅ Technicien créé avec succès ! ID: {technicien.ID_Technicien}")
        except Exception as e:
            print(f"❌ Erreur lors de la création : {e}")
    
    def lister_techniciens(self):
        print("\n--- LISTE DES TECHNICIENS ---")
        techniciens = TechnicienService.lister_techniciens(self.db)
        if techniciens:
            for tech in techniciens:
                print(f"ID: {tech.ID_Technicien} | {tech.Nom} {tech.Prenom}")
        else:
            print("Aucun technicien trouvé.")
    
    def consulter_technicien(self):
        id_tech = input("ID du technicien : ")
        technicien = TechnicienService.obtenir_technicien(self.db, id_tech)
        if technicien:
            print(f"\n--- DÉTAILS DU TECHNICIEN {id_tech} ---")
            print(f"Nom: {technicien.Nom}")
            print(f"Prénom: {technicien.Prenom}")
        else:
            print("❌ Technicien non trouvé.")
    
    def menu_sessions_test(self):
        while True:
            print("\n--- SESSIONS DE TEST ---")
            print("1. Créer une nouvelle session")
            print("2. Consulter une session")
            print("3. Terminer une session")
            print("0. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.creer_session_test()
            elif choix == "2":
                self.consulter_session_test()
            elif choix == "3":
                self.terminer_session_test()
            elif choix == "0":
                break
    
    def creer_session_test(self):
        print("\n--- CRÉATION D'UNE SESSION DE TEST ---")
        id_app = input("ID de l'appareil : ")
        id_tech = input("ID du technicien : ")
        
        try:
            session = SessionDeTestService.creer_session(self.db, id_app, id_tech)
            print(f"✅ Session créée avec succès ! ID: {session.ID_Session}")
        except Exception as e:
            print(f"❌ Erreur lors de la création : {e}")
    
    def consulter_session_test(self):
        id_session = input("ID de la session : ")
        session = SessionDeTestService.obtenir_session(self.db, id_session)
        if session:
            print(f"\n--- DÉTAILS DE LA SESSION {id_session} ---")
            print(f"Appareil: {session.ID_Appareil}")
            print(f"Technicien: {session.ID_Technicien}")
            print(f"Date début: {session.DateDebut}")
            print(f"Résultat: {session.ResultatFinal.value}")
            if session.DateFin:
                print(f"Date fin: {session.DateFin}")
            if session.Commentaires:
                print(f"Commentaires: {session.Commentaires}")
        else:
            print("❌ Session non trouvée.")
    
    def terminer_session_test(self):
        id_session = input("ID de la session : ")
        print("Résultats disponibles:")
        for i, resultat in enumerate(ResultatSession, 1):
            print(f"{i}. {resultat.value}")
        
        try:
            choix = int(input("Choisissez le résultat : ")) - 1
            resultat = list(ResultatSession)[choix]
            commentaires = input("Commentaires (optionnel) : ")
            
            if SessionDeTestService.terminer_session(self.db, id_session, resultat, commentaires):
                print("✅ Session terminée avec succès !")
            else:
                print("❌ Session non trouvée.")
        except (ValueError, IndexError):
            print("❌ Choix invalide.")
    
    def menu_programmes_test(self):
        while True:
            print("\n--- PROGRAMMES DE TEST ---")
            print("1. Créer un programme")
            print("2. Lancer un programme")
            print("3. Terminer un programme")
            print("0. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.creer_programme_test()
            elif choix == "2":
                self.lancer_programme_test()
            elif choix == "3":
                self.terminer_programme_test()
            elif choix == "0":
                break
    
    def creer_programme_test(self):
        print("\n--- CRÉATION D'UN PROGRAMME DE TEST ---")
        id_session = input("ID de la session : ")
        print("Programmes disponibles:")
        for i, prog in enumerate(NomProgramme, 1):
            print(f"{i}. {prog.value}")
        
        try:
            choix = int(input("Choisissez le programme : ")) - 1
            programme = list(NomProgramme)[choix]
            prog = ProgrammeDeTestService.creer_programme(self.db, id_session, programme)
            print(f"✅ Programme créé avec succès ! ID: {prog.ID_Programme}")
        except (ValueError, IndexError):
            print("❌ Choix invalide.")
    
    def lancer_programme_test(self):
        id_prog = input("ID du programme : ")
        if ProgrammeDeTestService.lancer_programme(self.db, id_prog):
            print("✅ Programme lancé avec succès !")
        else:
            print("❌ Programme non trouvé.")
    
    def terminer_programme_test(self):
        id_prog = input("ID du programme : ")
        succes = input("Succès ? (oui/non) : ").lower() == "oui"
        
        if ProgrammeDeTestService.terminer_programme(self.db, id_prog, succes):
            print("✅ Programme terminé avec succès !")
        else:
            print("❌ Programme non trouvé.")
    
    def menu_criteres_test(self):
        while True:
            print("\n--- CRITÈRES DE TEST ---")
            print("1. Créer un critère")
            print("2. Valider un critère")
            print("0. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.creer_critere_test()
            elif choix == "2":
                self.valider_critere_test()
            elif choix == "0":
                break
    
    def creer_critere_test(self):
        print("\n--- CRÉATION D'UN CRITÈRE DE TEST ---")
        id_prog = input("ID du programme : ")
        print("Critères disponibles:")
        for i, crit in enumerate(NomCritere, 1):
            print(f"{i}. {crit.value}")
        
        try:
            choix = int(input("Choisissez le critère : ")) - 1
            critere = list(NomCritere)[choix]
            crit = CritereDeTestService.creer_critere(self.db, id_prog, critere)
            print(f"✅ Critère créé avec succès ! ID: {crit.ID_Critere}")
        except (ValueError, IndexError):
            print("❌ Choix invalide.")
    
    def valider_critere_test(self):
        id_crit = input("ID du critère : ")
        id_tech = input("ID du technicien : ")
        commentaire = input("Commentaire défaut (optionnel) : ")
        
        if CritereDeTestService.valider_critere(self.db, id_crit, id_tech, commentaire):
            print("✅ Critère validé avec succès !")
        else:
            print("❌ Critère non trouvé.")
    
    def menu_diagnostics(self):
        while True:
            print("\n--- DIAGNOSTICS ET RÉPARATIONS ---")
            print("1. Créer un diagnostic")
            print("2. Terminer un diagnostic")
            print("0. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.creer_diagnostic()
            elif choix == "2":
                self.terminer_diagnostic()
            elif choix == "0":
                break
    
    def creer_diagnostic(self):
        print("\n--- CRÉATION D'UN DIAGNOSTIC ---")
        id_app = input("ID de l'appareil : ")
        id_tech = input("ID du technicien : ")
        description = input("Description du problème : ")
        id_session = input("ID de la session source (optionnel) : ")
        
        try:
            diagnostic = DiagnosticReparationService.creer_diagnostic(
                self.db, id_app, id_tech, description, id_session if id_session else None
            )
            print(f"✅ Diagnostic créé avec succès ! ID: {diagnostic.ID_DiagRep}")
        except Exception as e:
            print(f"❌ Erreur lors de la création : {e}")
    
    def terminer_diagnostic(self):
        id_diag = input("ID du diagnostic : ")
        actions = input("Actions de réparation : ")
        print("Résultats disponibles:")
        for i, resultat in enumerate(ResultatReparation, 1):
            print(f"{i}. {resultat.value}")
        
        try:
            choix = int(input("Choisissez le résultat : ")) - 1
            resultat = list(ResultatReparation)[choix]
            
            if DiagnosticReparationService.terminer_diagnostic(self.db, id_diag, actions, resultat):
                print("✅ Diagnostic terminé avec succès !")
            else:
                print("❌ Diagnostic non trouvé.")
        except (ValueError, IndexError):
            print("❌ Choix invalide.")
    
    def afficher_statistiques(self):
        print("\n--- STATISTIQUES ---")
        appareils = AppareilService.lister_appareils(self.db)
        techniciens = TechnicienService.lister_techniciens(self.db)
        
        print(f"Nombre total d'appareils : {len(appareils)}")
        print(f"Nombre total de techniciens : {len(techniciens)}")
        
        # Statistiques par état
        if appareils:
            etats = {}
            for app in appareils:
                etat = app.Etat.value
                etats[etat] = etats.get(etat, 0) + 1
            
            print("\nRépartition par état :")
            for etat, count in etats.items():
                print(f"  {etat} : {count}")
    
    def executer(self):
        print("🚀 Initialisation du système...")
        init_database()
        
        while True:
            self.afficher_menu_principal()
            choix = input("\nVotre choix : ")
            
            if choix == "1":
                self.menu_appareils()
            elif choix == "2":
                self.menu_techniciens()
            elif choix == "3":
                self.menu_sessions_test()
            elif choix == "4":
                self.menu_programmes_test()
            elif choix == "5":
                self.menu_criteres_test()
            elif choix == "6":
                self.menu_diagnostics()
            elif choix == "7":
                self.afficher_statistiques()
            elif choix == "0":
                print("👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide.")
        
        self.db.close()

if __name__ == "__main__":
    interface = InterfaceConsole()
    interface.executer() 