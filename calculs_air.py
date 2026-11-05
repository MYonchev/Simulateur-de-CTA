# MOTEUR DE CALCUL DE LA CTA
# Unite : T en °C, x en kg/kg d'air sec,
# h en kJ/kg, debit en m3/h, pression en Pa.

import math

CP = 1.006
CP_VAPEUR = 1.86
RHO = 1.2
P_ATM = 101325



# CALCULS GENERAUX DE L'AIR

def debit_massique(debit_m3_h, rho=RHO):
    """Convertit un debit volumique en debit massique."""
    return rho * debit_m3_h / 3600


def pression_saturation(T):
    """Pression de vapeur saturante en Pa."""
    return 610.94 * math.exp(17.625 * T / (T + 243.04))


def x_depuis_T_HR(T, HR, P=P_ATM):
    """Calcule l'humidite specifique x depuis T et HR."""
    if not 0 <= HR <= 100:
        raise ValueError("L'humidite relative doit etre entre 0 et 100 %.")

    pv = (HR / 100) * pression_saturation(T)

    if pv >= P:
        raise ValueError("Pression de vapeur trop elevee.")

    return 0.62198 * pv / (P - pv)


def HR_depuis_T_x(T, x, P=P_ATM):
    """Calcule l'humidite relative depuis T et x."""
    pv = P * x / (0.62198 + x)
    HR = 100 * pv / pression_saturation(T)

    return max(0, min(100, HR))


def enthalpie(T, x):
    """Calcule l'enthalpie de l'air humide en kJ/kg."""
    return CP * T + x * (2501 + CP_VAPEUR * T)


def point_rosee(T, x, P=P_ATM):
    """Calcule le point de rosee en °C."""
    pv = P * x / (0.62198 + x)

    if pv <= 0:
        return None

    a = math.log(pv / 610.94)

    return 243.04 * a / (17.625 - a)


def etat_air(T, HR, debit_m3_h, P=P_ATM):
    """Construit un etat d'air avec ses caracteristiques."""
    x = x_depuis_T_HR(T, HR, P)

    return {
        "T": T,
        "HR": HR,
        "x": x,
        "h": enthalpie(T, x),
        "P": P,
        "debit_m3_h": debit_m3_h,
        "m_dot": debit_massique(debit_m3_h)
    }


def actualiser(air):
    """Actualise l'enthalpie et l'humidite relative de l'air."""
    air["h"] = enthalpie(air["T"], air["x"])
    air["HR"] = HR_depuis_T_x(
        air["T"],
        air["x"],
        air["P"]
    )

    return air



# MODULES DE CALCUL

def filtre(air, delta_p):
    """Applique la perte de charge du filtre."""
    air["P"] -= delta_p

    return {
        "module": "Filtration",
        "perte_charge_Pa": delta_p
    }


def batterie_chaude(air, T_sortie):
    """Calcule la puissance de chauffage."""
    T_entree = air["T"]

    puissance_kw = (
        air["m_dot"] * CP * (T_sortie - T_entree)
    )

    air["T"] = T_sortie
    actualiser(air)

    return {
        "module": "Batterie chaude",
        "puissance_chauffage_kW": max(0, puissance_kw)
    }


def batterie_froide(air, T_sortie, x_sortie):
    """Calcule la puissance frigorifique et les condensats."""
    h_entree = air["h"]
    x_entree = air["x"]

    air["T"] = T_sortie
    air["x"] = x_sortie
    actualiser(air)

    puissance_kw = air["m_dot"] * (h_entree - air["h"])

    condensats_kg_s = max(
        0,
        air["m_dot"] * (x_entree - x_sortie)
    )

    return {
        "module": "Batterie froide",
        "puissance_froid_kW": max(0, puissance_kw),
        "condensats_kg_s": condensats_kg_s,
        "condensats_kg_h": condensats_kg_s * 3600
    }


def recuperateur(air, T_air_repris, rendement, delta_p=0):
    """Calcule la temperature de sortie du recuperateur."""
    if not 0 <= rendement <= 1:
        raise ValueError("Le rendement doit etre entre 0 et 1.")

    T_entree = air["T"]

    T_sortie = T_entree + rendement * (
        T_air_repris - T_entree
    )

    air["T"] = T_sortie
    air["P"] -= delta_p
    actualiser(air)

    return {
        "module": "Recuperateur",
        "temperature_sortie_C": T_sortie,
        "rendement": rendement,
        "perte_charge_Pa": delta_p
    }


def humidificateur(air, x_sortie):
    """Calcule le debit d'eau ajoute."""
    x_entree = air["x"]

    debit_eau = air["m_dot"] * (
        x_sortie - x_entree
    )

    air["x"] = x_sortie
    actualiser(air)

    return {
        "module": "Humidificateur",
        "eau_ajoutee_kg_s": max(0, debit_eau),
        "eau_ajoutee_kg_h": max(0, debit_eau * 3600)
    }


def ventilateur(air, delta_p, rendement):
    """Calcule la puissance absorbee par le ventilateur."""
    if rendement <= 0 or rendement > 1:
        raise ValueError(
            "Le rendement doit etre superieur a 0 et inferieur ou egal a 1."
        )

    debit_m3_s = air["debit_m3_h"] / 3600

    puissance_air_kw = debit_m3_s * delta_p / 1000
    puissance_absorbee_kw = puissance_air_kw / rendement

    air["P"] += delta_p

    return {
        "module": "Ventilateur",
        "puissance_air_kW": puissance_air_kw,
        "puissance_absorbee_kW": puissance_absorbee_kw
    }



# BILAN GENERAL

def bilan(resultats, duree_h=1):
    chauffage = sum(
        r.get("puissance_chauffage_kW", 0)
        for r in resultats
    )

    froid = sum(
        r.get("puissance_froid_kW", 0)
        for r in resultats
    )

    ventilation = sum(
        r.get("puissance_absorbee_kW", 0)
        for r in resultats
    )

    condensats = sum(
        r.get("condensats_kg_h", 0)
        for r in resultats
    )

    eau = sum(
        r.get("eau_ajoutee_kg_h", 0)
        for r in resultats
    )

    pertes_charge = sum(
        r.get("perte_charge_Pa", 0)
        for r in resultats
    )

    return {
        "chauffage_kW": chauffage,
        "froid_kW": froid,
        "ventilation_kW": ventilation,
        "energie_chauffage_kWh": chauffage * duree_h,
        "energie_froid_kWh": froid * duree_h,
        "energie_ventilation_kWh": ventilation * duree_h,
        "condensats_kg_h": condensats,
        "eau_humidification_kg_h": eau,
        "pertes_charge_Pa": pertes_charge
    }


def afficher_etat(air):
    print("\n--- ETAT DE L'AIR ---")
    print("Temperature :", round(air["T"], 2), "°C")
    print("Humidite relative :", round(air["HR"], 1), "%")
    print("Humidite specifique :", round(air["x"], 6), "kg/kg")
    print("Enthalpie :", round(air["h"], 2), "kJ/kg")
    print("Pression :", round(air["P"], 1), "Pa")
    print("Debit volumique :", air["debit_m3_h"], "m3/h")
    print("Debit massique :", round(air["m_dot"], 4), "kg/s")

    print(
        "Point de rosee :",
        point_rosee(air["T"], air["x"]),
        "°C"
    )
