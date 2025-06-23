"""
Core package - Logique métier et données
========================================

Contient les modèles, services et gestion de base de données.
"""

from .models import *
from .database import db_manager, init_database
from .services import *

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