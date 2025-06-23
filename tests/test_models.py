#!/usr/bin/env python3
"""
Tests pour les modèles GESTIA
=============================

Tests unitaires pour les modèles de données.
"""

import pytest
from datetime import date
import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.models import (
    Appareil, Technicien, SessionDeTest, ProgrammeDeTest,
    CritereDeTest, DiagnosticReparation,
    EtatAppareil, ResultatSession, NomProgramme, StatutExecution,
    NomCritere, ResultatReparation
)

class TestModels:
    """Tests pour les modèles de données"""
    
    def test_appareil_creation(self):
        """Test de création d'un appareil"""
        appareil = Appareil(
            Marque="Samsung",
            Modele="WF45T6000AW",
            DateReception=date.today(),
            Etat=EtatAppareil.EN_TEST
        )
        
        assert appareil.Marque == "Samsung"
        assert appareil.Modele == "WF45T6000AW"
        assert appareil.Etat == EtatAppareil.EN_TEST
    
    def test_technicien_creation(self):
        """Test de création d'un technicien"""
        technicien = Technicien(
            Nom="Dupont",
            Prenom="Jean"
        )
        
        assert technicien.Nom == "Dupont"
        assert technicien.Prenom == "Jean"
    
    def test_etat_appareil_enum(self):
        """Test des énumérations d'état d'appareil"""
        assert EtatAppareil.EN_TEST.value == "En Test"
        assert EtatAppareil.EN_REPARATION.value == "En Réparation"
        assert EtatAppareil.RECONDITIONNE.value == "Reconditionné"
        assert EtatAppareil.EN_VENTE.value == "En Vente"
        assert EtatAppareil.IRREPARABLE.value == "Irréparable"
    
    def test_nom_programme_enum(self):
        """Test des énumérations de programmes de test"""
        assert NomProgramme.RAPIDE.value == "Rapide"
        assert NomProgramme.COTON_90.value == "Coton 90"
        assert NomProgramme.ESSORAGE.value == "Essorage" 