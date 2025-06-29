#!/usr/bin/env python3
"""
Analyse des références d'appareils
==================================

Script pour analyser et décomposer les références complexes d'appareils électroménagers.
"""

import re
import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import init_database, db_manager, set_environment
from gestia.core.services import AppareilService

class AnalyseurReferences:
    """Classe pour analyser les références d'appareils"""
    
    def __init__(self):
        self.patterns = {
            'samsung_lave_linge': r'^WW(\d+)([A-Z])(\d+)([A-Z]+)(?:/([A-Z]+))?$',
            'samsung_lave_vaisselle': r'^DW(\d+)([A-Z])(\d+)([A-Z]+)(?:/([A-Z]+))?$',
            'lg_lave_linge': r'^F[A-Z](\d+)([A-Z]+)(\d+)([A-Z]+)(?:/([A-Z]+))?$',
            'bosch_lave_linge': r'^W[A-Z](\d+)([A-Z]+)(\d+)([A-Z]+)(?:/([A-Z]+))?$',
        }
        
        self.technologies = {
            'T': 'EcoBubble',
            'S': 'Steam',
            'V': 'VarioPerfect',
            'Q': 'QuickDrive',
            'A': 'AddWash',
            'D': 'Digital Inverter',
            'E': 'EcoSilence',
        }
        
        self.variantes = {
            'EF': 'Blanc',
            'BK': 'Noir',
            'SI': 'Inox',
            'WH': 'Blanc',
            'BL': 'Bleu',
            'GR': 'Gris',
        }
    
    def analyser_reference_samsung(self, reference):
        """Analyse une référence Samsung"""
        print(f"🔍 Analyse de la référence : {reference}")
        print("=" * 50)
        
        # Pattern pour Samsung WW90T534DAW/EF
        pattern = r'^WW(\d+)([A-Z])(\d+)([A-Z]+)(?:/([A-Z]+))?$'
        match = re.match(pattern, reference.upper())
        
        if match:
            capacite = match.group(1) + "kg"
            technologie_code = match.group(2)
            numero_modele = match.group(3)
            suffixe = match.group(4)
            variante = match.group(5)
            
            technologie = self.technologies.get(technologie_code, f"Technologie {technologie_code}")
            variante_nom = self.variantes.get(variante, variante) if variante else "Standard"
            
            print(f"📋 Décomposition :")
            print(f"  🏭 Marque : Samsung")
            print(f"  📦 Série : WW (Lave-linge)")
            print(f"  ⚖️ Capacité : {capacite}")
            print(f"  ⚡ Technologie : {technologie} ({technologie_code})")
            print(f"  🔢 Numéro modèle : {numero_modele}")
            print(f"  📝 Suffixe : {suffixe}")
            print(f"  🎨 Variante : {variante_nom} ({variante})")
            print(f"  🔗 Référence complète : {reference}")
            
            return {
                'marque': 'Samsung',
                'serie': 'WW',
                'capacite': capacite,
                'technologie': technologie,
                'technologie_code': technologie_code,
                'modele': numero_modele,
                'suffixe': suffixe,
                'variante': variante,
                'variante_nom': variante_nom,
                'reference_complete': reference
            }
        else:
            print(f"❌ Format non reconnu pour Samsung")
            return None
    
    def analyser_reference_generique(self, reference):
        """Analyse générique d'une référence"""
        print(f"🔍 Analyse générique : {reference}")
        print("=" * 50)
        
        # Recherche de patterns communs
        if re.match(r'^[A-Z]{2}\d+', reference):
            serie = reference[:2]
            print(f"  📦 Série détectée : {serie}")
        
        # Recherche de capacité
        capacite_match = re.search(r'(\d+)(?:kg|KG)', reference, re.IGNORECASE)
        if capacite_match:
            capacite = capacite_match.group(1) + "kg"
            print(f"  ⚖️ Capacité détectée : {capacite}")
        
        # Recherche de technologie
        for code, tech in self.technologies.items():
            if code in reference.upper():
                print(f"  ⚡ Technologie détectée : {tech} ({code})")
        
        return {
            'reference_complete': reference,
            'serie': serie if 'serie' in locals() else None,
            'capacite': capacite if 'capacite' in locals() else None,
        }

def test_analyse_references():
    """Test de l'analyse des références"""
    print("🧪 Test d'analyse des références")
    print("=" * 60)
    
    analyseur = AnalyseurReferences()
    
    # Exemples de références Samsung
    references_samsung = [
        "WW90T534DAW/EF",
        "WW10T534DAW/BK",
        "DW60M6050FS/EF",
        "WW80T554DAW/SI"
    ]
    
    print("📱 Références Samsung :")
    for ref in references_samsung:
        print()
        resultat = analyseur.analyser_reference_samsung(ref)
        if resultat:
            print(f"✅ Analyse réussie")
        else:
            print(f"❌ Analyse échouée")
    
    print("\n" + "=" * 60)
    print("🔧 Références génériques :")
    
    # Exemples génériques
    references_generiques = [
        "LG F4WV510S0E",
        "Bosch WAT28441FF",
        "Whirlpool FSCR12440"
    ]
    
    for ref in references_generiques:
        print()
        resultat = analyseur.analyser_reference_generique(ref)

def analyser_appareils_existants():
    """Analyse les appareils existants dans la base"""
    print("\n📊 Analyse des appareils existants")
    print("=" * 60)
    
    # Initialiser l'environnement
    set_environment('development')
    init_database()
    db = db_manager.get_session()
    
    try:
        appareils = AppareilService.lister_appareils(db)
        analyseur = AnalyseurReferences()
        
        print(f"📋 {len(appareils)} appareils trouvés dans la base")
        
        for appareil in appareils[:5]:  # Analyser les 5 premiers
            print(f"\n🔍 Appareil {appareil.ID_Appareil}:")
            print(f"  Marque : {appareil.Marque}")
            print(f"  Modèle : {appareil.Modele}")
            
            # Tenter d'analyser la référence
            if appareil.Marque.upper() == 'SAMSUNG':
                analyseur.analyser_reference_samsung(appareil.Modele)
            else:
                analyseur.analyser_reference_generique(appareil.Modele)
        
        if len(appareils) > 5:
            print(f"\n... et {len(appareils) - 5} autres appareils")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_analyse_references()
    analyser_appareils_existants() 