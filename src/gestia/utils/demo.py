#!/usr/bin/env python3
"""
Démonstration GESTIA
====================

Script de démonstration pour créer des données d'exemple
et afficher les statistiques du système.
"""

from datetime import date, datetime, timedelta
import random

from ..core.database import db_manager, init_database
from ..core.services import (
    AppareilService, TechnicienService, SessionDeTestService,
    ProgrammeDeTestService, CritereDeTestService, DiagnosticReparationService
)
from ..core.models import (
    EtatAppareil, ResultatSession, NomProgramme, StatutExecution,
    NomCritere, ResultatReparation
)

def creer_donnees_exemple():
    """Crée des données d'exemple pour tester le système"""
    db = db_manager.get_session()
    
    print("🎯 Création des données d'exemple...")
    
    try:
        # 1. Créer des techniciens
        print("\n1. Création des techniciens...")
        tech1 = TechnicienService.creer_technicien(db, "Dupont", "Jean")
        tech2 = TechnicienService.creer_technicien(db, "Martin", "Marie")
        tech3 = TechnicienService.creer_technicien(db, "Bernard", "Pierre")
        print(f"✅ Techniciens créés : {tech1.ID_Technicien}, {tech2.ID_Technicien}, {tech3.ID_Technicien}")
        
        # 2. Créer des appareils
        print("\n2. Création des appareils...")
        app1 = AppareilService.creer_appareil(db, "Samsung", "WW90T534DAW", date(2024, 1, 15))
        app2 = AppareilService.creer_appareil(db, "LG", "F4WV510S0E", date(2024, 1, 20))
        app3 = AppareilService.creer_appareil(db, "Bosch", "WAT28441FF", date(2024, 1, 25))
        print(f"✅ Appareils créés : {app1.ID_Appareil}, {app2.ID_Appareil}, {app3.ID_Appareil}")
        
        # 3. Créer des sessions de test
        print("\n3. Création des sessions de test...")
        session1 = SessionDeTestService.creer_session(db, app1.ID_Appareil, tech1.ID_Technicien)
        session2 = SessionDeTestService.creer_session(db, app2.ID_Appareil, tech2.ID_Technicien)
        session3 = SessionDeTestService.creer_session(db, app3.ID_Appareil, tech3.ID_Technicien)
        print(f"✅ Sessions créées : {session1.ID_Session}, {session2.ID_Session}, {session3.ID_Session}")
        
        # 4. Créer des programmes de test
        print("\n4. Création des programmes de test...")
        prog1_1 = ProgrammeDeTestService.creer_programme(db, session1.ID_Session, NomProgramme.RAPIDE)
        prog1_2 = ProgrammeDeTestService.creer_programme(db, session1.ID_Session, NomProgramme.COTON_90)
        prog2_1 = ProgrammeDeTestService.creer_programme(db, session2.ID_Session, NomProgramme.ESSORAGE)
        prog3_1 = ProgrammeDeTestService.creer_programme(db, session3.ID_Session, NomProgramme.RAPIDE)
        print(f"✅ Programmes créés : {prog1_1.ID_Programme}, {prog1_2.ID_Programme}, {prog2_1.ID_Programme}, {prog3_1.ID_Programme}")
        
        # 5. Créer des critères de test
        print("\n5. Création des critères de test...")
        crit1 = CritereDeTestService.creer_critere(db, prog1_1.ID_Programme, NomCritere.VERROUILLAGE_PORTE)
        crit2 = CritereDeTestService.creer_critere(db, prog1_1.ID_Programme, NomCritere.VIDANGE)
        crit3 = CritereDeTestService.creer_critere(db, prog1_2.ID_Programme, NomCritere.REMPLISSAGE)
        crit4 = CritereDeTestService.creer_critere(db, prog1_2.ID_Programme, NomCritere.ROTATION)
        crit5 = CritereDeTestService.creer_critere(db, prog2_1.ID_Programme, NomCritere.ESSORAGE)
        print(f"✅ Critères créés : {crit1.ID_Critere}, {crit2.ID_Critere}, {crit3.ID_Critere}, {crit4.ID_Critere}, {crit5.ID_Critere}")
        
        # 6. Valider certains critères
        print("\n6. Validation des critères...")
        CritereDeTestService.valider_critere(db, crit1.ID_Critere, tech1.ID_Technicien, "Verrouillage OK")
        CritereDeTestService.valider_critere(db, crit2.ID_Critere, tech1.ID_Technicien, "Vidange OK")
        CritereDeTestService.valider_critere(db, crit3.ID_Critere, tech1.ID_Technicien, "Remplissage OK")
        print("✅ Critères validés")
        
        # 7. Lancer et terminer des programmes
        print("\n7. Lancement et finalisation des programmes...")
        ProgrammeDeTestService.lancer_programme(db, prog1_1.ID_Programme)
        ProgrammeDeTestService.terminer_programme(db, prog1_1.ID_Programme, True)
        ProgrammeDeTestService.lancer_programme(db, prog1_2.ID_Programme)
        ProgrammeDeTestService.terminer_programme(db, prog1_2.ID_Programme, False)
        print("✅ Programmes exécutés")
        
        # 8. Terminer des sessions
        print("\n8. Finalisation des sessions...")
        SessionDeTestService.terminer_session(db, session1.ID_Session, ResultatSession.PASSE, "Tests réussis")
        SessionDeTestService.terminer_session(db, session2.ID_Session, ResultatSession.ECHOUÉ, "Problème d'essorage")
        print("✅ Sessions terminées")
        
        # 9. Créer des diagnostics
        print("\n9. Création des diagnostics...")
        diag1 = DiagnosticReparationService.creer_diagnostic(
            db, app2.ID_Appareil, tech2.ID_Technicien, 
            "Problème d'essorage - moteur défaillant", session2.ID_Session
        )
        diag2 = DiagnosticReparationService.creer_diagnostic(
            db, app3.ID_Appareil, tech3.ID_Technicien, 
            "Vérification générale", None
        )
        print(f"✅ Diagnostics créés : {diag1.ID_DiagRep}, {diag2.ID_DiagRep}")
        
        # 10. Terminer des diagnostics
        print("\n10. Finalisation des diagnostics...")
        DiagnosticReparationService.terminer_diagnostic(
            db, diag1.ID_DiagRep, "Remplacement du moteur d'essorage", ResultatReparation.REUSSI
        )
        DiagnosticReparationService.terminer_diagnostic(
            db, diag2.ID_DiagRep, "Aucune action nécessaire", ResultatReparation.REUSSI
        )
        print("✅ Diagnostics terminés")
        
        # 11. Modifier les états des appareils
        print("\n11. Modification des états des appareils...")
        AppareilService.modifier_etat_appareil(db, app1.ID_Appareil, EtatAppareil.EN_VENTE)
        AppareilService.modifier_etat_appareil(db, app2.ID_Appareil, EtatAppareil.RECONDITIONNE)
        AppareilService.modifier_etat_appareil(db, app3.ID_Appareil, EtatAppareil.EN_TEST)
        print("✅ États modifiés")
        
        print("\n🎉 Données d'exemple créées avec succès !")
        print("\n📊 Récapitulatif :")
        print(f"   - {len(db.query(Technicien).all())} techniciens")
        print(f"   - {len(db.query(Appareil).all())} appareils")
        print(f"   - {len(db.query(SessionDeTest).all())} sessions de test")
        print(f"   - {len(db.query(ProgrammeDeTest).all())} programmes de test")
        print(f"   - {len(db.query(CritereDeTest).all())} critères de test")
        print(f"   - {len(db.query(DiagnosticReparation).all())} diagnostics")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données : {e}")
        db.rollback()
    finally:
        db.close()

