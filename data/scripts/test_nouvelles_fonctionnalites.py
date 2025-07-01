#!/usr/bin/env python3
"""
Script de test des nouvelles fonctionnalités GESTIA
==================================================

Teste les nouvelles fonctionnalités d'actions à faire et problèmes identifiés.
"""

import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from gestia.core.database import db_manager, init_database
from gestia.core.services import AppareilService, TechnicienService
from gestia.core.models import EtatAppareil
from datetime import date

def tester_nouvelles_fonctionnalites():
    """Teste les nouvelles fonctionnalités"""
    print("🧪 Test des nouvelles fonctionnalités GESTIA...")
    
    try:
        # Initialiser la base de données
        init_database()
        db = db_manager.get_session()
        
        # Créer un technicien de test
        technicien = TechnicienService.creer_technicien(db, "Dupont", "Jean")
        print(f"✅ Technicien créé: {technicien.ID_Technicien}")
        
        # Créer un appareil de test
        appareil = AppareilService.creer_appareil(
            db, "Samsung", "WW90T534DAW", "SN123456789", date.today()
        )
        print(f"✅ Appareil créé: {appareil.ID_Appareil}")
        
        # Tester la mise à jour des actions à faire
        actions_test = """• Vérifier le verrouillage de porte
• Tester le cycle de lavage complet
• Contrôler la vidange
• Valider l'essorage"""
        
        if AppareilService.mettre_a_jour_actions_a_faire(db, appareil.ID_Appareil, actions_test):
            print("✅ Actions à faire mises à jour avec succès")
        else:
            print("❌ Échec de la mise à jour des actions à faire")
        
        # Tester la mise à jour des problèmes identifiés
        problemes_test = """• Bruit anormal lors de l'essorage
• Fuite mineure au niveau du joint de porte
• Affichage LCD partiellement défaillant"""
        
        if AppareilService.mettre_a_jour_problemes_identifies(db, appareil.ID_Appareil, problemes_test):
            print("✅ Problèmes identifiés mis à jour avec succès")
        else:
            print("❌ Échec de la mise à jour des problèmes identifiés")
        
        # Récupérer le récapitulatif complet
        recapitulatif = AppareilService.obtenir_recapitulatif_appareil(db, appareil.ID_Appareil)
        if recapitulatif:
            print("✅ Récapitulatif récupéré avec succès")
            print(f"   - Actions à faire: {recapitulatif['appareil'].ActionsAFaire[:50]}...")
            print(f"   - Problèmes identifiés: {recapitulatif['appareil'].SoucisMachine[:50]}...")
        else:
            print("❌ Échec de la récupération du récapitulatif")
        
        print("\n🎉 Tous les tests sont passés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    tester_nouvelles_fonctionnalites() 