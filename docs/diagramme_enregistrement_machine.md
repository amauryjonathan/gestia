# Diagrammes UML pour l'Enregistrement d'une Machine - GESTIA

## 🎯 **1. Diagramme de Classes (Recommandé)**

### **Objectif** : Montrer la structure des données et les relations

```
┌─────────────────────────────────────────────────────────────┐
│                        Appareil                             │
├─────────────────────────────────────────────────────────────┤
│ - ID_Appareil: String (PK)                                  │
│ - Marque: String (100) [OBLIGATOIRE]                        │
│ - Modele: String (100) [OBLIGATOIRE]                        │
│ - DateReception: Date [OBLIGATOIRE]                         │
│ - Etat: EtatAppareil [OBLIGATOIRE]                          │
│ - DateMiseEnVente: Date [OPTIONNEL]                         │
├─────────────────────────────────────────────────────────────┤
│ + creer_appareil(marque, modele, date_reception)            │
│ + obtenir_appareil(id_appareil)                             │
│ + lister_appareils()                                        │
│ + modifier_etat_appareil(id, nouvel_etat)                   │
├─────────────────────────────────────────────────────────────┤
│                    Relations                                │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ SessionDeTest   │    │ Diagnostic      │                │
│  │ (1..*)          │    │ Reparation      │                │
│  └─────────────────┘    │ (0..*)          │                │
│                         └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    EtatAppareil                             │
├─────────────────────────────────────────────────────────────┤
│ EN_TEST = "En Test"                                         │
│ EN_REPARATION = "En Réparation"                             │
│ RECONDITIONNE = "Reconditionné"                             │
│ EN_VENTE = "En Vente"                                       │
│ IRREPARABLE = "Irréparable"                                 │
└─────────────────────────────────────────────────────────────┘
```

### **Avantages** :
- ✅ Montre tous les champs requis
- ✅ Indique les contraintes (obligatoire/optionnel)
- ✅ Affiche les relations avec d'autres entités
- ✅ Inclut les méthodes de service

---

## 🔄 **2. Diagramme de Séquence**

### **Objectif** : Montrer le processus d'enregistrement étape par étape

```
Utilisateur    Interface    AppareilService    BaseDeDonnées
     │             │              │                │
     │ 1. Saisir   │              │                │
     │   données   │              │                │
     │─────────────│              │                │
     │             │ 2. Valider   │                │
     │             │   données    │                │
     │             │──────────────│                │
     │             │              │ 3. Créer       │
     │             │              │   appareil     │
     │             │              │───────────────│
     │             │              │                │ 4. Sauvegarder
     │             │              │                │───────────────│
     │             │              │ 5. Retourner   │                │
     │             │              │   ID           │                │
     │             │ 6. Afficher  │                │                │
     │             │   succès     │                │                │
     │ 7. Confirmer│              │                │                │
```

### **Avantages** :
- ✅ Montre l'ordre des opérations
- ✅ Identifie les acteurs impliqués
- ✅ Détaille les interactions
- ✅ Facilite la compréhension du processus

---

## 📋 **3. Diagramme d'Activité**

### **Objectif** : Montrer le flux de travail d'enregistrement

```
[Début] → [Saisir Marque] → [Saisir Modèle] → [Saisir Date Réception]
    ↓
[Validation des données] → {Données valides?}
    ↓ Non
[Erreur] → [Corriger] → [Retour saisie]
    ↓ Oui
[Générer ID unique] → [Créer enregistrement] → [Sauvegarder en DB]
    ↓
[État = "EN_TEST"] → [Confirmer création] → [Fin]
```

### **Avantages** :
- ✅ Montre les décisions et conditions
- ✅ Affiche les boucles de correction
- ✅ Détaille les étapes de validation
- ✅ Facilite l'identification des points de contrôle

---

## 🎨 **4. Diagramme de Cas d'Usage**

### **Objectif** : Montrer les fonctionnalités disponibles

```
┌─────────────────────────────────────────────────────────────┐
│                    Système GESTIA                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Technicien  │    │ Administra- │    │ Superviseur │     │
│  │             │    │ teur        │    │             │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │           │
│         │                   │                   │           │
│  ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐     │
│  │ Enregistrer │    │ Enregistrer │    │ Enregistrer │     │
│  │ Machine     │    │ Machine     │    │ Machine     │     │
│  │ (Basique)   │    │ (Complet)   │    │ (Avancé)    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Consulter   │    │ Modifier    │    │ Lister      │     │
│  │ Machine     │    │ État        │    │ Machines    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Avantages** :
- ✅ Montre les acteurs et leurs rôles
- ✅ Identifie les fonctionnalités disponibles
- ✅ Clarifie les permissions
- ✅ Facilite la gestion des droits

---

## 🏗️ **5. Diagramme d'État-Transition**

### **Objectif** : Montrer les états possibles d'une machine

```
[EN_TEST] ←─── [Nouvelle Machine]
    │
    ├─── Test réussi ───→ [RECONDITIONNE]
    │
    ├─── Test échoué ───→ [EN_REPARATION]
    │
    └─── Problème majeur ───→ [IRREPARABLE]

[EN_REPARATION] ←─── [Réparation nécessaire]
    │
    ├─── Réparation réussie ───→ [RECONDITIONNE]
    │
    └─── Réparation échouée ───→ [IRREPARABLE]

[RECONDITIONNE] ←─── [Machine prête]
    │
    └─── Mise en vente ───→ [EN_VENTE]

[EN_VENTE] ←─── [Disponible à la vente]
    │
    └─── Vendu ───→ [SUPPRIMÉ de la base]
```

### **Avantages** :
- ✅ Montre le cycle de vie complet
- ✅ Identifie les transitions possibles
- ✅ Clarifie les conditions de changement d'état
- ✅ Facilite la gestion des workflows

---

## 🎯 **Recommandation selon votre besoin**

### **Si vous voulez montrer :**
- **Structure des données** → **Diagramme de Classes**
- **Processus d'enregistrement** → **Diagramme de Séquence**
- **Workflow complet** → **Diagramme d'Activité**
- **Fonctionnalités disponibles** → **Diagramme de Cas d'Usage**
- **États de la machine** → **Diagramme d'État-Transition**

### **Pour l'enregistrement d'une machine, je recommande :**
1. **Diagramme de Classes** (structure des données)
2. **Diagramme de Séquence** (processus d'enregistrement)
3. **Diagramme d'Activité** (workflow complet)

Ces trois diagrammes couvrent tous les aspects de l'enregistrement d'une machine dans GESTIA. 