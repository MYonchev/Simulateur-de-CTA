
import json
from pathlib import Path

# Fichier de sauvegarde
FICHIER = Path(__file__).parent / "partie.json"


def sauvegarder(projet, composants_places):

    donnees = {
        "projet": projet,
        "composants": composants_places
    }

    with open(FICHIER, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, indent=4)

    print("Partie sauvegardée !")


def charger():

    if not FICHIER.exists():
        return None

    with open(FICHIER, "r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    return donnees