def afficher_statistiques():
    """Affiche les statistiques de la base de données"""
    db = db_manager.get_session()
    
    try:
        print("\n📈 STATISTIQUES DE LA BASE DE DONNÉES")
        print("=" * 40)
        
        # Compter les appareils par état
        appareils = AppareilService.lister_appareils(db)
        etats = {}
        for app in appareils:
            etat = app.Etat.value
            etats[etat] = etats.get(etat, 0) + 1
        
        print(f"\nAppareils ({len(appareils)} total) :")
        for etat, count in etats.items():
            print(f"  {etat} : {count}")
        
        # Compter les sessions par résultat
        sessions = db.query(SessionDeTest).all()
        resultats = {}
        for sess in sessions:
            resultat = sess.ResultatFinal.value
            resultats[resultat] = resultats.get(resultat, 0) + 1
        
        print(f"\nSessions de test ({len(sessions)} total) :")
        for resultat, count in resultats.items():
            print(f"  {resultat} : {count}")
        
        # Compter les programmes par statut
        programmes = db.query(ProgrammeDeTest).all()
        statuts = {}
        for prog in programmes:
            statut = prog.StatutExecution.value
            statuts[statut] = statuts.get(statut, 0) + 1
        
        print(f"\nProgrammes de test ({len(programmes)} total) :")
        for statut, count in statuts.items():
            print(f"  {statut} : {count}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des statistiques : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 DÉMONSTRATION GESTIA")
    print("=" * 30)
    
    # Initialiser la base de données
    init_database()
    
    # Créer les données d'exemple
    creer_donnees_exemple()
    
    # Afficher les statistiques
    afficher_statistiques()
    
    print("\n✅ Démonstration terminée !")
    print("Vous pouvez maintenant lancer 'python main.py' pour utiliser l'interface interactive.") 