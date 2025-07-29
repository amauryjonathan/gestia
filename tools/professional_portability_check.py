#!/usr/bin/env python3
"""
Script professionnel de vérification de portabilité GESTIA
========================================================

Simule les pratiques professionnelles pour garantir la portabilité
entre différents systèmes d'exploitation.
"""

import os
import sys
import platform
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

class PortabilityChecker:
    """Classe pour vérifier la portabilité du projet"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "os": platform.system(),
            "version": platform.release(),
            "python": sys.version,
            "architecture": platform.machine(),
            "checks": {},
            "errors": [],
            "warnings": []
        }
    
    def check_file_structure(self):
        """Vérifie la structure des fichiers critiques"""
        print("📁 VÉRIFICATION DE LA STRUCTURE")
        print("=" * 40)
        
        critical_files = [
            "main.py",
            "src/gestia/core/database.py",
            "src/gestia/core/models.py",
            "src/gestia/core/services.py",
            "tools/manage_env.py",
            "data/.env_config.json",
            "requirements.txt"
        ]
        
        structure_ok = True
        for file_path in critical_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {file_path} ({size} bytes)")
            else:
                print(f"❌ {file_path} - MANQUANT")
                structure_ok = False
                self.report["errors"].append(f"Fichier manquant: {file_path}")
        
        self.report["checks"]["structure"] = structure_ok
        print()
        return structure_ok
    
    def check_database_consistency(self):
        """Vérifie la cohérence des bases de données"""
        print("🗄️  VÉRIFICATION DES BASES DE DONNÉES")
        print("=" * 40)
        
        environments = ['development', 'production', 'test']
        db_consistency = True
        
        for env in environments:
            db_path = f"data/{env}/gestia.db"
            if os.path.exists(db_path):
                size = os.path.getsize(db_path)
                # Calculer le hash pour vérifier l'intégrité
                hash_md5 = self.calculate_file_hash(db_path)
                print(f"✅ {env}: {db_path} ({size} bytes) - Hash: {hash_md5[:8]}")
            else:
                print(f"❌ {env}: {db_path} - MANQUANT")
                db_consistency = False
                self.report["errors"].append(f"Base de données manquante: {db_path}")
        
        self.report["checks"]["database"] = db_consistency
        print()
        return db_consistency
    
    def check_dependencies(self):
        """Vérifie les dépendances Python"""
        print("📦 VÉRIFICATION DES DÉPENDANCES")
        print("=" * 40)
        
        required_modules = [
            "sqlalchemy",
            "tkinter",
            "json",
            "pathlib",
            "sqlite3"
        ]
        
        dependencies_ok = True
        for module in required_modules:
            try:
                __import__(module)
                print(f"✅ {module}")
            except ImportError:
                print(f"❌ {module} - MANQUANT")
                dependencies_ok = False
                self.report["errors"].append(f"Module manquant: {module}")
        
        self.report["checks"]["dependencies"] = dependencies_ok
        print()
        return dependencies_ok
    
    def check_paths_portability(self):
        """Vérifie la portabilité des chemins"""
        print("🔗 VÉRIFICATION DE LA PORTABILITÉ DES CHEMINS")
        print("=" * 40)
        
        # Vérifier les chemins critiques
        critical_paths = [
            "data/development/gestia.db",
            "data/production/gestia.db",
            "data/test/gestia.db"
        ]
        
        paths_ok = True
        for path in critical_paths:
            # Vérifier que le chemin utilise des séparateurs portables
            normalized_path = os.path.normpath(path)
            if normalized_path == path:
                print(f"✅ {path} - Portable")
            else:
                print(f"⚠️  {path} - Normalisé vers: {normalized_path}")
                self.report["warnings"].append(f"Chemin normalisé: {path}")
        
        self.report["checks"]["paths"] = paths_ok
        print()
        return paths_ok
    
    def check_encoding(self):
        """Vérifie l'encodage des caractères"""
        print("🔤 VÉRIFICATION DE L'ENCODAGE")
        print("=" * 40)
        
        test_strings = [
            "éèàçù€£¥",
            "Hello World",
            "1234567890",
            "!@#$%^&*()"
        ]
        
        encoding_ok = True
        for test_str in test_strings:
            try:
                encoded = test_str.encode('utf-8')
                decoded = encoded.decode('utf-8')
                if decoded == test_str:
                    print(f"✅ '{test_str}' - Encodage OK")
                else:
                    print(f"❌ '{test_str}' - Problème d'encodage")
                    encoding_ok = False
            except Exception as e:
                print(f"❌ '{test_str}' - Erreur: {e}")
                encoding_ok = False
        
        self.report["checks"]["encoding"] = encoding_ok
        print()
        return encoding_ok
    
    def check_git_status(self):
        """Vérifie l'état Git du projet"""
        print("📋 ÉTAT GIT")
        print("=" * 40)
        
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                if changes:
                    print("⚠️  Fichiers modifiés non commités:")
                    for change in changes:
                        if change:
                            print(f"  - {change}")
                            self.report["warnings"].append(f"Fichier non commité: {change}")
                else:
                    print("✅ Aucune modification non commitée")
                
                # Vérifier la branche actuelle
                branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                            capture_output=True, text=True, timeout=10)
                if branch_result.returncode == 0:
                    current_branch = branch_result.stdout.strip()
                    print(f"🌿 Branche actuelle: {current_branch}")
                
            else:
                print("❌ Erreur Git")
                self.report["errors"].append("Erreur lors de la vérification Git")
                
        except Exception as e:
            print(f"❌ Erreur vérification Git: {e}")
            self.report["errors"].append(f"Exception Git: {e}")
        
        print()
    
    def calculate_file_hash(self, file_path):
        """Calcule le hash MD5 d'un fichier"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "ERROR"
    
    def generate_summary(self):
        """Génère un résumé de la vérification"""
        print("📊 RÉSUMÉ DE LA VÉRIFICATION")
        print("=" * 40)
        
        total_checks = len(self.report["checks"])
        passed_checks = sum(1 for check in self.report["checks"].values() if check)
        failed_checks = total_checks - passed_checks
        
        print(f"✅ Tests réussis: {passed_checks}/{total_checks}")
        print(f"❌ Tests échoués: {failed_checks}/{total_checks}")
        
        if self.report["errors"]:
            print(f"\n🚨 Erreurs ({len(self.report['errors'])}):")
            for error in self.report["errors"]:
                print(f"  - {error}")
        
        if self.report["warnings"]:
            print(f"\n⚠️  Avertissements ({len(self.report['warnings'])}):")
            for warning in self.report["warnings"]:
                print(f"  - {warning}")
        
        print()
    
    def save_report(self):
        """Sauvegarde le rapport"""
        report_file = f"portability_report_{platform.system().lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport sauvegardé: {report_file}")
        return report_file
    
    def run_all_checks(self):
        """Exécute tous les tests de portabilité"""
        print("🔍 VÉRIFICATION PROFESSIONNELLE DE PORTABILITÉ GESTIA")
        print("=" * 60)
        print()
        
        # Exécuter tous les tests
        self.check_file_structure()
        self.check_database_consistency()
        self.check_dependencies()
        self.check_paths_portability()
        self.check_encoding()
        self.check_git_status()
        
        # Générer le résumé
        self.generate_summary()
        
        # Sauvegarder le rapport
        report_file = self.save_report()
        
        print("✅ Vérification terminée !")
        print("💡 Comparez les rapports entre vos différents OS")
        print(f"📁 Rapport: {report_file}")
        
        return self.report

def main():
    """Fonction principale"""
    checker = PortabilityChecker()
    report = checker.run_all_checks()
    
    # Retourner le code de sortie approprié
    if report["errors"]:
        sys.exit(1)  # Erreur
    elif report["warnings"]:
        sys.exit(2)  # Avertissements
    else:
        sys.exit(0)  # Succès

if __name__ == "__main__":
    main() 