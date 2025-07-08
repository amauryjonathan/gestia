#!/usr/bin/env python3
"""
Test d'intégration des migrations
================================

Script pour tester que l'intégration automatique des migrations fonctionne.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_migration_integration():
    """Test l'intégration des migrations"""
    print("🧪 Test d'intégration des migrations GESTIA")
    print("=" * 50)
    
    try:
        # Test 1: Import du gestionnaire de migrations
        print("1️⃣ Test d'import du gestionnaire de migrations...")
        from gestia.core.migration_manager import auto_migrate_on_startup, get_migration_status
        print("✅ Import réussi")
        
        # Test 2: Vérification du statut
        print("\n2️⃣ Vérification du statut des migrations...")
        status = get_migration_status('development')
        print(f"   Environnement: {status.get('environment', 'N/A')}")
        print(f"   Total migrations: {status.get('total_migrations', 0)}")
        print(f"   Migrations appliquées: {status.get('applied_migrations', 0)}")
        print(f"   Migrations en attente: {status.get('pending_migrations', 0)}")
        print(f"   Base à jour: {status.get('is_up_to_date', False)}")
        
        if status.get('error'):
            print(f"   ❌ Erreur: {status['error']}")
            return False
        
        # Test 3: Application des migrations si nécessaire
        print("\n3️⃣ Test d'application automatique des migrations...")
        migrations_applied = auto_migrate_on_startup('development', verbose=True)
        
        if migrations_applied:
            print("✅ Migrations appliquées avec succès")
        else:
            print("✅ Aucune migration nécessaire")
        
        # Test 4: Vérification finale
        print("\n4️⃣ Vérification finale...")
        final_status = get_migration_status('development')
        if final_status.get('is_up_to_date', False):
            print("✅ Base de données à jour - test réussi !")
            return True
        else:
            print("❌ Base de données pas à jour après migration")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test la connexion à la base de données"""
    print("\n🔗 Test de connexion à la base de données...")
    
    try:
        from gestia.core.database import db_manager, init_database
        from gestia.core.services import AppareilService
        
        # Initialiser la base
        init_database()
        db = db_manager.get_session()
        
        # Tester une requête simple
        appareils = AppareilService.lister_appareils(db)
        print(f"✅ Connexion réussie - {len(appareils)} appareils trouvés")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests d'intégration...")
    
    # Test des migrations
    migration_ok = test_migration_integration()
    
    # Test de la base de données
    db_ok = test_database_connection()
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 50)
    print(f"Migrations: {'✅ OK' if migration_ok else '❌ ÉCHEC'}")
    print(f"Base de données: {'✅ OK' if db_ok else '❌ ÉCHEC'}")
    
    if migration_ok and db_ok:
        print("\n🎉 Tous les tests sont passés ! L'intégration fonctionne correctement.")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez la configuration.") 