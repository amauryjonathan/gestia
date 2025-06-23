from sqlalchemy import create_engine, Column, String, Date, Boolean, ForeignKey, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, date
import enum

Base = declarative_base()

# Enums
class EtatAppareil(enum.Enum):
    EN_TEST = "En Test"
    EN_REPARATION = "En Réparation"
    RECONDITIONNE = "Reconditionné"
    EN_VENTE = "En Vente"
    IRREPARABLE = "Irréparable"

class ResultatSession(enum.Enum):
    PASSE = "Passé"
    ECHOUÉ = "Échoué"
    EN_COURS = "En Cours"
    REPARE = "Réparé"

class NomProgramme(enum.Enum):
    RAPIDE = "Rapide"
    COTON_90 = "Coton 90"
    ESSORAGE = "Essorage"

class StatutExecution(enum.Enum):
    NON_LANCE = "Non Lancé"
    EN_COURS = "En Cours"
    TERMINE_OK = "Terminé OK"
    TERMINE_ECHEC = "Terminé Échec"

class NomCritere(enum.Enum):
    VERROUILLAGE_PORTE = "Verrouillage Porte"
    VIDANGE = "Vidange"
    REMPLISSAGE = "Remplissage"
    ROTATION = "Rotation"
    CHAUFFE = "Chauffe"
    ESSORAGE = "Essorage"
    PROGRAMME_TERMINE = "Programme Terminé"

class ResultatReparation(enum.Enum):
    REUSSI = "Réussi"
    ECHOUÉ_IRREPARABLE = "Échoué / Irréparable"

# Classes du modèle
class Appareil(Base):
    __tablename__ = 'appareils'
    
    ID_Appareil = Column(String(50), primary_key=True)
    Marque = Column(String(100), nullable=False)
    Modele = Column(String(100), nullable=False)
    DateReception = Column(Date, nullable=False)
    Etat = Column(Enum(EtatAppareil), nullable=False, default=EtatAppareil.EN_TEST)
    DateMiseEnVente = Column(Date, nullable=True)
    
    # Relations
    sessions = relationship("SessionDeTest", back_populates="appareil")
    diagnostics = relationship("DiagnosticReparation", back_populates="appareil")

class Technicien(Base):
    __tablename__ = 'techniciens'
    
    ID_Technicien = Column(String(50), primary_key=True)
    Nom = Column(String(100), nullable=False)
    Prenom = Column(String(100), nullable=False)
    
    # Relations
    sessions = relationship("SessionDeTest", back_populates="technicien")
    diagnostics = relationship("DiagnosticReparation", back_populates="technicien")
    criteres_valides = relationship("CritereDeTest", back_populates="technicien")

class SessionDeTest(Base):
    __tablename__ = 'sessions_de_test'
    
    ID_Session = Column(String(50), primary_key=True)
    DateDebut = Column(Date, nullable=False)
    DateFin = Column(Date, nullable=True)
    ResultatFinal = Column(Enum(ResultatSession), nullable=False, default=ResultatSession.EN_COURS)
    Commentaires = Column(Text, nullable=True)
    
    # Clés étrangères
    ID_Appareil = Column(String(50), ForeignKey('appareils.ID_Appareil'), nullable=False)
    ID_Technicien = Column(String(50), ForeignKey('techniciens.ID_Technicien'), nullable=False)
    
    # Relations
    appareil = relationship("Appareil", back_populates="sessions")
    technicien = relationship("Technicien", back_populates="sessions")
    programmes = relationship("ProgrammeDeTest", back_populates="session")
    diagnostics = relationship("DiagnosticReparation", back_populates="session_source")

class ProgrammeDeTest(Base):
    __tablename__ = 'programmes_de_test'
    
    ID_Programme = Column(String(50), primary_key=True)
    NomProgramme = Column(Enum(NomProgramme), nullable=False)
    StatutExecution = Column(Enum(StatutExecution), nullable=False, default=StatutExecution.NON_LANCE)
    DateLancement = Column(Date, nullable=True)
    DateFinExecution = Column(Date, nullable=True)
    
    # Clé étrangère
    ID_Session = Column(String(50), ForeignKey('sessions_de_test.ID_Session'), nullable=False)
    
    # Relations
    session = relationship("SessionDeTest", back_populates="programmes")
    criteres = relationship("CritereDeTest", back_populates="programme")

class CritereDeTest(Base):
    __tablename__ = 'criteres_de_test'
    
    ID_Critere = Column(String(50), primary_key=True)
    NomCritere = Column(Enum(NomCritere), nullable=False)
    EstValide = Column(Boolean, nullable=False, default=False)
    DateValidation = Column(Date, nullable=True)
    CommentaireDefaut = Column(Text, nullable=True)
    
    # Clés étrangères
    ID_Programme = Column(String(50), ForeignKey('programmes_de_test.ID_Programme'), nullable=False)
    ID_Technicien = Column(String(50), ForeignKey('techniciens.ID_Technicien'), nullable=True)
    
    # Relations
    programme = relationship("ProgrammeDeTest", back_populates="criteres")
    technicien = relationship("Technicien", back_populates="criteres_valides")

class DiagnosticReparation(Base):
    __tablename__ = 'diagnostics_reparation'
    
    ID_DiagRep = Column(String(50), primary_key=True)
    DateDebut = Column(Date, nullable=False)
    DateFin = Column(Date, nullable=True)
    DescriptionProbleme = Column(Text, nullable=False)
    ActionsReparation = Column(Text, nullable=True)
    ResultatReparation = Column(Enum(ResultatReparation), nullable=True)
    
    # Clés étrangères
    ID_Appareil = Column(String(50), ForeignKey('appareils.ID_Appareil'), nullable=False)
    ID_Technicien = Column(String(50), ForeignKey('techniciens.ID_Technicien'), nullable=False)
    ID_Session = Column(String(50), ForeignKey('sessions_de_test.ID_Session'), nullable=True)
    
    # Relations
    appareil = relationship("Appareil", back_populates="diagnostics")
    technicien = relationship("Technicien", back_populates="diagnostics")
    session_source = relationship("SessionDeTest", back_populates="diagnostics") 