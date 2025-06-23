# GESTIA - Système de Gestion d'Appareils

## 📋 Description

GESTIA est un système complet de gestion d'appareils avec tests, diagnostics et réparations. Le système est basé sur un diagramme de classe UML et implémente toutes les relations et fonctionnalités décrites.

## 🏗️ Architecture

Le système est composé de plusieurs modules :

- **`models.py`** : Définition des classes et relations (SQLAlchemy ORM)
- **`database.py`** : Gestion de la base de données
- **`services.py`** : Logique métier et opérations CRUD
- **`interface.py`** : Interface console interactive
- **`gui.py`** : Interface graphique avec Tkinter
- **`main.py`** : Point d'entrée principal avec choix d'interface
- **`gui_launcher.py`** : Lanceur direct de l'interface graphique

## 🗄️ Modèle de données

### Classes principales :
- **Appareil** : Gestion du cycle de vie des appareils
- **Technicien** : Personnel technique
- **SessionDeTest** : Sessions de test sur les appareils
- **ProgrammeDeTest** : Programmes de test (Rapide, Coton 90, Essorage)
- **CritereDeTest** : Critères de validation des tests
- **DiagnosticReparation** : Diagnostics et réparations

### Relations :
- Un appareil peut avoir plusieurs sessions de test
- Une session de test appartient à un appareil et un technicien
- Une session contient plusieurs programmes de test
- Un programme contient plusieurs critères
- Un technicien peut valider des critères et effectuer des diagnostics

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Tkinter (inclus avec Python sur la plupart des systèmes)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <url-du-repo>
   cd gestia
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Lancement de l'application

### Option 1 : Lanceur principal (recommandé)
```bash
python main.py
```
Puis choisissez :
- **1** : Interface Graphique (Tkinter)
- **2** : Interface Console
- **3** : Démonstration automatique

### Option 2 : Interface graphique directe
```bash
python gui_launcher.py
```

### Option 3 : Interface console directe
```bash
python interface.py
```

### Option 4 : Démonstration
```bash
python demo.py
```

## 🖼️ Interface Graphique

L'interface graphique offre une expérience utilisateur moderne avec :

### Fonctionnalités disponibles :
- **Tableau de bord** : Vue d'ensemble avec statistiques
- **Gestion des appareils** : Création, consultation, modification d'état
- **Gestion des techniciens** : Création et consultation
- **Navigation intuitive** : Menu latéral avec icônes

### Fonctionnalités en développement :
- Sessions de test
- Programmes de test
- Critères de test
- Diagnostics et réparations
- Statistiques détaillées

### Utilisation de l'interface graphique :
1. **Créer un appareil** : Cliquez sur "➕ Nouvel Appareil"
2. **Consulter un appareil** : Double-cliquez sur un appareil dans la liste
3. **Modifier l'état** : Dans les détails d'un appareil, cliquez sur "Modifier l'état"
4. **Actualiser** : Cliquez sur "🔄 Actualiser" pour mettre à jour les données

## 📖 Interface Console

L'interface console propose 7 options principales :

1. **Gestion des Appareils**
   - Créer un nouvel appareil
   - Lister tous les appareils
   - Consulter un appareil
   - Modifier l'état d'un appareil

2. **Gestion des Techniciens**
   - Créer un nouveau technicien
   - Lister tous les techniciens
   - Consulter un technicien

3. **Sessions de Test**
   - Créer une nouvelle session
   - Consulter une session
   - Terminer une session

4. **Programmes de Test**
   - Créer un programme
   - Lancer un programme
   - Terminer un programme

5. **Critères de Test**
   - Créer un critère
   - Valider un critère

6. **Diagnostics et Réparations**
   - Créer un diagnostic
   - Terminer un diagnostic

7. **Rapports et Statistiques**
   - Afficher les statistiques générales

### Workflow typique

1. **Créer un technicien** (option 2 → 1)
2. **Créer un appareil** (option 1 → 1)
3. **Créer une session de test** (option 3 → 1)
4. **Ajouter des programmes de test** (option 4 → 1)
5. **Créer et valider des critères** (option 5)
6. **Effectuer des diagnostics si nécessaire** (option 6)
7. **Terminer la session** (option 3 → 3)

## 🗃️ Base de données

Le système utilise SQLite par défaut (fichier `gestia.db`). La base de données est créée automatiquement au premier lancement.

### Structure des tables :
- `appareils` : Informations sur les appareils
- `techniciens` : Informations sur les techniciens
- `sessions_de_test` : Sessions de test
- `programmes_de_test` : Programmes de test
- `criteres_de_test` : Critères de validation
- `diagnostics_reparation` : Diagnostics et réparations

## 🔧 Configuration

### Changer la base de données
Modifiez la ligne dans `database.py` :
```python
db_manager = DatabaseManager("sqlite:///votre_fichier.db")
```

### Utiliser PostgreSQL
```python
db_manager = DatabaseManager("postgresql://user:password@localhost/gestia")
```

## 📊 Fonctionnalités avancées

### États des appareils
- **En Test** : Appareil en cours de test
- **En Réparation** : Appareil en réparation
- **Reconditionné** : Appareil réparé et prêt
- **En Vente** : Appareil disponible à la vente
- **Irréparable** : Appareil non réparable

### Programmes de test
- **Rapide** : Test rapide
- **Coton 90** : Test complet coton 90°
- **Essorage** : Test d'essorage

### Critères de test
- Verrouillage Porte
- Vidange
- Remplissage
- Rotation
- Chauffe
- Essorage
- Programme Terminé

## 🐛 Dépannage

### Erreur de base de données
- Vérifiez les permissions d'écriture dans le répertoire
- Supprimez le fichier `gestia.db` pour recréer la base

### Erreur d'importation
- Vérifiez que toutes les dépendances sont installées
- Activez l'environnement virtuel

### Erreur Tkinter
- Sur Linux : `sudo apt-get install python3-tk`
- Sur macOS : Tkinter est généralement inclus
- Sur Windows : Tkinter est inclus avec Python

### Interface graphique ne se lance pas
- Vérifiez que Tkinter est installé
- Utilisez l'interface console en attendant
- Vérifiez les logs d'erreur

## 📝 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités
- Améliorer l'interface graphique

## 🚀 Roadmap

### Prochaines fonctionnalités :
- [ ] Interface complète pour les sessions de test
- [ ] Interface pour les programmes de test
- [ ] Interface pour les critères de test
- [ ] Interface pour les diagnostics
- [ ] Graphiques et statistiques avancées
- [ ] Export de données (PDF, Excel)
- [ ] Système de notifications
- [ ] Interface web (Flask/FastAPI)

---

**Développé avec ❤️ pour la gestion d'appareils** 