# NoteBlock ✨

**NoteBlock** est une application (en beta)de prise de notes de bureau moderne et esthétique, développée en Python avec la bibliothèque PyQt6. Elle offre une interface épurée, des thèmes personnalisables, et des fonctionnalités d'édition de texte riche, le tout sur un fond animé subtil pour une expérience utilisateur unique.

Ce projet a été développé par **Shushi**.

![Aperçu de NoteBlock en thème clair]
<img width="1920" height="1020" alt="white_note" src="https://github.com/user-attachments/assets/2ab480c8-35ef-4ca3-829c-0163bbd6f594" />

![Aperçu de NoteBlock en thème sombre]
<img width="1920" height="1020" alt="black_note" src="https://github.com/user-attachments/assets/5137e7aa-1912-49e9-90a2-3582ddb652d1" />

---

## 🚀 Fonctionnalités

- **Interface Moderne** : Un design inspiré des applications de productivité modernes comme Notion ou Gemini, avec des conteneurs "cartes" flottants et des ombres portées.
- **Thèmes Personnalisables** :
  - **Thème Clair** : Un look frais et apaisant avec des tons bleu pastel.
  - **Thème Sombre** : Un design élégant et concentré avec des gris profonds.
- **Fond Animé** : Des particules et des formes techniques (atomes, cubes, ADN) flottent doucement en arrière-plan.
- **Mode Statique** : Possibilité de désactiver l'animation pour une concentration maximale.
- **Éditeur de Texte Riche** :
  - **Formatage de base** : Gras, Italique, Souligné.
  - **Couleur du texte** : Choisissez n'importe quelle couleur.
  - **Listes Intelligentes** : Créez des listes à puces, numérotées, alphabétiques ou en chiffres romains.
  - **Tabulation** : Indentez et désindentez les listes avec `Tab` et `Shift+Tab`.
- **Gestion des Notes** :
  - **Base de Données SQLite** : Les notes sont stockées de manière sécurisée dans un fichier `notes.db`.
  - **Statut des Notes** : Marquez vos notes comme "En cours" ou "Terminé".
  - **CRUD complet** : Créez, lisez, mettez à jour et supprimez vos notes.
- **Sauvegarde Automatique** : Une option pour sauvegarder automatiquement votre travail toutes les 30 secondes.
- **Préférences Utilisateur** : L'application se souvient de votre thème préféré, de la taille et de la position de la fenêtre.

---

## 🛠️ Installation et Lancement

### Prérequis

- Python 3.x
- pip (généralement inclus avec Python)

### Étapes

1. **Clonez le dépôt (ou téléchargez les fichiers)**
   ```bash
   git clone https://github.com/Shushi/NoteBlock.git
   cd NoteBlock
   ```

2. **Créez un environnement virtuel (recommandé)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
   ```

3. **Installez les dépendances**
   Le fichier `requirements.txt` contient tout ce dont vous avez besoin.
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancez l'application**
   Exécutez le fichier `main.py` pour démarrer NoteBlock.
   ```bash
   python main.py
   ```

---

## 📂 Structure du Projet

```
NoteBlock/
├── Asset/
│   └── ICON/
│       ├── BLK_moon.png
│       ├── blk_setting.png
│       ├── left-arrow.png
│       ├── wht_setting.png
│       └── wht_sun.png
├── style/
│   └── theme.qss
├── ui/
│   ├── background.py
│   ├── content_container.py
│   ├── editor_widget.py
│   ├── mainwindow.py
│   └── toast.py
├── database.py
├── main.py
├── notes.db
├── README.md
└── requirements.txt
```

---

## 💡 Concepts Techniques

- **Framework** : PyQt6
- **Base de Données** : SQLite 3
- **Dessin et Animation** : `QPainter` pour le fond animé.
- **Styling** : QSS (Qt Style Sheets) pour un design personnalisé.
- **Persistance** : `QSettings` pour sauvegarder les préférences utilisateur.

---

*Projet réalisé par Shushi.*
