# CONFIGURATION DES MODULES DE LA CTA

import calculs_air as ca


# MODULE 1 : FILTRATION

def filtration(air):
    print("\n--- CONFIGURATION : FILTRATION ---")

    type_filtre = input("Type de filtre : ")
    perte_filtre = float(input("Perte de charge du filtre (Pa) : "))

    # Lien avec calculs_air.py : on utilise le meme etat d'air.
    resultat = ca.filtre(air, perte_filtre)

    print("\n--- RESULTATS FILTRATION ---")
    print("Type de filtre :", type_filtre)
    print("Debit volumique =", air["debit_m3_h"], "m3/h")
    print("Debit massique =", round(air["m_dot"], 4), "kg/s")
    print("Perte de charge =", perte_filtre, "Pa")

    return resultat


# MODULE 2 : BATTERIE CHAUDE

def batterie_chaude(air):
    print("\n--- CONFIGURATION : BATTERIE CHAUDE ---")

    type_batterie = input("Type de batterie chaude : ")
    temperature_entree = air["T"]
    humidite_entree = air["HR"]
    temperature_sortie = float(input("Temperature sortie (°C) : "))

    # Calcul de l'enthalpie d'entree avant de modifier l'air.
    enthalpie_entree = air["h"]

    # Calcul de la puissance avec calculs_air.py.
    resultat = ca.batterie_chaude(air, temperature_sortie)

    print("\n--- RESULTATS BATTERIE CHAUDE ---")
    print("Type de batterie :", type_batterie)
    print("Temperature entree =", temperature_entree, "°C")
    print("Humidite relative entree =", round(humidite_entree, 1), "%")
    print("Enthalpie entree =", round(enthalpie_entree, 2), "kJ/kg")
    print("Temperature sortie =", temperature_sortie, "°C")
    print("Puissance de chauffage =", round(
        resultat["puissance_chauffage_kW"], 2
    ), "kW")

    return resultat


# MODULE 3 : BATTERIE FROIDE

def batterie_froide(air):
    print("\n--- CONFIGURATION : BATTERIE FROIDE ---")

    type_batterie = input("Type de batterie froide : ")
    temperature_entree = air["T"]
    humidite_entree = air["HR"]
    enthalpie_entree = air["h"]

    temperature_sortie = float(input("Temperature sortie (°C) : "))
    humidite_sortie = float(input("Humidite specifique sortie (kg/kg) : "))

    # Calcul de l'enthalpie de sortie.
    enthalpie_sortie = ca.enthalpie(
        temperature_sortie,
        humidite_sortie
    )

    # Calcul de la puissance avec calculs_air.py.
    resultat = ca.batterie_froide(
        air,
        temperature_sortie,
        humidite_sortie
    )

    print("\n--- RESULTATS BATTERIE FROIDE ---")
    print("Type de batterie :", type_batterie)
    print("Temperature entree =", temperature_entree, "°C")
    print("Humidite relative entree =", round(humidite_entree, 1), "%")
    print("Enthalpie entree =", round(enthalpie_entree, 2), "kJ/kg")
    print("Enthalpie sortie =", round(enthalpie_sortie, 2), "kJ/kg")
    print("Puissance frigorifique =", round(
        resultat["puissance_froid_kW"], 2
    ), "kW")
    print("Condensats =", round(
        resultat["condensats_kg_h"], 2
    ), "kg/h")

    return resultat


# MODULE 4 : VENTILATEUR

def ventilateur(air):
    print("\n--- CONFIGURATION : VENTILATEUR ---")

    type_ventilateur = input("Type de ventilateur : ")
    perte_charge = float(input("Pression fournie / perte de charge totale (Pa) : "))
    rendement = float(input("Rendement (entre 0 et 1) : "))

    # Calcul de la puissance avec calculs_air.py.
    resultat = ca.ventilateur(
        air,
        perte_charge,
        rendement
    )

    print("\n--- RESULTATS VENTILATEUR ---")
    print("Type de ventilateur :", type_ventilateur)
    print("Debit volumique =", air["debit_m3_h"], "m3/h")
    print("Pression fournie =", perte_charge, "Pa")
    print("Rendement =", rendement)
    print("Puissance absorbee =", round(
        resultat["puissance_absorbee_kW"] * 1000, 2
    ), "W")

    return resultat


