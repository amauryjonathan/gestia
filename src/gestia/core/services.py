#!/usr/bin/env python3
"""
Services - Logique métier GESTIA
================================

Contient tous les services pour la gestion des entités du système.
"""

from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Optional
import uuid

from .models import (
    Appareil, Technicien, SessionDeTest, ProgrammeDeTest, 
    CritereDeTest, DiagnosticReparation,
    EtatAppareil, ResultatSession, NomProgramme, StatutExecution,
    NomCritere, ResultatReparation
)

class AppareilService:
    @staticmethod
    def creer_appareil(db: Session, marque: str, modele: str, date_reception: date) -> Appareil:
        """Crée un nouvel appareil"""
        appareil = Appareil(
            ID_Appareil=f"APP_{uuid.uuid4().hex[:8].upper()}",
            Marque=marque,
            Modele=modele,
            DateReception=date_reception,
            Etat=EtatAppareil.EN_TEST
        )
        db.add(appareil)
        db.commit()
        db.refresh(appareil)
        return appareil
    
    @staticmethod
    def obtenir_appareil(db: Session, id_appareil: str) -> Optional[Appareil]:
        """Récupère un appareil par son ID"""
        return db.query(Appareil).filter(Appareil.ID_Appareil == id_appareil).first()
    
    @staticmethod
    def lister_appareils(db: Session) -> List[Appareil]:
        """Liste tous les appareils"""
        return db.query(Appareil).all()
    
    @staticmethod
    def modifier_etat_appareil(db: Session, id_appareil: str, nouvel_etat: EtatAppareil) -> bool:
        """Modifie l'état d'un appareil"""
        appareil = AppareilService.obtenir_appareil(db, id_appareil)
        if appareil:
            appareil.Etat = nouvel_etat
            if nouvel_etat == EtatAppareil.EN_VENTE:
                appareil.DateMiseEnVente = date.today()
            db.commit()
            return True
        return False
    
    @staticmethod
    def lister_marques(db: Session) -> List[str]:
        """Liste toutes les marques distinctes d'appareils"""
        marques = db.query(Appareil.Marque).distinct().all()
        return sorted([marque[0] for marque in marques])

class TechnicienService:
    @staticmethod
    def creer_technicien(db: Session, nom: str, prenom: str) -> Technicien:
        """Crée un nouveau technicien"""
        technicien = Technicien(
            ID_Technicien=f"TECH_{uuid.uuid4().hex[:8].upper()}",
            Nom=nom,
            Prenom=prenom
        )
        db.add(technicien)
        db.commit()
        db.refresh(technicien)
        return technicien
    
    @staticmethod
    def obtenir_technicien(db: Session, id_technicien: str) -> Optional[Technicien]:
        """Récupère un technicien par son ID"""
        return db.query(Technicien).filter(Technicien.ID_Technicien == id_technicien).first()
    
    @staticmethod
    def lister_techniciens(db: Session) -> List[Technicien]:
        """Liste tous les techniciens"""
        return db.query(Technicien).all()

