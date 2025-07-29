#!/usr/bin/env python3
"""
Script professionnel de comparaison d'environnements GESTIA
=========================================================

Compare les rapports de portabilité entre différents OS
avec une analyse détaillée des différences.
"""

import json
import os
import glob
import hashlib
from pathlib import Path
from datetime import datetime

class EnvironmentComparator:
    """Classe pour comparer les environnements entre OS"""
    
    def __init__(self):
        self.reports = {}
        self.differences = []
        self.warnings = []
    
    def load_reports(self):
        """Charge tous les rapports de portabilité"""
        print("📂 CHARGEMENT DES RAPPORTS")
        print("=" * 40)
        
        pattern = "portability_report_*.json"
        for report_file in glob.glob(pattern):
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    report = json.load(f)
                    os_name = report.get('os', 'unknown').lower()
                    self.reports[os_name] = report
                    print(f"✅ {report_file} - {os_name}")
            except Exception as e:
                print(f"❌ Erreur lecture {report_file}: {e}")
        
        print(f"\n📊 {len(self.reports)} rapport(s) chargé(s)")
        print()
    
    def compare_system_info(self):
        """Compare les informations système"""
        print("🖥️  COMPARAISON DES SYSTÈMES")
        print("=" * 40)
        
        if len(self.reports) < 2:
            print("❌ Il faut au moins 2 rapports pour comparer")
            return
        
        os_names = list(self.reports.keys())
        print(f"OS comparés: {', '.join(os_names)}")
        print()
        
        for os_name in os_names:
            report = self.reports[os_name]
            print(f"📋 {os_name.upper()}:")
            print(f"  - OS: {report.get('os', 'N/A')}")
            print(f"  - Version: {report.get('version', 'N/A')}")
            print(f"  - Python: {report.get('python', 'N/A').split()[0]}")
            print(f"  - Architecture: {report.get('architecture', 'N/A')}")
            print()
    
    def compare_file_hashes(self):
        """Compare les hashes des fichiers critiques"""
        print("🔍 COMPARAISON DES FICHIERS")
        print("=" * 40)
        
        critical_files = [
            "main.py",
            "src/gestia/core/database.py",
            "src/gestia/core/models.py",
            "src/gestia/core/services.py",
            "tools/manage_env.py"
        ]
        
        for file_path in critical_files:
            print(f"📄 {file_path}:")
            
            file_hashes = {}
            for os_name, report in self.reports.items():
                # Calculer le hash du fichier
                if os.path.exists(file_path):
                    hash_md5 = self.calculate_file_hash(file_path)
                    file_hashes[os_name] = hash_md5[:8]
                    print(f"  - {os_name}: {hash_md5[:8]}")
                else:
                    print(f"  - {os_name}: MANQUANT")
            
            # Vérifier si tous les hashes sont identiques
            unique_hashes = set(file_hashes.values())
            if len(unique_hashes) > 1:
                print(f"  ⚠️  DIFFÉRENCES DÉTECTÉES!")
                self.differences.append(f"Fichier {file_path} différent entre OS")
            else:
                print(f"  ✅ Identique sur tous les OS")
            
            print()
    
    def compare_database_sizes(self):
        """Compare les tailles des bases de données"""
        print("🗄️  COMPARAISON DES BASES DE DONNÉES")
        print("=" * 40)
        
        environments = ['development', 'production', 'test']
        
        for env in environments:
            print(f"📊 {env.upper()}:")
            db_path = f"data/{env}/gestia.db"
            
            env_sizes = {}
            for os_name, report in self.reports.items():
                if os.path.exists(db_path):
                    size = os.path.getsize(db_path)
                    env_sizes[os_name] = size
                    print(f"  - {os_name}: {size} bytes")
                else:
                    print(f"  - {os_name}: MANQUANT")
            
            # Vérifier les différences de taille
            if env_sizes:
                unique_sizes = set(env_sizes.values())
                if len(unique_sizes) > 1:
                    print(f"  ⚠️  TAILLES DIFFÉRENTES!")
                    self.differences.append(f"Base {env} de tailles différentes")
                else:
                    print(f"  ✅ Tailles identiques")
            
            print()
    
    def check_git_consistency(self):
        """Vérifie la cohérence Git entre OS"""
        print("📋 COHÉRENCE GIT")
        print("=" * 40)
        
        # Vérifier les fichiers non commités
        uncommitted_files = set()
        for os_name, report in self.reports.items():
            warnings = report.get('warnings', [])
            for warning in warnings:
                if 'Fichier non commité' in warning:
                    uncommitted_files.add(warning)
        
        if uncommitted_files:
            print("⚠️  Fichiers non commités détectés:")
            for file_warning in uncommitted_files:
                print(f"  - {file_warning}")
            self.warnings.append("Fichiers non synchronisés via Git")
        else:
            print("✅ Tous les fichiers sont commités")
        
        print()
    
    def calculate_file_hash(self, file_path):
        """Calcule le hash MD5 d'un fichier"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "ERROR"
    
    def generate_comparison_report(self):
        """Génère un rapport de comparaison"""
        print("📊 RAPPORT DE COMPARAISON")
        print("=" * 40)
        
        total_os = len(self.reports)
        print(f"📈 OS analysés: {total_os}")
        
        if self.differences:
            print(f"\n🚨 Différences détectées ({len(self.differences)}):")
            for diff in self.differences:
                print(f"  - {diff}")
        else:
            print("\n✅ Aucune différence critique détectée")
        
        if self.warnings:
            print(f"\n⚠️  Avertissements ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        print()
    
    def save_comparison_report(self):
        """Sauvegarde le rapport de comparaison"""
        comparison_report = {
            "timestamp": datetime.now().isoformat(),
            "os_count": len(self.reports),
            "os_list": list(self.reports.keys()),
            "differences": self.differences,
            "warnings": self.warnings,
            "summary": {
                "has_differences": len(self.differences) > 0,
                "has_warnings": len(self.warnings) > 0,
                "all_identical": len(self.differences) == 0
            }
        }
        
        report_file = f"comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(comparison_report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Rapport de comparaison sauvegardé: {report_file}")
        return report_file
    
    def run_comparison(self):
        """Exécute la comparaison complète"""
        print("🔍 COMPARAISON PROFESSIONNELLE D'ENVIRONNEMENTS GESTIA")
        print("=" * 60)
        print()
        
        # Charger les rapports
        self.load_reports()
        
        if len(self.reports) < 2:
            print("❌ Impossible de comparer - il faut au moins 2 rapports")
            print("💡 Exécutez professional_portability_check.py sur vos différents OS")
            return
        
        # Effectuer les comparaisons
        self.compare_system_info()
        self.compare_file_hashes()
        self.compare_database_sizes()
        self.check_git_consistency()
        
        # Générer le rapport
        self.generate_comparison_report()
        report_file = self.save_comparison_report()
        
        print("✅ Comparaison terminée !")
        print(f"📁 Rapport: {report_file}")
        
        # Retourner le statut
        if self.differences:
            print("🚨 ATTENTION: Différences détectées entre les OS!")
            return False
        else:
            print("✅ Tous les environnements sont cohérents!")
            return True

def main():
    """Fonction principale"""
    comparator = EnvironmentComparator()
    success = comparator.run_comparison()
    
    if not success:
        sys.exit(1)  # Différences détectées
    else:
        sys.exit(0)  # Succès

if __name__ == "__main__":
    import sys
    main() 