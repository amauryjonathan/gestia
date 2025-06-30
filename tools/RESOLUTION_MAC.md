# 🔧 Résolution du problème de migration sur Mac

## 🚨 **Erreur rencontrée :**
```
(sqlite3.OperationalError) no such column: appareils.Serie
```

## 📋 **Explication du problème :**

Votre base de données SQLite sur Mac ne contient pas les nouvelles colonnes ajoutées pour les références Samsung :
- `Serie`
- `Capacite` 
- `Technologie`
- `Variante`
- `ReferenceComplete`

## ✅ **Solutions disponibles :**

### **Option 1 : Migration automatique (Recommandée)**
```bash
# Vérifier le statut actuel
python tools/manage_env.py migrate-status --env development

# Appliquer les migrations
python tools/manage_env.py migrate --env development

# Vérifier que tout fonctionne
python tools/manage_env.py status
```

### **Option 2 : Réinitialisation complète**
```bash
# Réinitialiser complètement l'environnement (⚠️ Supprime toutes les données)
python tools/manage_env.py reset --env development --force

# Ou utiliser le script dédié
python tools/init_db.py --env development --force
```

### **Option 3 : Migration manuelle**
```bash
# Utiliser directement le script de migration
python tools/migrate_db.py migrate --env development
```

## 🎯 **Recommandation pour votre cas :**

Puisque vous êtes en développement et que l'erreur indique que les colonnes n'existent pas, je recommande :

1. **Vérifier d'abord le statut :**
   ```bash
   python tools/manage_env.py migrate-status --env development
   ```

2. **Si aucune migration n'est appliquée, faire une migration :**
   ```bash
   python tools/manage_env.py migrate --env development
   ```

3. **Si cela ne fonctionne pas, réinitialiser :**
   ```bash
   python tools/manage_env.py reset --env development --force
   ```

## 🔄 **Pour éviter ce problème à l'avenir :**

### **Workflow recommandé :**
1. **Avant de commencer à travailler :**
   ```bash
   python tools/manage_env.py migrate --env development
   ```

2. **Après avoir récupéré des changements Git :**
   ```bash
   python tools/manage_env.py migrate --env development
   ```

3. **Si vous changez d'environnement :**
   ```bash
   python tools/manage_env.py switch --env development
   python tools/manage_env.py migrate --env development
   ```

## 📊 **Vérification du succès :**

Après la migration, vous devriez voir :
```bash
python tools/manage_env.py status
```

Et l'application devrait fonctionner sans erreur :
```bash
python main.py
```

## 🆘 **En cas de problème persistant :**

1. **Vérifier la structure de la base :**
   ```bash
   python tools/explore_db.py
   ```

2. **Consulter les logs de migration :**
   ```bash
   python tools/migrate_db.py status --env development
   ```

3. **Réinitialiser complètement :**
   ```bash
   python tools/init_db.py --env development --force
   ```

## 💡 **Pourquoi ce système est meilleur :**

✅ **Migrations versionnées** - Chaque changement de schéma est tracé  
✅ **Réversible** - Possibilité de revenir en arrière  
✅ **Multi-environnements** - Chaque environnement peut être migré indépendamment  
✅ **Sécurisé** - Pas de perte de données accidentelle  
✅ **Collaboratif** - Tous les développeurs peuvent synchroniser leur base  

---

**🎉 Avec ce système, vous n'aurez plus jamais ce problème de synchronisation de base de données !** 