from flask import Flask, render_template, send_from_directory, abort
import os, re

app = Flask(__name__)

PROJETS_DIR = os.path.dirname(__file__)
EXCLUDE_DIRS = {'static', 'templates', '.git', '.github', '__pycache__', '10_Master'}
IMG_EXT     = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALL_EXT     = IMG_EXT | {'.pdf'}

# ── À personnaliser ────────────────────────────────────────────────────────
CONFIG = {
    'nom'        : 'Gabriel Spartalioglou',
    'titre'      : 'Étudiant en architecture · ENSAPB',
    'disciplines': 'Réhabilitation · Réemploi · Participation',
    'email'      : 'contact@email.com',
    'instagram'  : 'https://instagram.com/toncompte',
    'behance'    : 'https://behance.net/toncompte',
    'linkedin'   : 'https://linkedin.com/in/toncompte',

    # Texte affiché dans la section "À propos" — issu de l'avant-propos
    # du portfolio.
    'bio': "Mon parcours en architecture s'est construit autour d'une "
           "conviction : bâtir aujourd'hui ne peut plus se penser en dehors "
           "de ce qui existe déjà — les sols, les structures, les usages, "
           "les communautés. Les studios que j'ai choisi de suivre "
           "traduisent cette conviction et la prolongent, projet après "
           "projet, vers une pratique de la réhabilitation, du réemploi "
           "et de la participation.",

    # Les trois piliers de la démarche, affichés dans la section "Approche" —
    # reprennent directement l'avant-propos du portfolio.
    'approche': [
        {
            'titre'      : 'Réhabilitation',
            'description': "Composer avec l'existant — un site, une "
                            "mémoire, une communauté — plutôt que "
                            "d'imposer une forme close et définitive.",
        },
        {
            'titre'      : 'Réemploi',
            'description': 'Partir des matériaux, des structures et des '
                            'ressources déjà là pour construire la suite.',
        },
        {
            'titre'      : 'Participation',
            'description': "Associer les usagers et les communautés "
                            "concernées à la fabrication du projet, à "
                            "chaque échelle.",
        },
    ],

    # Parcours affiché dans la section du même nom — formation, mobilité,
    # expérience professionnelle.
    'parcours': [
        {
            'periode'    : 'L1 → M2',
            'titre'      : 'Formation en architecture',
            'lieu'       : 'ENSAPB',
            'description': "Du matériau à l'espace jusqu'au projet de fin "
                            "d'études, en passant par sept studios "
                            "successifs.",
        },
        {
            'periode'    : 'Semestres 7-8',
            'titre'      : 'Erasmus — Laboratorio di Restauro',
            'lieu'       : 'Università La Sapienza, Rome',
            'description': 'Une année consacrée à la restauration du '
                            'patrimoine, au Ninfeo di Bramante à '
                            'Genazzano.',
        },
        {
            'periode'    : 'Juin 2023',
            'titre'      : 'Stage — ANIS Architecture',
            'lieu'       : 'Jérôme Durand, architecte du patrimoine',
            'description': "Relevés d'état des lieux et suivi de chantier "
                            "à Aix-en-Provence.",
        },
    ],
}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def lire_projets():
    """
    Lit le dossier projets/ et reconstruit automatiquement la liste.
    Format dossier : ORDRE_TITRE__CATEGORIE
    Exemple        : 01_Carnet_de_Venise__Dessin
    """
    if not os.path.exists(PROJETS_DIR):
        return []
    projets = []
    for dossier in sorted(os.listdir(PROJETS_DIR)):
        if dossier in EXCLUDE_DIRS or dossier.startswith('.'):
            continue
        chemin = os.path.join(PROJETS_DIR, dossier)
        if not os.path.isdir(chemin):
            continue

        base, categorie = dossier, 'Architecture'
        if '__' in base:
            base, cat = base.rsplit('__', 1)
            categorie = cat.replace('_', ' ').strip()

        parts = base.split('_', 1)
        ordre = int(parts[0]) if len(parts) == 2 and parts[0].isdigit() else 99
        titre = (parts[1] if len(parts) == 2 else base).replace('_', ' ').strip()

        fichiers = sorted([
            f for f in os.listdir(chemin)
            if os.path.splitext(f)[1].lower() in ALL_EXT
            and f.lower() not in ('cover.jpg', 'cover.jpeg', 'cover.png')
        ])

        couverture = next(
            (e for e in ['cover.jpg', 'cover.jpeg', 'cover.png']
             if os.path.exists(os.path.join(chemin, e))),
            next((f for f in fichiers
                  if os.path.splitext(f)[1].lower() in IMG_EXT), None)
        )

        projets.append({
            'titre'    : titre,
            'categorie': categorie,
            'ordre'    : ordre,
            'dossier'  : dossier,
            'slug'     : slug(titre),
            'couverture': couverture,
            'images'   : [f for f in fichiers
                          if os.path.splitext(f)[1].lower() in IMG_EXT],
            'pdfs'     : [f for f in fichiers
                          if os.path.splitext(f)[1].lower() == '.pdf'],
            'nb'       : len(fichiers),
        })

    projets.sort(key=lambda p: p['ordre'])
    return projets


@app.route('/')
def home():
    projets = lire_projets()
    cats = ['Tous'] + sorted({p['categorie'] for p in projets})
    return render_template('index.html',
                           projets=projets, categories=cats, cfg=CONFIG)


@app.route('/projet/<projet_slug>')
def projet(projet_slug):
    projets = lire_projets()
    p = next((x for x in projets if x['slug'] == projet_slug), None)
    if p is None:
        abort(404)
    return render_template('projet.html',
                           projet=p, projets=projets, cfg=CONFIG)


@app.route('/projets/<dossier>/<filename>')
def fichier(dossier, filename):
    return send_from_directory(os.path.join(PROJETS_DIR, dossier), filename)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
