# CONFIGURATION DES MODULES DE LA CTA


import calculs_air as ca


# MODULE 1 : FILTRATION

def filtration():
    print("\n--- CONFIGURATION : FILTRATION ---")

    type_filtre = input("Type de filtre : ")
    debit_air = float(input("Debit d'air (m3/h) : "))
    perte_filtre = float(input("Perte de charge du filtre (Pa) : "))

    # Lien avec calculs_air.py
    debit_massique = ca.debit_massique(debit_air)

    print("\n--- RESULTATS FILTRATION ---")
    print("Type de filtre :", type_filtre)
    print("Debit volumique =", debit_air, "m3/h")
    print("Debit massique =", round(debit_massique, 4), "kg/s")
    print("Perte de charge =", perte_filtre, "Pa")

    return {
        "module": "Filtration",
        "debit_massique": debit_massique,
        "perte_charge_Pa": perte_filtre
    }


# MODULE 2 : BATTERIE CHAUDE

def batterie_chaude():
    print("\n--- CONFIGURATION : BATTERIE CHAUDE ---")

    type_batterie = input("Type de batterie chaude : ")

    debit_air = float(input("Debit d'air (m3/h) : "))
    temperature_entree = float(input("Temperature entree (°C) : "))
    humidite_entree = float(input("Humidite relative entree (%) : "))
    temperature_sortie = float(input("Temperature sortie (°C) : "))

    # Creation de l'etat d'air avec calculs_air.py
    air = ca.etat_air(
        temperature_entree,
        humidite_entree,
        debit_air
    )

    # Calcul de la puissance avec calculs_air.py
    resultat = ca.batterie_chaude(
        air,
        temperature_sortie
    )

    print("\n--- RESULTATS BATTERIE CHAUDE ---")
    print("Type de batterie :", type_batterie)
    print("Enthalpie entree =", round(
        ca.enthalpie(temperature_entree, air["x"]), 2
    ), "kJ/kg")
    print("Temperature sortie =", temperature_sortie, "°C")
    print("Puissance de chauffage =", round(
        resultat["puissance_chauffage_kW"], 2
    ), "kW")

    return resultat


# MODULE 3 : BATTERIE FROIDE

def batterie_froide():
    print("\n--- CONFIGURATION : BATTERIE FROIDE ---")

    type_batterie = input("Type de batterie froide : ")

    debit_air = float(input("Debit d'air (m3/h) : "))
    temperature_entree = float(input("Temperature entree (°C) : "))
    humidite_entree = float(input("Humidite relative entree (%) : "))

    temperature_sortie = float(input("Temperature sortie (°C) : "))
    humidite_sortie = float(input("Humidite specifique sortie (kg/kg) : "))

    # Creation de l'etat d'air
    air = ca.etat_air(
        temperature_entree,
        humidite_entree,
        debit_air
    )

    # Calcul de l'enthalpie de sortie
    enthalpie_sortie = ca.enthalpie(
        temperature_sortie,
        humidite_sortie
    )

    # Calcul de la puissance frigorifique
    resultat = ca.batterie_froide(
        air,
        temperature_sortie,
        humidite_sortie
    )

    print("\n--- RESULTATS BATTERIE FROIDE ---")
    print("Type de batterie :", type_batterie)
    print("Enthalpie entree =", round(air["h"], 2), "kJ/kg")
    print("Enthalpie sortie =", round(enthalpie_sortie, 2), "kJ/kg")
    print("Puissance frigorifique =", round(
        resultat["puissance_froid_kW"], 2
    ), "kW")
    print("Condensats =", round(
        resultat["condensats_kg_h"], 2
    ), "kg/h")

    return resultat


# MODULE 4 : VENTILATEUR

def ventilateur():
    print("\n--- CONFIGURATION : VENTILATEUR ---")

    type_ventilateur = input("Type de ventilateur : ")

    debit_air = float(input("Debit d'air (m3/h) : "))
    temperature_air = float(input("Temperature de l'air (°C) : "))
    humidite_air = float(input("Humidite relative de l'air (%) : "))

    perte_charge = float(input("Perte de charge totale (Pa) : "))
    rendement = float(input("Rendement (entre 0 et 1) : "))

    # Creation de l'etat d'air
    air = ca.etat_air(
        temperature_air,
        humidite_air,
        debit_air
    )

    # Calcul de la puissance avec calculs_air.py
    resultat = ca.ventilateur(
        air,
        perte_charge,
        rendement
    )

    print("\n--- RESULTATS VENTILATEUR ---")
    print("Type de ventilateur :", type_ventilateur)
    print("Debit volumique =", debit_air, "m3/h")
    print("Perte de charge =", perte_charge, "Pa")
    print("Rendement =", rendement)
    print("Puissance absorbee =", round(
        resultat["puissance_absorbee_kW"] * 1000, 2
    ), "W")

    return resultat