# MODULE 5 : HUMIDIFICATEUR

def humidificateur(air):
    print("\n--- CONFIGURATION : HUMIDIFICATEUR ---")

    type_humidificateur = input("Type d'humidificateur : ")
    temperature_entree = air["T"]
    humidite_entree = air["HR"]
    x_entree = air["x"]
    humidite_sortie = float(input("Humidite specifique sortie (kg/kg) : "))

    # Calcul de l'eau ajoutee avec calculs_air.py.
    resultat = ca.humidificateur(
        air,
        humidite_sortie
    )

    print("\n--- RESULTATS HUMIDIFICATEUR ---")
    print("Type d'humidificateur :", type_humidificateur)
    print("Temperature entree =", temperature_entree, "°C")
    print("Humidite relative entree =", round(humidite_entree, 1), "%")
    print("Humidite specifique entree =", round(x_entree, 6), "kg/kg")
    print("Humidite specifique sortie =", humidite_sortie, "kg/kg")
    print("Debit d'eau ajoute =", round(
        resultat["eau_ajoutee_kg_s"], 5
    ), "kg/s")
    print("Debit d'eau ajoute =", round(
        resultat["eau_ajoutee_kg_h"], 2
    ), "kg/h")

    return resultat


# MODULE 6 : RECUPERATEUR

def recuperateur(air):
    print("\n--- CONFIGURATION : RECUPERATEUR ---")

    type_recuperateur = input("Type de recuperateur : ")
    temperature_air_neuf = air["T"]
    temperature_air_repris = float(input("Temperature air repris (°C) : "))
    rendement = float(input("Rendement (entre 0 et 1) : "))
    perte_charge = float(input("Perte de charge (Pa) : "))

    # Calcul du recuperateur avec calculs_air.py.
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
    print("\n================================")
    print(" CONFIGURATION DE LA CTA")
    print("================================")

    # L'etat de l'air est cree une seule fois au debut de la simulation.
    temperature = float(input("Temperature de l'air entrant (°C) : "))
    humidite = float(input("Humidite relative de l'air entrant (%) : "))
    debit_air = float(input("Debit d'air (m3/h) : "))

    air = ca.etat_air(temperature, humidite, debit_air)
    resultats = []

    print("\nEtat initial de l'air :")
    ca.afficher_etat(air)

    while True:
        print("\n================================")
        print(" AJOUTER UN MODULE A LA CTA")
        print("================================")
        print("1 - Filtration")
        print("2 - Batterie chaude")
        print("3 - Batterie froide")
        print("4 - Ventilateur")
        print("5 - Humidificateur")
        print("6 - Recuperateur")
        print("7 - Terminer la simulation et afficher le bilan")
        print("0 - Quitter")

        choix = input("Choisir un module : ")

        if choix == "1":
            resultat = filtration(air)
        elif choix == "2":
            resultat = batterie_chaude(air)
        elif choix == "3":
            resultat = batterie_froide(air)
        elif choix == "4":
            resultat = ventilateur(air)
        elif choix == "5":
            resultat = humidificateur(air)
        elif choix == "6":
            resultat = recuperateur(air)
        elif choix == "7":
            break
        elif choix == "0":
            print("Fin du programme.")
            return
        else:
            print("Choix invalide. Veuillez recommencer.")
            continue

        resultats.append(resultat)
        print("\nEtat de l'air apres ce module :")
        ca.afficher_etat(air)

    # Affichage du bilan de tous les modules utilises.
    resultat_bilan = ca.bilan(resultats)

    print("\n================================")
    print(" BILAN GENERAL DE LA CTA")
    print("================================")

    for nom, valeur in resultat_bilan.items():
        print(nom, "=", round(valeur, 3))

    print("\nEtat final de l'air :")
    ca.afficher_etat(air)


# LANCEMENT DU PROGRAMME

if __name__ == "__main__":
    menu()
