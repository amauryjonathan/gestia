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
- `data/gestia_dev.db` : Base de développement
- `data/gestia_test.db` : Base de test
- `data/gestia_prod.db` : Base de production

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