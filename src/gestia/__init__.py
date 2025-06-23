"""
GESTIA - Système de Gestion d'Appareils
=======================================

Un système complet de gestion d'appareils avec tests, diagnostics et réparations.
"""

__version__ = "1.0.0"
__author__ = "Assistant IA"
__description__ = "Système de Gestion d'Appareils avec Interface Graphique"

# Imports principaux pour faciliter l'utilisation
from .core.models import *
from .core.database import db_manager, init_database
from .core.services import *

__all__ = [
    'db_manager',
    'init_database',
    'AppareilService',
    'TechnicienService',
    'SessionDeTestService',
    'ProgrammeDeTestService',
    'CritereDeTestService',
    'DiagnosticReparationService'
] 