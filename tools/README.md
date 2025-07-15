1# 🛠️ Outils GESTIA

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

### `test_dropdown.py`
Script de test pour la fonctionnalité dropdown des marques.
- Teste la récupération des marques existantes
- Vérifie la création d'appareils avec marques existantes/nouvelles
- Valide la mise à jour de la liste des marques

### `test_tri.py`
Script de test pour la fonctionnalité de tri des colonnes.
- Teste le tri par marque, état, date de réception
- Vérifie que les données sont correctement ordonnées
- Documente l'utilisation de la fonctionnalité de tri

## 🚀 Utilisation

```bash
# Gérer les environnements
python tools/manage_env.py status
python tools/manage_env.py switch --env production

# Explorer la base de données
python tools/explore_db.py

# Lancer l'interface graphique
python tools/gui_launcher.py

# Tester le dropdown des marques
python tools/test_dropdown.py

# Tester la fonctionnalité de tri
python tools/test_tri.py
```

## 🆕 Nouvelles fonctionnalités

### Dropdown des marques
Le formulaire de création d'appareil inclut maintenant un **dropdown des marques** qui :

✅ **Affiche toutes les marques existantes** dans la base de données  
✅ **Permet de sélectionner une marque existante** pour éviter les doublons  
✅ **Offre l'option "Nouvelle marque"** pour ajouter de nouvelles marques  
✅ **Valide les données** avant la création  
✅ **Interface intuitive** avec explications visuelles  

### Tri des colonnes
Les listes d'appareils et de techniciens incluent maintenant un **tri interactif** :

✅ **Double-clic sur les en-têtes** pour trier par colonne  
✅ **Indicateurs visuels** (↑/↓) pour l'ordre de tri  
✅ **Tri inversé** en double-cliquant à nouveau  
✅ **Tri par toutes les colonnes** (ID, Marque, Modèle, Date, État, etc.)  
✅ **Interface professionnelle** et intuitive  

### Utilisation du tri :
1. **Double-cliquez** sur l'en-tête d'une colonne pour trier
2. **Les flèches ↑/↓** indiquent l'ordre de tri actuel
3. **Double-cliquez à nouveau** pour inverser l'ordre
4. **Changez de colonne** pour trier par un autre critère

### Utilisation dans l'interface :
1. Cliquer sur "➕ Nouvel Appareil"
2. Dans le dropdown "Marque", choisir :
   - Une marque existante (recommandé)
   - "--- Nouvelle marque ---" pour saisir une nouvelle marque
3. Remplir le modèle et la date
4. Cliquer sur "Créer" 