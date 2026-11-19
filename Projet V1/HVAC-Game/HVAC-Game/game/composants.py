
# =========================================
# HVAC-GAME : COMPOSANTS
# =========================================

COMPOSANTS = {

    "Filtre": {
        "role": "Filtration de l'air",
        "description": (
            "Retient les poussières et certaines "
            "particules présentes dans l'air."
        ),
        "saison": "Toute l'année",
        "perte_charge": None
    },

    "Ventilateur": {
        "role": "Circulation de l'air",
        "description": (
            "Assure la circulation et le soufflage "
            "de l'air dans le bâtiment."
        ),
        "saison": "Toute l'année",
        "perte_charge": None
    },

    "Batterie chaude": {
        "role": "Chauffage de l'air",
        "description": (
            "Réchauffe l'air lorsque cela est nécessaire."
        ),
        "saison": "Principalement en hiver",
        "perte_charge": None
    },

    "Batterie froide": {
        "role": "Refroidissement de l'air",
        "description": (
            "Refroidit l'air lorsque cela est nécessaire."
        ),
        "saison": "Principalement en été",
        "perte_charge": None
    },

    "Humidificateur": {
        "role": "Humidification de l'air",
        "description": (
            "Ajoute de l'humidité lorsque l'air "
            "est trop sec."
        ),
        "saison": "Selon les besoins",
        "perte_charge": None
    },

    "Récupérateur": {
        "role": "Récupération d'énergie",
        "description": (
            "Récupère une partie de l'énergie "
            "contenue dans l'air extrait."
        ),
        "saison": "Selon les conditions",
        "perte_charge": None
    }
}


def obtenir_composant(nom):
    return COMPOSANTS.get(nom)


def obtenir_description(nom):

    composant = obtenir_composant(nom)

    if composant is None:
        return "Composant inconnu."

    return (
        f"Rôle : {composant['role']}\n"
        f"{composant['description']}\n"
        f"Utilisation : {composant['saison']}"
    )


def obtenir_perte_charge(nom):

    composant = obtenir_composant(nom)

    if composant is None:
        return None

    return composant["perte_charge"]