# MODULE 5 : HUMIDIFICATEUR

def humidificateur():
    print("\n--- CONFIGURATION : HUMIDIFICATEUR ---")

    type_humidificateur = input("Type d'humidificateur : ")

    debit_air = float(input("Debit d'air (m3/h) : "))
    temperature_entree = float(input("Temperature entree (°C) : "))
    humidite_entree = float(input("Humidite relative entree (%) : "))
    humidite_sortie = float(input("Humidite specifique sortie (kg/kg) : "))

    # Creation de l'etat d'air
    air = ca.etat_air(
        temperature_entree,
        humidite_entree,
        debit_air
    )

    # Calcul de l'eau ajoutee avec calculs_air.py
    resultat = ca.humidificateur(
        air,
        humidite_sortie
    )

    print("\n--- RESULTATS HUMIDIFICATEUR ---")
    print("Type d'humidificateur :", type_humidificateur)
    print("Humidite specifique entree =", round(
        ca.x_depuis_T_HR(temperature_entree, humidite_entree), 6
    ), "kg/kg")
    print("Humidite specifique sortie =", humidite_sortie, "kg/kg")
    print("Debit d'eau ajoute =", round(
        resultat["eau_ajoutee_kg_s"], 5
    ), "kg/s")
    print("Debit d'eau ajoute =", round(
        resultat["eau_ajoutee_kg_h"], 2
    ), "kg/h")

    return resultat



# MODULE 6 : RECUPERATEUR

def recuperateur():
    print("\n--- CONFIGURATION : RECUPERATEUR ---")

    type_recuperateur = input("Type de recuperateur : ")

    debit_air = float(input("Debit d'air (m3/h) : "))
    temperature_air_neuf = float(input("Temperature air neuf (°C) : "))
    humidite_air_neuf = float(input("Humidite relative air neuf (%) : "))

    temperature_air_repris = float(input("Temperature air repris (°C) : "))
    rendement = float(input("Rendement (entre 0 et 1) : "))
    perte_charge = float(input("Perte de charge (Pa) : "))

    # Creation de l'etat d'air neuf
    air = ca.etat_air(
        temperature_air_neuf,
        humidite_air_neuf,
        debit_air
    )

    # Calcul du recuperateur avec calculs_air.py
    resultat = ca.recuperateur(
        air,
        temperature_air_repris,
        rendement,
        perte_charge
    )

    print("\n--- RESULTATS RECUPERATEUR ---")
    print("Type de recuperateur :", type_recuperateur)
    print("Temperature air neuf =", temperature_air_neuf, "°C")
    print("Temperature air repris =", temperature_air_repris, "°C")
    print("Rendement =", rendement)
    print("Temperature de sortie =", round(
        resultat["temperature_sortie_C"], 2
    ), "°C")
    print("Perte de charge =", perte_charge, "Pa")

    return resultat



# MENU PRINCIPAL

def menu():
    while True:
        print("\n================================")
        print(" CONFIGURATION DE LA CTA")
        print("================================")
        print("1 - Filtration")
        print("2 - Batterie chaude")
        print("3 - Batterie froide")
        print("4 - Ventilateur")
        print("5 - Humidificateur")
        print("6 - Recuperateur")
        print("7 - Configurer tous les modules")
        print("0 - Quitter")

        choix = input("Choisir une option : ")

        if choix == "1":
            filtration()

        elif choix == "2":
            batterie_chaude()

        elif choix == "3":
            batterie_froide()

        elif choix == "4":
            ventilateur()

        elif choix == "5":
            humidificateur()

        elif choix == "6":
            recuperateur()

        elif choix == "7":
            filtration()
            batterie_chaude()
            batterie_froide()
            ventilateur()
            humidificateur()
            recuperateur()

        elif choix == "0":
            print("Fin du programme.")
            break

        else:
            print("Choix invalide. Veuillez recommencer.")


# LANCEMENT DU PROGRAMME

if __name__ == "__main__":
    menu()
