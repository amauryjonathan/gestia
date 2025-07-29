#!/usr/bin/env python3
"""
Script de vérification de la portabilité GESTIA
==============================================

Vérifie que le projet fonctionne identiquement sur différents OS.
"""

import os
import sys
import platform
import json
from pathlib import Path

def check_os_info():
    """Affiche les informations du système d'exploitation"""
    print("🖥️  INFORMATIONS SYSTÈME")
    print("=" * 40)
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {sys.version}")
    print()

def check_paths():
    """Vérifie la portabilité des chemins"""
    print("📁 VÉRIFICATION DES CHEMINS")
    print("=" * 40)
    
    # Chemins à vérifier
    paths_to_check = [
        "data/development/gestia.db",
        "data/production/gestia.db", 
        "data/test/gestia.db",
        "data/.env_config.json",
        "src/gestia/core/database.py",
        "tools/manage_env.py"
    ]
    
    for path in paths_to_check:
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"{status} {path}")
    
    print()

def check_imports():
    """Vérifie que tous les imports fonctionnent"""
    print("📦 VÉRIFICATION DES IMPORTS")
    print("=" * 40)
    
    modules_to_check = [
        "sqlalchemy",
        "tkinter",
        "json",
        "pathlib"
    ]
    
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - MANQUANT")
    
    print()

def check_encoding():
    """Vérifie l'encodage des caractères"""
    print("🔤 VÉRIFICATION DE L'ENCODAGE")
    print("=" * 40)
    
    # Test d'encodage
    test_string = "éèàçù€£¥"
    try:
        encoded = test_string.encode('utf-8')
        decoded = encoded.decode('utf-8')
        if decoded == test_string:
            print("✅ Encodage UTF-8 fonctionne")
        else:
            print("❌ Problème d'encodage")
    except Exception as e:
        print(f"❌ Erreur d'encodage: {e}")
    
    print()

def check_configuration():
    """Vérifie la configuration du projet"""
    print("⚙️  VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 40)
    
    # Vérifier le fichier de configuration
    config_file = "data/.env_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                env = config.get('environment', 'development')
                print(f"✅ Environnement actuel: {env}")
        except Exception as e:
            print(f"❌ Erreur lecture config: {e}")
    else:
        print("❌ Fichier de configuration manquant")
    
    print()

def check_database_consistency():
    """Vérifie la cohérence des bases de données"""
    print("🗄️  VÉRIFICATION DES BASES DE DONNÉES")
    print("=" * 40)
    
    environments = ['development', 'production', 'test']
    
    for env in environments:
        db_path = f"data/{env}/gestia.db"
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"✅ {env}: {db_path} ({size} bytes)")
        else:
            print(f"❌ {env}: {db_path} - MANQUANT")
    
    print()

def generate_report():
    """Génère un rapport de portabilité"""
    print("📊 RAPPORT DE PORTABILITÉ")
    print("=" * 40)
    
    # Informations système
    report = {
        "os": platform.system(),
        "version": platform.release(),
        "python": sys.version,
        "architecture": platform.machine(),
        "timestamp": str(Path().cwd()),
        "checks": {}
    }
    
    # Sauvegarder le rapport
    report_file = f"portability_report_{platform.system().lower()}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Rapport sauvegardé: {report_file}")
    print()

def main():
    """Fonction principale"""
    print("🔍 VÉRIFICATION DE LA PORTABILITÉ GESTIA")
    print("=" * 50)
    print()
    
    check_os_info()
    check_paths()
    check_imports()
    check_encoding()
    check_configuration()
    check_database_consistency()
    generate_report()
    
    print("✅ Vérification terminée !")
    print("💡 Comparez les rapports entre vos différents OS")

if __name__ == "__main__":
    main() 