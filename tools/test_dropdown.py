#!/usr/bin/env python3
"""
Test du dropdown des marques
============================

Script pour tester la nouvelle fonctionnalité de dropdown des marques.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import init_database, db_manager, set_environment
from gestia.core.services import AppareilService

def test_dropdown_marques():
    """Test de la fonctionnalité dropdown des marques"""
    print("🧪 Test du dropdown des marques")
    print("=" * 40)
    
    # Initialiser l'environnement de test
    set_environment('development')
    init_database()
    db = db_manager.get_session()
    
    try:
        # 1. Vérifier les marques existantes
        print("📋 Marques existantes dans la base :")
        marques = AppareilService.lister_marques(db)
        
        if marques:
            for i, marque in enumerate(marques, 1):
                print(f"  {i}. {marque}")
        else:
            print("  Aucune marque trouvée")
        
        print(f"\n✅ Total : {len(marques)} marques distinctes")
        
        # 2. Tester la création d'un nouvel appareil avec une marque existante
        print("\n🔧 Test de création d'appareil avec marque existante...")
        if marques:
            marque_test = marques[0]
            appareil = AppareilService.creer_appareil(
                db, marque_test, "Test-Model-001", "2025-06-29"
            )
            print(f"  ✅ Appareil créé : {appareil.ID_Appareil} - {appareil.Marque} {appareil.Modele}")
        
        # 3. Tester la création avec une nouvelle marque
        print("\n🆕 Test de création d'appareil avec nouvelle marque...")
        nouvelle_marque = "TestBrand-2025"
        appareil2 = AppareilService.creer_appareil(
            db, nouvelle_marque, "Test-Model-002", "2025-06-29"
        )
        print(f"  ✅ Appareil créé : {appareil2.ID_Appareil} - {appareil2.Marque} {appareil2.Modele}")
        
        # 4. Vérifier que la nouvelle marque apparaît dans la liste
        print("\n📋 Vérification de la mise à jour de la liste des marques :")
        marques_apres = AppareilService.lister_marques(db)
        print(f"  ✅ Nouvelles marques disponibles : {len(marques_apres)}")
        
        if nouvelle_marque in marques_apres:
            print(f"  ✅ Nouvelle marque '{nouvelle_marque}' bien ajoutée à la liste")
        else:
            print(f"  ❌ Nouvelle marque '{nouvelle_marque}' non trouvée dans la liste")
        
        print("\n🎉 Test terminé avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_dropdown_marques() 