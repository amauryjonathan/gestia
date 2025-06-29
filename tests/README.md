# 🧪 Tests GESTIA

Ce dossier contient tous les tests du projet GESTIA.

## 📁 Structure

### `unit/`
Tests unitaires pour les composants individuels.
- `test_models.py` - Tests des modèles de données

### `integration/` (à créer)
Tests d'intégration pour les interactions entre composants.

### `e2e/` (à créer)
Tests end-to-end pour les scénarios complets.

## 🚀 Exécution des tests

```bash
# Tous les tests
python -m pytest tests/

# Tests unitaires uniquement
python -m pytest tests/unit/

# Tests avec couverture
python -m pytest tests/ --cov=src/gestia
```

## 📋 Ajout de nouveaux tests

1. Créer un fichier `test_*.py` dans le bon dossier
2. Importer les modules à tester
3. Écrire les tests avec pytest
4. Exécuter pour vérifier 