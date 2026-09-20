# LISEZ-MOI — Comment utiliser le portfolio

## Structure du projet

```
portfolio/
├── app.py              ← serveur (ne pas toucher)
├── requirements.txt    ← dépendances (ne pas toucher)
├── LISEZ-MOI.md
├── static/
│   └── animation.mp4  ← vidéo de fond du hero (optionnel)
├── templates/
│   ├── index.html
│   └── projet.html
└── projets/
    ├── 01_Carnet_de_Venise__Dessin/
    │   ├── cover.jpg
    │   ├── 01.jpg
    │   └── 02.jpg
    └── 02_Portrait__Encre/
        └── ...
```

---

## Ajouter un projet — 2 étapes

**1. Créer un dossier dans `projets/` avec ce format :**
```
ORDRE_TITRE_DU_PROJET__CATEGORIE
```
Exemples :
```
01_Carnet_de_Venise__Dessin
02_Portrait_au_Fusain__Encre
03_La_Foret_Bleue__Peinture
04_Creatures_Numeriques__Digital
```

**2. Y déposer les fichiers :**
```
cover.jpg     ← image de couverture (optionnel)
01.jpg        ← images dans l'ordre
02.jpg
03.pdf        ← les PDF s'ouvrent dans un onglet séparé
```

**C'est tout. Aucun code à modifier.**

---

## Catégories disponibles
- Dessin
- Encre
- Peinture
- Digital

---

## Personnaliser nom / liens sociaux

Ouvrir `app.py` et modifier le bloc CONFIG en haut du fichier :

```python
CONFIG = {
    'nom'        : 'Prénom Nom',
    'titre'      : 'Artiste & Illustrateur',
    'disciplines': 'Dessin · Peinture · Illustration',
    'email'      : 'contact@email.com',
    'instagram'  : 'https://instagram.com/toncompte',
    'behance'    : 'https://behance.net/toncompte',
    'linkedin'   : 'https://linkedin.com/in/toncompte',
}
```

---

## Vidéo de fond

Déposer `animation.mp4` dans `static/`.
Si absent → dégradé automatique, le site fonctionne quand même.

---

## Lancer en local

```bash
pip install flask
python app.py
```
→ Ouvrir `http://localhost:8080`

## Déployer sur Render

Start command : `gunicorn app:app`
