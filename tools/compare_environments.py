#!/usr/bin/env python3
"""
Script de comparaison d'environnements GESTIA
============================================

Compare les rapports de portabilité entre différents OS.
"""

import json
import os
import glob
from pathlib import Path

def load_reports():
    """Charge tous les rapports de portabilité"""
    reports = {}
    
    # Chercher tous les rapports
    pattern = "portability_report_*.json"
    for report_file in glob.glob(pattern):
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                os_name = report_file.replace('portability_report_', '').replace('.json', '')
                reports[os_name] = json.load(f)
        except Exception as e:
            print(f"❌ Erreur lecture {report_file}: {e}")
    
    return reports

def compare_reports(reports):
    """Compare les rapports entre OS"""
    print("🔍 COMPARAISON DES ENVIRONNEMENTS")
    print("=" * 50)
    
    if len(reports) < 2:
        print("❌ Il faut au moins 2 rapports pour comparer")
        print("💡 Exécutez check_portability.py sur vos différents OS")
        return
    
    os_names = list(reports.keys())
    print(f"📊 OS comparés: {', '.join(os_names)}")
    print()
    
    # Comparer les informations système
    print("🖥️  INFORMATIONS SYSTÈME")
    print("-" * 30)
    for os_name in os_names:
        report = reports[os_name]
        print(f"{os_name.upper()}:")
        print(f"  - OS: {report.get('os', 'N/A')}")
        print(f"  - Version: {report.get('version', 'N/A')}")
        print(f"  - Python: {report.get('python', 'N/A').split()[0]}")
        print()
    
    # Comparer les chemins
    print("📁 COHÉRENCE DES CHEMINS")
    print("-" * 30)
    
    # Chemins critiques à vérifier
    critical_paths = [
        "data/development/gestia.db",
        "data/production/gestia.db",
        "data/test/gestia.db",
        "data/.env_config.json"
    ]
    
    for path in critical_paths:
        print(f"🔍 {path}:")
        for os_name in os_names:
            report = reports[os_name]
            # Vérifier si le chemin existe dans le rapport
            exists = "✅" if path in report.get('checks', {}).get('paths', []) else "❌"
            print(f"  - {os_name}: {exists}")
        print()

def check_git_status():
    """Vérifie l'état Git du projet"""
    print("📋 ÉTAT GIT")
    print("=" * 30)
    
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            if changes:
                print("⚠️  Fichiers modifiés non commités:")
                for change in changes:
                    if change:  # Ignorer les lignes vides
                        print(f"  - {change}")
            else:
                print("✅ Aucune modification non commitée")
        else:
            print("❌ Erreur Git")
            
    except Exception as e:
        print(f"❌ Erreur vérification Git: {e}")
    
    print()

def check_file_consistency():
    """Vérifie la cohérence des fichiers critiques"""
    print("📄 COHÉRENCE DES FICHIERS")
    print("=" * 30)
    
    critical_files = [
        "main.py",
        "src/gestia/core/database.py",
        "src/gestia/core/models.py",
        "tools/manage_env.py",
        "data/.env_config.json"
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - MANQUANT")
    
    print()

def main():
    """Fonction principale"""
    print("🔍 COMPARAISON D'ENVIRONNEMENTS GESTIA")
    print("=" * 50)
    print()
    
    # Charger les rapports
    reports = load_reports()
    
    if not reports:
        print("❌ Aucun rapport trouvé")
        print("💡 Exécutez d'abord: python tools/check_portability.py")
        return
    
    # Comparer les rapports
    compare_reports(reports)
    
    # Vérifications supplémentaires
    check_git_status()
    check_file_consistency()
    
    print("✅ Comparaison terminée !")
    print("💡 Vérifiez que tous les OS ont les mêmes résultats")

if __name__ == "__main__":
    main() 