class SessionDeTestService:
    @staticmethod
    def creer_session(db: Session, id_appareil: str, id_technicien: str) -> SessionDeTest:
        """Crée une nouvelle session de test"""
        session = SessionDeTest(
            ID_Session=f"SESS_{uuid.uuid4().hex[:8].upper()}",
            DateDebut=date.today(),
            ResultatFinal=ResultatSession.EN_COURS,
            ID_Appareil=id_appareil,
            ID_Technicien=id_technicien
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def terminer_session(db: Session, id_session: str, resultat: ResultatSession, commentaires: str = None) -> bool:
        """Termine une session de test"""
        session = db.query(SessionDeTest).filter(SessionDeTest.ID_Session == id_session).first()
        if session:
            session.DateFin = date.today()
            session.ResultatFinal = resultat
            session.Commentaires = commentaires
            db.commit()
            return True
        return False
    
    @staticmethod
    def obtenir_session(db: Session, id_session: str) -> Optional[SessionDeTest]:
        """Récupère une session par son ID"""
        return db.query(SessionDeTest).filter(SessionDeTest.ID_Session == id_session).first()

class ProgrammeDeTestService:
    @staticmethod
    def creer_programme(db: Session, id_session: str, nom_programme: NomProgramme) -> ProgrammeDeTest:
        """Crée un nouveau programme de test"""
        programme = ProgrammeDeTest(
            ID_Programme=f"PROG_{uuid.uuid4().hex[:8].upper()}",
            NomProgramme=nom_programme,
            StatutExecution=StatutExecution.NON_LANCE,
            ID_Session=id_session
        )
        db.add(programme)
        db.commit()
        db.refresh(programme)
        return programme
    
    @staticmethod
    def lancer_programme(db: Session, id_programme: str) -> bool:
        """Lance un programme de test"""
        programme = db.query(ProgrammeDeTest).filter(ProgrammeDeTest.ID_Programme == id_programme).first()
        if programme:
            programme.StatutExecution = StatutExecution.EN_COURS
            programme.DateLancement = date.today()
            db.commit()
            return True
        return False
    
    @staticmethod
    def terminer_programme(db: Session, id_programme: str, succes: bool) -> bool:
        """Termine un programme de test"""
        programme = db.query(ProgrammeDeTest).filter(ProgrammeDeTest.ID_Programme == id_programme).first()
        if programme:
            programme.StatutExecution = StatutExecution.TERMINE_OK if succes else StatutExecution.TERMINE_ECHEC
            programme.DateFinExecution = date.today()
            db.commit()
            return True
        return False

class CritereDeTestService:
    @staticmethod
    def creer_critere(db: Session, id_programme: str, nom_critere: NomCritere) -> CritereDeTest:
        """Crée un nouveau critère de test"""
        critere = CritereDeTest(
            ID_Critere=f"CRIT_{uuid.uuid4().hex[:8].upper()}",
            NomCritere=nom_critere,
            EstValide=False,
            ID_Programme=id_programme
        )
        db.add(critere)
        db.commit()
        db.refresh(critere)
        return critere
    
    @staticmethod
    def valider_critere(db: Session, id_critere: str, id_technicien: str, commentaire_defaut: str = None) -> bool:
        """Valide un critère de test"""
        critere = db.query(CritereDeTest).filter(CritereDeTest.ID_Critere == id_critere).first()
        if critere:
            critere.EstValide = True
            critere.DateValidation = date.today()
            critere.ID_Technicien = id_technicien
            critere.CommentaireDefaut = commentaire_defaut
            db.commit()
            return True
        return False

class DiagnosticReparationService:
    @staticmethod
    def creer_diagnostic(db: Session, id_appareil: str, id_technicien: str, 
                        description_probleme: str, id_session: str = None) -> DiagnosticReparation:
        """Crée un nouveau diagnostic/réparation"""
        diagnostic = DiagnosticReparation(
            ID_DiagRep=f"DIAG_{uuid.uuid4().hex[:8].upper()}",
            DateDebut=date.today(),
            DescriptionProbleme=description_probleme,
            ID_Appareil=id_appareil,
            ID_Technicien=id_technicien,
            ID_Session=id_session
        )
        db.add(diagnostic)
        db.commit()
        db.refresh(diagnostic)
        return diagnostic
    
    @staticmethod
    def terminer_diagnostic(db: Session, id_diagnostic: str, actions_reparation: str, 
                           resultat: ResultatReparation) -> bool:
        """Termine un diagnostic/réparation"""
        diagnostic = db.query(DiagnosticReparation).filter(DiagnosticReparation.ID_DiagRep == id_diagnostic).first()
        if diagnostic:
            diagnostic.DateFin = date.today()
            diagnostic.ActionsReparation = actions_reparation
            diagnostic.ResultatReparation = resultat
            db.commit()
            return True
        return False 