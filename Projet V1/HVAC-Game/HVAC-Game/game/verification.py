
# =====================================
# VERIFICATION DES CTA
# =====================================

# CTA simple flux : 5 cases

ORDRE_SIMPLE = [
    "Filtre",
    "Batterie chaude",
    "Batterie froide",
    "Humidificateur",
    "Ventilateur"
]


# CTA double flux : 8 cases

ORDRE_DOUBLE = [
    "Filtre",
    "Filtre",
    "Ventilateur",
    "Récupérateur",
    "Ventilateur",
    "Batterie chaude",
    "Batterie froide",
    "Humidificateur"
]


# =====================================
# VERIFIER LES EMPLACEMENTS
# =====================================

def verifier_construction(
    type_cta,
    composants_places,
    temperature,
    temperature_cible
):

    erreurs = []

    if type_cta == "simple":
        ordre_attendu = ORDRE_SIMPLE

    elif type_cta == "double":
        ordre_attendu = ORDRE_DOUBLE

    else:
        return ["Type de CTA inconnu."]

    for numero, composant_attendu in enumerate(
        ordre_attendu
    ):

        composant_place = composants_places.get(
            numero
        )

        if composant_place is None:

            erreurs.append(
                f"Case {numero + 1} : "
                "il manque un composant."
            )

        elif composant_place != composant_attendu:

            erreurs.append(
                f"Case {numero + 1} : "
                "le composant est mal placé."
            )

    return erreurs


# =====================================
# ANALYSER LE MODE DE FONCTIONNEMENT
# =====================================

def analyser_mode(
    mode,
    temperature,
    temperature_cible
):

    difference = temperature_cible - temperature

    # MODE HIVER

    if mode.lower() == "hiver":

        if difference > 0:

            return (
                "❄️ MODE HIVER\n"
                "L'air extérieur est trop froid.\n"
                "Il faut utiliser le chauffage "
                "pour atteindre la température cible."
            )

        elif difference < 0:

            return (
                "❄️ MODE HIVER\n"
                "L'air extérieur est plus chaud "
                "que la température cible.\n"
                "Un refroidissement peut être nécessaire."
            )

        else:

            return (
                "❄️ MODE HIVER\n"
                "La température extérieure est "
                "déjà égale à la température cible."
            )

    # MODE ETE

    elif mode.lower() in ("été", "ete"):

        if difference < 0:

            return (
                "☀️ MODE ÉTÉ\n"
                "L'air extérieur est trop chaud.\n"
                "Il faut utiliser le refroidissement "
                "pour atteindre la température cible."
            )

        elif difference > 0:

            return (
                "☀️ MODE ÉTÉ\n"
                "L'air extérieur est plus froid "
                "que la température cible.\n"
                "Un chauffage peut être nécessaire."
            )

        else:

            return (
                "☀️ MODE ÉTÉ\n"
                "La température extérieure est "
                "déjà égale à la température cible."
            )

    # MODE MI-SAISON

    elif mode.lower() in (
        "mi-saison",
        "mi saison",
        "mi_saison"
    ):

        if difference > 0:

            return (
                "🍃 MODE MI-SAISON\n"
                "L'air extérieur doit être réchauffé "
                "pour atteindre la température cible."
            )

        elif difference < 0:

            return (
                "🍃 MODE MI-SAISON\n"
                "L'air extérieur doit être refroidi "
                "pour atteindre la température cible."
            )

        else:

            return (
                "🍃 MODE MI-SAISON\n"
                "La température extérieure correspond "
                "à la température cible."
            )

    return "Mode de fonctionnement inconnu."
