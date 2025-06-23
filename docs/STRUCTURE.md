# Structure du Projet GESTIA

## 📁 Organisation des dossiers

```
gestia/
├── src/
│   └── gestia/
│       ├── __init__.py          # Package principal
│       ├── core/                # Logique métier
│       │   ├── __init__.py
│       │   ├── models.py        # Modèles SQLAlchemy
│       │   ├── database.py      # Gestion de la base de données
│       │   └── services.py      # Services métier
│       ├── ui/                  # Interfaces utilisateur
│       │   ├── __init__.py
│       │   ├── console.py       # Interface console
│       │   └── gui.py          # Interface graphique Tkinter
│       └── utils/               # Utilitaires
│           ├── __init__.py
│           └── demo.py          # Scripts de démonstration
├── tests/                       # Tests unitaires
│   ├── __init__.py
│   └── test_models.py
├── docs/                        # Documentation
│   └── STRUCTURE.md
├── scripts/                     # Scripts utilitaires
│   └── gui_launcher.py
├── main.py                      # Point d'entrée principal
├── setup.py                     # Configuration d'installation
├── pyproject.toml              # Configuration moderne du projet
├── requirements.txt             # Dépendances
├── README.md                    # Documentation principale
└── .gitignore                   # Fichiers à ignorer
```

## 🏗️ Architecture

### Package `core`
Contient la logique métier et la gestion des données :

- **`models.py`** : Définition des classes SQLAlchemy et énumérations
- **`database.py`** : Configuration et gestion de la base de données
- **`services.py`** : Services métier avec opérations CRUD

### Package `ui`
Contient les interfaces utilisateur :

- **`console.py`** : Interface console interactive
- **`gui.py`** : Interface graphique avec Tkinter

### Package `utils`
Contient les utilitaires et scripts :

- **`demo.py`** : Scripts de démonstration et données d'exemple

## 🚀 Points d'entrée

### `main.py`
Point d'entrée principal avec choix d'interface :
- Interface graphique
- Interface console
- Démonstration automatique

### `scripts/gui_launcher.py`
Lanceur direct de l'interface graphique pour :
- Développement rapide
- Tests de l'interface graphique
- Raccourcis utilisateur

## 📦 Installation et développement

### Installation en mode développement
```bash
pip install -e .
```

### Installation des dépendances de développement
```bash
pip install -e ".[dev]"
```

### Lancement des tests
```bash
pytest
```

### Formatage du code
```bash
black src/ tests/
```

## 🔧 Configuration

### Base de données
La base de données SQLite est créée automatiquement dans le répertoire racine.

### Variables d'environnement
Aucune variable d'environnement requise pour le moment.

## 📝 Conventions

### Imports
- Utiliser des imports relatifs dans les packages
- Imports absolus depuis la racine du projet

### Nommage
- Classes : PascalCase
- Fonctions et variables : snake_case
- Constantes : UPPER_SNAKE_CASE

### Documentation
- Docstrings en français
- Type hints pour toutes les fonctions
- Commentaires pour la logique complexe 