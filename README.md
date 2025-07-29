# 🏭 GESTIA - Système de Gestion d'Appareils

Un système complet de gestion d'appareils électroménagers avec tests, diagnostics et suivi des réparations.

## 📁 Structure du Projet

```
gestia/
├── 📁 src/gestia/           # Code source principal
│   ├── 📁 core/             # Logique métier et modèles
│   ├── 📁 ui/               # Interfaces utilisateur
│   └── 📁 utils/            # Utilitaires
├── 📁 data/                 # Données et environnements
│   ├── 📁 backups/          # Sauvegardes des bases
│   ├── 📁 samples/          # Données d'exemple CSV
│   └── 📁 scripts/          # Scripts de gestion des données
├── 📁 tools/                # Outils et scripts utilitaires
├── 📁 tests/                # Tests automatisés
│   └── 📁 unit/             # Tests unitaires
├── 📁 docs/                 # Documentation
├── main.py                  # Point d'entrée principal
├── pyproject.toml           # Configuration du projet
└── requirements.txt         # Dépendances Python
```

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Cloner le projet
git clone <votre-repo>
cd gestia

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration des environnements
```bash
# Voir l'environnement actuel
python tools/manage_env.py status

# Initialiser l'environnement de développement
python tools/manage_env.py init --env development

# Générer des données de test
python tools/manage_env.py generate
```

### 3. Lancement
```bash
# Interface graphique
python main.py

# Ou via l'outil de gestion
python tools/manage_env.py run
```

## 🛠️ Outils Disponibles

### Gestion des environnements
```bash
python tools/manage_env.py status          # Voir l'environnement actuel
python tools/manage_env.py switch --env production  # Changer d'environnement
python tools/manage_env.py init --env test         # Initialiser un environnement
python tools/manage_env.py generate               # Générer des données de test
```

### Exploration de la base de données
```bash
python tools/explore_db.py                 # Explorer la structure et les données
```

### Gestion des données
```bash
python data/scripts/generate_test_data.py  # Générer des données de test
python data/scripts/import_csv.py          # Importer depuis CSV
python data/scripts/backup_manager.py      # Gérer les sauvegardes
```

### Génération de données par environnement
```bash
# Générer des données pour l'environnement de développement
python tools/manage_env.py switch --env development
python tools/manage_env.py generate

# Générer des données pour l'environnement de test
python tools/manage_env.py switch --env test
python tools/manage_env.py generate

# Générer des données pour l'environnement de production
python tools/manage_env.py switch --env production
python tools/manage_env.py generate

# Note : Le script direct generate_test_data.py génère uniquement pour development
```

## 💾 Sauvegarde des Bases de Données

### Sauvegarde manuelle par environnement
```bash
# Sauvegarder l'environnement de développement
python data/scripts/backup_manager.py --env development --backup

# Sauvegarder l'environnement de test
python data/scripts/backup_manager.py --env test --backup

# Sauvegarder l'environnement de production
python data/scripts/backup_manager.py --env production --backup

# Sauvegarder tous les environnements
python data/scripts/backup_manager.py --all --backup
```

### Restauration d'une sauvegarde
```bash
# Restaurer une sauvegarde spécifique
python data/scripts/backup_manager.py --env development --restore --file backup_2024-01-15_14-30-00.db

# Restaurer la sauvegarde la plus récente
python data/scripts/backup_manager.py --env production --restore --latest
```

### Gestion des sauvegardes
```bash
# Lister toutes les sauvegardes disponibles
python data/scripts/backup_manager.py --list

# Lister les sauvegardes d'un environnement spécifique
python data/scripts/backup_manager.py --env development --list

# Nettoyer les anciennes sauvegardes (garde les 10 plus récentes)
python data/scripts/backup_manager.py --cleanup --keep 10
```

### Sauvegarde automatique
```bash
# Configurer une sauvegarde automatique quotidienne
python data/scripts/backup_manager.py --schedule --daily --env production

# Configurer une sauvegarde automatique hebdomadaire
python data/scripts/backup_manager.py --schedule --weekly --env all
```

### Emplacement des sauvegardes
- **Développement** : `data/backups/development/`
- **Test** : `data/backups/test/`
- **Production** : `data/backups/production/`

### Format des noms de fichiers
Les sauvegardes sont nommées avec le format :
```
backup_[ENVIRONNEMENT]_[DATE]_[HEURE].db
Exemple : backup_production_2024-01-15_14-30-00.db
```

## 🧪 Tests

```bash
# Exécuter tous les tests
python -m pytest tests/

# Tests unitaires uniquement
python -m pytest tests/unit/

# Avec couverture de code
python -m pytest tests/ --cov=src/gestia
```

## 📋 Fonctionnalités

### ✅ Gestion des Appareils
- Enregistrement d'appareils (marque, modèle, date de réception)
- Suivi des états (En Test, En Réparation, Reconditionné, En Vente, Irréparable)
- Historique complet des modifications

### ✅ Gestion des Techniciens
- Enregistrement des techniciens
- Attribution des sessions de test
- Suivi des diagnostics et réparations

### ✅ Sessions de Test
- Création de sessions de test
- Attribution d'appareils et techniciens
- Programmes de test configurables
- Critères de validation

### ✅ Diagnostics et Réparations
- Enregistrement des problèmes
- Suivi des actions de réparation
- Résultats de réparation

### ✅ Environnements Multiples
- **Développement** : Données de test, développement
- **Test** : Tests automatisés, validation
- **Production** : Données réelles, exploitation

## 🔧 Configuration

### Variables d'environnement
- `GESTIA_ENV` : Environnement actuel (development/test/production)

### Bases de données
- `data/development/gestia.db` : Base de développement
- `data/production/gestia.db` : Base de production
- `data/test/gestia.db` : Base de test

## 📊 Statistiques

Le système fournit des statistiques en temps réel :
- Nombre total d'appareils par état
- Répartition des techniciens
- Sessions de test en cours
- Diagnostics en cours

## 🔒 Sécurité

- Les bases de données ne sont jamais commitées dans Git
- Chaque environnement a sa propre base isolée
- Sauvegardes automatiques disponibles

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Consulter la documentation dans `docs/`
2. Vérifier les issues existantes
3. Créer une nouvelle issue avec les détails du problème

---

**GESTIA** - Simplifiez la gestion de vos appareils électroménagers ! 🏭✨ 

```
import sys
if sys.platform.startswith('win'):
    import os
    if os.environ.get('PYTHONIOENCODING') != 'utf-8':
        print("Veuillez lancer la console avec l'encodage UTF-8 (chcp 65001) ou définir PYTHONIOENCODING=utf-8")
        sys.exit(1) 