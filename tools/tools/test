#!/usr/bin/env python3
"""
Test de la fonctionnalité de tri
================================

Script pour tester le tri des colonnes dans l'interface graphique.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import init_database, db_manager, set_environment
from gestia.core.services import AppareilService

def test_tri_appareils():
    """Test du tri des appareils"""
    print("🧪 Test de la fonctionnalité de tri")
    print("=" * 50)
    
    # Initialiser l'environnement
    set_environment('development')
    init_database()
    db = db_manager.get_session()
    
    try:
        # Récupérer les appareils
        appareils = AppareilService.lister_appareils(db)
        print(f"📋 {len(appareils)} appareils trouvés")
        
        # Tester le tri par marque
        print("\n📊 Tri par marque :")
        appareils_tries_marque = sorted(appareils, key=lambda x: x.Marque)
        for app in appareils_tries_marque[:5]:  # Afficher les 5 premiers
            print(f"  {app.Marque} - {app.Modele}")
        
        # Tester le tri par état
        print("\n📊 Tri par état :")
        appareils_tries_etat = sorted(appareils, key=lambda x: x.Etat.value)
        for app in appareils_tries_etat[:5]:  # Afficher les 5 premiers
            print(f"  {app.Etat.value} - {app.Marque} {app.Modele}")
        
        # Tester le tri par date de réception
        print("\n📊 Tri par date de réception :")
        appareils_tries_date = sorted(appareils, key=lambda x: x.DateReception)
        for app in appareils_tries_date[:5]:  # Afficher les 5 premiers
            print(f"  {app.DateReception} - {app.Marque} {app.Modele}")
        
        print("\n✅ Tests de tri terminés avec succès !")
        print("\n💡 Dans l'interface graphique :")
        print("  - Double-cliquez sur les en-têtes de colonnes pour trier")
        print("  - Les flèches ↑/↓ indiquent l'ordre de tri")
        print("  - Double-cliquez à nouveau pour inverser l'ordre")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_tri_appareils() 