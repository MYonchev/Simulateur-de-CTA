# SIMULATION DE LA CTA
# Ce programme utilise les fichiers calculs_air.py et configuration_modules.py.
# L'air passe d'un module au suivant dans l'ordre choisi par l'utilisateur.

import calculs_air as ca
import configuration_modules as cm


# ENREGISTREMENT DE L'ETAT DE L'AIR

def enregistrer_etat(air, nom_etape):
    """Enregistre les caracteristiques de l'air a une etape de la CTA."""
    return {
        "etape": nom_etape,
        "T": air["T"],
        "HR": air["HR"],
        "x": air["x"],
        "h": air["h"],
        "P": air["P"]
    }


def afficher_historique(historique):
    """Affiche l'evolution de l'air dans les differents modules."""
    print("\n================================")
    print(" HISTORIQUE DE LA SIMULATION")
    print("================================")

    for etat in historique:
        print("\nEtape :", etat["etape"])
        print("Temperature :", round(etat["T"], 2), "°C")
        print("Humidite relative :", round(etat["HR"], 1), "%")
        print("Humidite specifique :", round(etat["x"], 6), "kg/kg")
        print("Enthalpie :", round(etat["h"], 2), "kJ/kg")
        print("Pression :", round(etat["P"], 1), "Pa")


# LANCEMENT DE LA SIMULATION

def simulation():
    print("\n================================")
    print(" SIMULATION DE LA CTA")
    print("================================")

    # Conditions de depart de l'air.
    temperature = float(input("Temperature de l'air entrant (°C) : "))
    humidite = float(input("Humidite relative de l'air entrant (%) : "))
    debit_air = float(input("Debit d'air (m3/h) : "))

    # Creation de l'etat d'air. Le meme dictionnaire sera utilise par les modules.
    air = ca.etat_air(temperature, humidite, debit_air)

    # Listes qui vont recevoir les resultats et les etats successifs.
    resultats = []
    historique = []

    historique.append(enregistrer_etat(air, "Air entrant"))

    print("\nEtat initial de l'air :")
    ca.afficher_etat(air)

    # L'utilisateur choisit les modules et leur ordre de passage.
    while True:
        print("\n================================")
        print(" CHOIX DU MODULE")
        print("================================")
        print("1 - Filtration")
        print("2 - Batterie chaude")
        print("3 - Batterie froide")
        print("4 - Ventilateur")
        print("5 - Humidificateur")
        print("6 - Recuperateur")
        print("7 - Terminer la simulation")
        print("0 - Quitter")

        choix = input("Choisir le prochain module : ")

        try:
            if choix == "1":
                resultat = cm.filtration(air)
                nom_etape = "Filtration"

            elif choix == "2":
                resultat = cm.batterie_chaude(air)
                nom_etape = "Batterie chaude"

            elif choix == "3":
                resultat = cm.batterie_froide(air)
                nom_etape = "Batterie froide"

            elif choix == "4":
                resultat = cm.ventilateur(air)
                nom_etape = "Ventilateur"

            elif choix == "5":
                resultat = cm.humidificateur(air)
                nom_etape = "Humidificateur"

            elif choix == "6":
                resultat = cm.recuperateur(air)
                nom_etape = "Recuperateur"

            elif choix == "7":
                break

            elif choix == "0":
                print("Simulation arretee.")
                return

            else:
                print("Choix invalide. Veuillez recommencer.")
                continue

            # On ajoute le resultat du module a la liste.
            resultats.append(resultat)

            # On enregistre le nouvel etat de l'air apres le module.
            historique.append(enregistrer_etat(air, nom_etape))

            print("\nEtat de l'air apres", nom_etape, ":")
            ca.afficher_etat(air)

        except ValueError as erreur:
            print("Erreur dans les valeurs entrees :", erreur)
            print("Le module n'a pas ete ajoute a la simulation.")

    # Duree utilisee pour calculer les energies en kWh.
    duree_h = float(input("Duree de fonctionnement (heures) : "))

    if duree_h < 0:
        print("La duree ne peut pas etre negative.")
        return

    # Calcul du bilan avec les resultats de tous les modules.
    resultat_bilan = ca.bilan(resultats, duree_h)

    # Affichage de l'historique des etats de l'air.
    afficher_historique(historique)

    # Affichage du bilan final.
    print("\n================================")
    print(" BILAN GENERAL DE LA CTA")
    print("================================")

    for nom, valeur in resultat_bilan.items():
        print(nom, "=", round(valeur, 3))

    print("\nEtat final de l'air :")
    ca.afficher_etat(air)

    print("\nFin de la simulation.")


# LANCEMENT DU PROGRAMME

if __name__ == "__main__":
    try:
        simulation()
    except ValueError as erreur:
        print("Impossible de lancer la simulation :", erreur)

