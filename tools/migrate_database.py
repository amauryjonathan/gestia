#!/usr/bin/env python3
"""
Migration de la base de données GESTIA
======================================

Script pour migrer la base de données vers la nouvelle structure avec les champs de référence détaillés.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gestia.core.database import init_database, db_manager, set_environment
from gestia.core.services import AppareilService
from gestia.core.models import Base
from sqlalchemy import text

def migrer_base_donnees():
    """Migre la base de données vers la nouvelle structure"""
    print("🔄 Migration de la base de données")
    print("=" * 50)
    
    # Initialiser l'environnement
    set_environment('development')
    db = db_manager.get_session()
    
    try:
        # 1. Vérifier si les nouvelles colonnes existent
        print("📋 Vérification de la structure actuelle...")
        
        # Obtenir la liste des colonnes existantes
        result = db.execute(text("PRAGMA table_info(appareils)"))
        colonnes_existantes = [row[1] for row in result.fetchall()]
        
        print(f"Colonnes existantes : {colonnes_existantes}")
        
        # 2. Ajouter les nouvelles colonnes si elles n'existent pas
        nouvelles_colonnes = [
            ('Serie', 'TEXT'),
            ('Capacite', 'TEXT'),
            ('Technologie', 'TEXT'),
            ('Variante', 'TEXT'),
            ('ReferenceComplete', 'TEXT')
        ]
        
        for nom_colonne, type_colonne in nouvelles_colonnes:
            if nom_colonne not in colonnes_existantes:
                print(f"➕ Ajout de la colonne {nom_colonne}...")
                db.execute(text(f"ALTER TABLE appareils ADD COLUMN {nom_colonne} {type_colonne}"))
                print(f"✅ Colonne {nom_colonne} ajoutée")
            else:
                print(f"✅ Colonne {nom_colonne} existe déjà")
        
        # 3. Valider les changements
        db.commit()
        print("✅ Migration terminée avec succès !")
        
        # 4. Vérifier la nouvelle structure
        print("\n📋 Nouvelle structure de la table appareils :")
        result = db.execute(text("PRAGMA table_info(appareils)"))
        for row in result.fetchall():
            print(f"  - {row[1]} ({row[2]})")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        db.rollback()
    finally:
        db.close()

def analyser_et_mettre_a_jour_references():
    """Analyse les références existantes et met à jour les nouveaux champs"""
    print("\n🔍 Analyse et mise à jour des références existantes")
    print("=" * 60)
    
    # Initialiser l'environnement
    set_environment('development')
    db = db_manager.get_session()
    
    try:
        from tools.analyse_references import AnalyseurReferences
        
        appareils = AppareilService.lister_appareils(db)
        analyseur = AnalyseurReferences()
        
        print(f"📋 {len(appareils)} appareils à analyser")
        
        for appareil in appareils:
            print(f"\n🔍 Analyse de {appareil.ID_Appareil}: {appareil.Marque} {appareil.Modele}")
            
            # Analyser la référence selon la marque
            if appareil.Marque.upper() == 'SAMSUNG':
                resultat = analyseur.analyser_reference_samsung(appareil.Modele)
                if resultat:
                    # Mettre à jour l'appareil avec les nouvelles informations
                    appareil.Serie = resultat.get('serie')
                    appareil.Capacite = resultat.get('capacite')
                    appareil.Technologie = resultat.get('technologie')
                    appareil.Variante = resultat.get('variante')
                    appareil.ReferenceComplete = resultat.get('reference_complete')
                    print(f"  ✅ Mise à jour effectuée")
                else:
                    print(f"  ⚠️ Référence non reconnue")
            else:
                # Pour les autres marques, utiliser la référence complète
                appareil.ReferenceComplete = appareil.Modele
                print(f"  📝 Référence complète définie")
        
        # Sauvegarder les changements
        db.commit()
        print(f"\n✅ {len(appareils)} appareils mis à jour")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrer_base_donnees()
    analyser_et_mettre_a_jour_references() 