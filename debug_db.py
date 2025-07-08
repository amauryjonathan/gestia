#!/usr/bin/env python3
"""
Script de diagnostic pour la base de données GESTIA
==================================================

Teste étape par étape l'initialisation de la base de données.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_import():
    """Teste l'import du module gestia"""
    print("🔍 Test 1: Import du module gestia")
    try:
        from gestia.core.database import init_database, set_environment
        print("✅ Import réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_environment():
    """Teste la configuration d'environnement"""
    print("\n🔍 Test 2: Configuration d'environnement")
    try:
        from gestia.core.database import set_environment
        set_environment('production')
        print("✅ Environnement configuré")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_database_creation():
    """Teste la création de la base de données"""
    print("\n🔍 Test 3: Création de la base de données")
    try:
        from gestia.core.database import init_database, db_manager
        
        # Vérifier le chemin de la base
        db_path = db_manager.get_database_path()
        print(f"📁 Chemin de la base: {db_path}")
        
        # Créer les tables
        init_database()
        
        # Vérifier que le fichier existe
        if os.path.exists(db_path):
            print(f"✅ Base de données créée: {db_path}")
            return True
        else:
            print(f"❌ Fichier de base non trouvé: {db_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de création: {e}")
        return False

def test_migrations():
    """Teste l'application des migrations"""
    print("\n🔍 Test 4: Application des migrations")
    try:
        from tools.tools.db.migrate_db import DatabaseMigrator
        
        migrator = DatabaseMigrator('production')
        migrator.migrate()
        print("✅ Migrations appliquées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de migration: {e}")
        return False

def main():
    """Point d'entrée principal"""
    print("🚀 Diagnostic de la base de données GESTIA")
    print("=" * 50)
    
    # Tests en séquence
    tests = [
        test_import,
        test_environment,
        test_database_creation,
        test_migrations
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    test_names = ["Import", "Environnement", "Création DB", "Migrations"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅" if result else "❌"
        print(f"{status} Test {i+1}: {name}")
    
    if all(results):
        print("\n🎉 Tous les tests sont passés !")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main() 