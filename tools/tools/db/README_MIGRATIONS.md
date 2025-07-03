# 🚀 Guide des Migrations de Base de Données GESTIA

## 📋 **Vue d'ensemble**

Ce système de migrations vous permet de gérer les modifications de schéma de base de données de manière professionnelle et sécurisée.

## 🎯 **Avantages du système**

✅ **Versioning automatique** - Chaque migration a un numéro unique  
✅ **Suivi des migrations appliquées** - Évite les doublons  
✅ **Exécution sélective** - Seules les nouvelles migrations sont appliquées  
✅ **Rollback possible** - Possibilité de revenir en arrière  
✅ **Environnements multiples** - Development, test, production  
✅ **Création automatisée** - Scripts pour créer facilement de nouvelles migrations  

## 🛠️ **Commandes principales**

### **1. Vérifier le statut des migrations**
```bash
python tools/tools/db/migrate_db.py status --env development
```

### **2. Appliquer les migrations**
```bash
python tools/tools/db/migrate_db.py migrate --env development
```

### **3. Créer une nouvelle migration**
```bash
python tools/tools/db/create_migration.py \
  --name "add_user_table" \
  --description "Ajout de la table utilisateurs" \
  --sql "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)" \
  --sql "CREATE INDEX idx_users_name ON users(name)"
```

## 📝 **Comment ajouter un nouvel attribut à la base de données**

### **Méthode 1 : Utilisation du script automatique (Recommandée)**

```bash
# Exemple : Ajouter une colonne "Prix" à la table appareils
python tools/tools/db/create_migration.py \
  --name "add_price_field" \
  --description "Ajout du champ Prix pour la gestion des coûts" \
  --sql "ALTER TABLE appareils ADD COLUMN Prix REAL"
```

### **Méthode 2 : Ajout manuel**

1. **Ouvrir le fichier** `tools/tools/db/migrate_db.py`
2. **Trouver la méthode** `get_all_migrations()`
3. **Ajouter une nouvelle migration** à la fin de la liste :

```python
{
    'version': '004_add_price_field',
    'description': 'Ajout du champ Prix pour la gestion des coûts',
    'sql': [
        'ALTER TABLE appareils ADD COLUMN Prix REAL'
    ]
}
```

### **Méthode 3 : Prévisualisation avant ajout**

```bash
python tools/tools/db/create_migration.py \
  --name "add_price_field" \
  --description "Ajout du champ Prix pour la gestion des coûts" \
  --sql "ALTER TABLE appareils ADD COLUMN Prix REAL" \
  --preview
```

## 🔄 **Workflow recommandé**

### **Pour chaque modification de base de données :**

1. **Créer la migration**
   ```bash
   python tools/tools/db/create_migration.py --name "nom_migration" --description "..." --sql "..."
   ```

2. **Vérifier le statut**
   ```bash
   python tools/tools/db/migrate_db.py status --env development
   ```

3. **Appliquer la migration**
   ```bash
   python tools/tools/db/migrate_db.py migrate --env development
   ```

4. **Tester l'application**
   ```bash
   python src/main.py
   ```

## 📊 **Migrations existantes**

| Version | Description | Colonnes ajoutées |
|---------|-------------|-------------------|
| 001 | Champs Samsung | Serie, Capacite, Technologie, Variante, ReferenceComplete |
| 002 | Champ Label | Label |
| 003 | Champs Tests/Diagnostics | ActionsAFaire, SoucisMachine |

## ⚠️ **Bonnes pratiques**

### **✅ À faire :**
- **Toujours créer une migration** pour chaque modification de schéma
- **Tester sur development** avant production
- **Faire des sauvegardes** avant les migrations importantes
- **Utiliser des descriptions claires** pour chaque migration
- **Numéroter les versions** de manière séquentielle

### **❌ À éviter :**
- **Modifier directement la base** sans migration
- **Supprimer des migrations** déjà appliquées
- **Modifier les migrations** existantes
- **Oublier de tester** avant production

## 🔧 **Commandes avancées**

### **Créer une migration avec version manuelle**
```bash
python tools/tools/db/create_migration.py \
  --version "005" \
  --name "add_complex_table" \
  --description "Ajout d'une table complexe avec contraintes" \
  --sql "CREATE TABLE complex_table (id INTEGER PRIMARY KEY)" \
  --sql "ALTER TABLE complex_table ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
```

### **Vérifier le statut sur tous les environnements**
```bash
python tools/tools/db/migrate_db.py status --env development
python tools/tools/db/migrate_db.py status --env test
python tools/tools/db/migrate_db.py status --env production
```

## 🚨 **Résolution de problèmes**

### **Erreur : "Migration déjà appliquée"**
- Normal, la migration a déjà été exécutée
- Vérifiez avec `status` pour confirmer

### **Erreur : "Base de données verrouillée"**
- Fermez l'application GESTIA
- Vérifiez qu'aucun autre processus n'utilise la base

### **Erreur : "Colonne existe déjà"**
- La migration a déjà été appliquée partiellement
- Vérifiez le statut avec `status`

## 📚 **Exemples concrets**

### **Exemple 1 : Ajouter un champ simple**
```bash
python tools/tools/db/create_migration.py \
  --name "add_notes_field" \
  --description "Ajout du champ Notes pour les commentaires" \
  --sql "ALTER TABLE appareils ADD COLUMN Notes TEXT"
```

### **Exemple 2 : Ajouter une table complète**
```bash
python tools/tools/db/create_migration.py \
  --name "add_maintenance_table" \
  --description "Ajout de la table de maintenance" \
  --sql "CREATE TABLE maintenance (id INTEGER PRIMARY KEY, appareil_id INTEGER, date TEXT, description TEXT)" \
  --sql "CREATE INDEX idx_maintenance_appareil ON maintenance(appareil_id)"
```

### **Exemple 3 : Modifier une contrainte**
```bash
python tools/tools/db/create_migration.py \
  --name "add_unique_constraint" \
  --description "Ajout d'une contrainte unique sur le numéro de série" \
  --sql "CREATE UNIQUE INDEX idx_appareils_serie ON appareils(Serie)"
```

## 🎉 **Conclusion**

Avec ce système, vous n'avez plus besoin de créer un script séparé pour chaque modification ! Le système gère automatiquement :
- Le versioning des migrations
- L'application sélective
- Le suivi des modifications
- La compatibilité entre environnements

**Plus jamais de problème de schéma de base de données !** 🚀 