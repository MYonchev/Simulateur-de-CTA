
# =========================================
# HVAC-GAME : CALCULS DE L'AIR
# =========================================


# =========================================
# 1. PUISSANCE DE CHAUFFAGE
# =========================================

def chauffage(debit, t_entree, t_sortie):
    """
    Débit en m³/h
    Températures en °C
    Résultat en kW
    """

    puissance = (
        0.34 * debit * (t_sortie - t_entree) / 1000
    )

    return max(0, puissance)


# =========================================
# 2. PUISSANCE DE REFROIDISSEMENT
# =========================================

def refroidissement(debit, t_entree, t_sortie):
    """
    Débit en m³/h
    Températures en °C
    Résultat en kW
    """

    puissance = (
        0.34 * debit * (t_entree - t_sortie) / 1000
    )

    return max(0, puissance)


# =========================================
# 3. PUISSANCE DU VENTILATEUR
# =========================================

def ventilateur(debit, pression, rendement=0.7):
    """
    Débit en m³/h
    Pression en Pa
    Rendement entre 0 et 1
    Résultat en kW
    """

    if rendement <= 0 or rendement > 1:
        raise ValueError(
            "Le rendement doit être entre 0 et 1."
        )

    puissance = (
        debit * pression
        / (3600 * rendement * 1000)
    )

    return max(0, puissance)


# =========================================
# 4. RECUPERATION DE CHALEUR
# =========================================

def recuperation(
    t_exterieure,
    t_interieure,
    rendement=0.7
):
    """
    Estimation pédagogique de la température
    après récupération de chaleur.
    """

    return (
        t_exterieure
        + rendement * (t_interieure - t_exterieure)
    )


# =========================================
# 5. PERTE DE CHARGE DU FILTRE
# =========================================

def perte_charge_filtre(
    debit,
    surface_filtre=None,
    coefficient=41.7,
    masse_volumique=1.2
):
    """
    Calcule la perte de charge du filtre.

    Formule :
    delta_p = K * rho * v² / 2

    debit : m³/h
    surface_filtre : m²
    coefficient : coefficient de résistance
    masse_volumique : kg/m³

    Résultat : Pa

    Hypothèses pédagogiques :
    - Filtre de référence à 12500 m³/h
    - Vitesse de référence : 2 m/s
    - Environ 100 Pa au débit de référence
    """

    if debit < 0:
        raise ValueError(
            "Le débit ne peut pas être négatif."
        )

    # Surface du filtre de référence :
    # 12500 m³/h à une vitesse de 2 m/s
    if surface_filtre is None:

        debit_reference = 12500
        vitesse_reference = 2

        surface_filtre = (
            debit_reference / 3600
        ) / vitesse_reference

    if surface_filtre <= 0:
        raise ValueError(
            "La surface du filtre doit être positive."
        )

    # Conversion du débit : m³/h -> m³/s
    debit_m3s = debit / 3600

    # Vitesse de l'air à travers le filtre
    vitesse = debit_m3s / surface_filtre

    # Perte de charge en Pa
    perte_charge = (
        coefficient
        * masse_volumique
        * vitesse ** 2
        / 2
    )

    return perte_charge
