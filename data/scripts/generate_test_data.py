#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération de données de test pour GESTIA
===================================================

Ce script crée des données virtuelles pour l'environnement de développement.
"""

import sys
import os
from datetime import date, timedelta
import random

# Configuration de l'encodage pour Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from gestia.core.database import init_database, db_manager
from gestia.core.services import (
    AppareilService, TechnicienService, SessionDeTestService,
    ProgrammeDeTestService, CritereDeTestService, DiagnosticReparationService
)
from gestia.core.models import (
    EtatAppareil, ResultatSession, NomProgramme, StatutExecution,
    NomCritere, ResultatReparation
)

def generer_donnees_test():
    """Génère des données de test complètes"""
    print("[GENERATION] Génération de données de test...")
    
    # Initialiser la base de données
    init_database()
    db = db_manager.get_session()
    
    try:
        # 1. Créer des techniciens
        print("[TECHNICIENS] Création des techniciens...")
        techniciens = []
        noms_techniciens = [
            ("Dupont", "Jean"),
            ("Martin", "Marie"),
            ("Bernard", "Pierre"),
            ("Petit", "Sophie"),
            ("Robert", "Michel"),
            ("Richard", "Nathalie"),
            ("Durand", "François"),
            ("Moreau", "Isabelle")
        ]
        
        for nom, prenom in noms_techniciens:
            technicien = TechnicienService.creer_technicien(db, nom, prenom)
            techniciens.append(technicien)
            print(f"  [OK] {prenom} {nom} créé (ID: {technicien.ID_Technicien})")
        
        # 2. Créer des appareils
        print("\n[APPAREILS] Création des appareils...")
        appareils = []
        marques_modeles = [
            ("Samsung", "WW90T534DAW"),
            ("LG", "F4WV510S0E"),
            ("Bosch", "WAT28441FF"),
            ("Whirlpool", "FSCR12440"),
            ("Electrolux", "EW6F1408CI"),
            ("Beko", "WTV8734XW"),
            ("Candy", "CSO1410D3"),
            ("Hotpoint", "AQUALTIS C 1040 D"),
            ("Indesit", "IWSC 61251"),
            ("Zanussi", "ZWF01486SI")
        ]
        
        # Ajouter des variantes
        for marque, modele in marques_modeles:
            # Créer plusieurs appareils de chaque modèle
            for i in range(random.randint(2, 5)):
                # Créer une variante de modèle
                modele_variant = f"{modele}-{chr(65+i)}" if i > 0 else modele
                
                # Date de réception aléatoire (derniers 30 jours)
                jours_aleatoires = random.randint(1, 30)
                date_reception = date.today() - timedelta(days=jours_aleatoires)
                
                # Numéro de série unique
                num_serie = f"SN{random.randint(100000000, 999999999)}"
                
                # État aléatoire
                etats = list(EtatAppareil)
                etat = random.choice(etats)
                
                appareil = AppareilService.creer_appareil(db, marque, modele_variant, num_serie, date_reception)
                
                # Modifier l'état si nécessaire
                if etat != EtatAppareil.EN_TEST:
                    AppareilService.modifier_etat_appareil(db, appareil.ID_Appareil, etat)
                
                appareils.append(appareil)
                print(f"  [OK] {marque} {modele_variant} créé (ID: {appareil.ID_Appareil}, S/N: {num_serie}, État: {etat.value})")
        
        # 3. Créer des sessions de test
        print("\n[SESSIONS] Création des sessions de test...")
        sessions = []
        for _ in range(min(20, len(appareils))):
            appareil = random.choice(appareils)
            technicien = random.choice(techniciens)
            
            session = SessionDeTestService.creer_session(db, appareil.ID_Appareil, technicien.ID_Technicien)
            sessions.append(session)
            print(f"  [OK] Session créée (ID: {session.ID_Session})")
        
        # 4. Créer des programmes de test pour certaines sessions
        print("\n[PROGRAMMES] Création des programmes de test...")
        for session in random.sample(sessions, min(10, len(sessions))):
            # Créer 1 à 3 programmes par session
            nb_programmes = random.randint(1, 3)
            programmes_disponibles = list(NomProgramme)
            
            for _ in range(nb_programmes):
                nom_programme = random.choice(programmes_disponibles)
                programmes_disponibles.remove(nom_programme)  # Éviter les doublons
                
                programme = ProgrammeDeTestService.creer_programme(db, session.ID_Session, nom_programme)
                
                # Simuler l'exécution de certains programmes
                if random.choice([True, False]):
                    ProgrammeDeTestService.lancer_programme(db, programme.ID_Programme)
                    
                    # Simuler la fin d'exécution
                    if random.choice([True, False]):
                        succes = random.choice([True, False])
                        ProgrammeDeTestService.terminer_programme(db, programme.ID_Programme, succes)
                        print(f"  [OK] Programme {nom_programme.value} {'réussi' if succes else 'échoué'}")
                    else:
                        print(f"  [EN COURS] Programme {nom_programme.value} en cours")
                else:
                    print(f"  [NON LANCE] Programme {nom_programme.value} non lancé")
        
        # 5. Créer quelques diagnostics
        print("\n[DIAGNOSTICS] Création des diagnostics...")
        for _ in range(min(5, len(appareils))):
            appareil = random.choice(appareils)
            technicien = random.choice(techniciens)
            
            descriptions = [
                "Vérification générale de l'appareil",
                "Problème de vidange détecté",
                "Anomalie dans le cycle d'essorage",
                "Défaut d'étanchéité de la porte",
                "Problème de chauffage",
                "Bruit anormal lors de la rotation"
            ]
            
            description = random.choice(descriptions)
            diagnostic = DiagnosticReparationService.creer_diagnostic(
                db, appareil.ID_Appareil, technicien.ID_Technicien, description
            )
            
            # Terminer certains diagnostics
            if random.choice([True, False]):
                actions = [
                    "Nettoyage et lubrification effectués",
                    "Remplacement du joint d'étanchéité",
                    "Réparation du système de vidange",
                    "Ajustement de la courroie",
                    "Remplacement du thermostat"
                ]
                action = random.choice(actions)
                resultat = random.choice([ResultatReparation.REUSSI, ResultatReparation.ECHOUÉ_IRREPARABLE])
                
                DiagnosticReparationService.terminer_diagnostic(db, diagnostic.ID_DiagRep, action, resultat)
                print(f"  [OK] Diagnostic terminé : {resultat.value}")
            else:
                print(f"  [EN COURS] Diagnostic en cours : {description}")
        
        print(f"\n[FIN] Génération terminée !")
        print(f"[STATS] Statistiques :")
        print(f"  - {len(techniciens)} techniciens créés")
        print(f"  - {len(appareils)} appareils créés")
        print(f"  - {len(sessions)} sessions de test créées")
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la génération : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Définir l'environnement de développement
    os.environ['GESTIA_ENV'] = 'development'
    generer_donnees_test() 