# 🏋️‍♂️ FITNESS PRO 

Une application moderne de fitness avec une interface utilisateur élégante et intuitive, développée en Python avec CustomTkinter.

## ✨ Fonctionnalités

### Interface Principale
- Design moderne avec thème sombre
- Animation du logo dynamique
- Barre latérale personnalisée avec profil utilisateur
- Navigation fluide entre les différentes sections

### 👤 Profil Utilisateur
- Affichage des informations personnelles (nom, âge, poids)
- Avatar personnalisé avec initiales
- Modification des informations dans les paramètres
- Sauvegarde automatique des données

### 🏋️‍♂️ Programmes d'Entraînement
- Liste scrollable des programmes disponibles
- Différentes durées d'entraînement (15s, 30s, 60s)
- Calcul automatique des calories brûlées
- Interface d'entraînement avec timer animé
- Animation des cercles pendant l'entraînement

### 📊 Statistiques
- Suivi des entraînements totaux
- Compteur de calories brûlées
- Suivi des séries d'entraînement
- Historique des performances
- Affichage des records personnels

### ⚙️ Paramètres
- Gestion du profil utilisateur
- Gestion des programmes d'entraînement
  - Ajout de nouveaux programmes
  - Modification des programmes existants
  - Suppression des programmes
- Interface intuitive avec onglets

## 🛠️ Installation

1. Cloner le repository :
```bash
git clone https://github.com/votre-username/fitness-pro.git
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer l'application :
```bash
python fitness_app.py
```

## 📦 Dépendances

- Python 3.x
- CustomTkinter
- Pillow (PIL)
- JSON (intégré à Python)

## 📁 Structure des Fichiers

```
fitness_pro/
├── fitness_app.py          # Application principale
├── data/
│   ├── settings.json       # Paramètres utilisateur
│   ├── progress.json       # Données de progression
│   └── workout_programs.json # Programmes d'entraînement
├── README.md
└── requirements.txt
```

## 🎨 Personnalisation

L'application utilise un thème de couleurs moderne et personnalisable :
- `primary`: Vert néon (#00ff88)
- `secondary`: Rose néon (#ff3366)
- `accent`: Bleu néon (#00ccff)
- `background`: Noir profond (#111111)
- `card`: Gris foncé (#1a1a1a)
- `text`: Blanc (#ffffff)

## 🔄 Fonctionnalités à Venir

- [ ] Support multi-langues
- [ ] Exportation des statistiques
- [ ] Partage social des performances
- [ ] Mode clair/sombre
- [ ] Synchronisation cloud

## 👨‍💻 Développé par

Made by Achraf