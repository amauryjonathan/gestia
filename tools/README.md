# 🛠️ Outils GESTIA

Ce dossier contient tous les outils et scripts utilitaires pour le projet GESTIA.

## 📁 Contenu

### `manage_env.py`
Script principal pour gérer les environnements (développement, test, production).
- Changer d'environnement
- Initialiser les bases de données
- Générer des données de test
- Lancer l'application

### `explore_db.py`
Outil pour explorer et analyser la base de données.
- Afficher la structure des tables
- Lister les données
- Vérifier l'intégrité

### `gui_launcher.py`
Lanceur alternatif pour l'interface graphique.

## 🚀 Utilisation

```bash
# Gérer les environnements
python tools/manage_env.py status
python tools/manage_env.py switch --env production

# Explorer la base de données
python tools/explore_db.py

# Lancer l'interface graphique
python tools/gui_launcher.py
``` 