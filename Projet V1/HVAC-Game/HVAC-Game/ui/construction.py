
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image, ImageTk

from game import calculs_air as ca
from game.composants import obtenir_description

from game.verification import (
    verifier_construction,
    analyser_mode
)

from sauvegarde.gestion import sauvegarder


def afficher_construction(
    app,
    type_cta,
    retour_menu,
    projet,
    composants_restaures=None
):

    # =====================================
    # 1. INFORMATIONS DU PROJET
    # =====================================

    debit = float(projet["debit"])
    temperature = float(projet["temperature"])
    temperature_cible = float(
        projet["temperature_cible"]
    )
    pression = float(projet["pression"])
    humidite = float(projet["humidite"])
    humidite_cible = float(
        projet["humidite_cible"]
    )
    mode = projet["mode"]

    # =====================================
    # 2. CALCULS HVAC
    # =====================================

    chauffage_kw = ca.chauffage(
        debit,
        temperature,
        temperature_cible
    )

    froid_kw = ca.refroidissement(
        debit,
        temperature,
        temperature_cible
    )

    ventilateur_kw = ca.ventilateur(
        debit,
        pression
    )

    temperature_recup = ca.recuperation(
        temperature,
        20
    )

    perte_filtre_pa = ca.perte_charge_filtre(
        debit
    )

    # =====================================
    # 3. IMAGES DES COMPOSANTS
    # =====================================

    dossier_assets = (
        Path(__file__).resolve().parent.parent
        / "assets"
    )

    dossier_composants = (
        dossier_assets / "Composant"
    )

    fichiers_composants = {
        "Filtre": "filtre.png",
        "Ventilateur": "ventilateur.png",
        "Batterie chaude": "batterie_chaude.png",
        "Batterie froide": "batterie_froide.png",
        "Récupérateur": "recuperateur.png",
        "Humidificateur": "humidificateur.png"
    }

    images_originales = {}
    images_boutons = {}
    images_placement = {}

    for nom, fichier in fichiers_composants.items():

        chemin = dossier_composants / fichier

        if chemin.exists():

            with Image.open(chemin) as source:
                image = source.convert("RGBA")

            images_originales[nom] = image

            images_boutons[nom] = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(46, 46)
            )

        else:

            images_originales[nom] = None
            images_boutons[nom] = None

            print("Image manquante :", chemin)

    # =====================================
    # 4. POSITIONS DES CASES
    # =====================================

    # CTA SIMPLE FLUX : 5 CASES

    positions_simple = [
        (182, 172),
        (289, 171),
        (406, 172),
        (522, 176),
        (632, 177)
    ]

    # CTA DOUBLE FLUX : 8 CASES
    # Tes coordonnées définitives

    positions_double = [
        (187, 127),
        (351, 120),
        (204, 213),
        (289, 170),
        (382, 216),
        (469, 216),
        (576, 218),
        (633, 219)
    ]

    # =====================================
    # 5. DIMENSIONS DES CASES
    # =====================================

    # Dimensions provisoires.
    # Ton collègue pourra les modifier.

    dimensions_simple = [
        (70, 110),
        (70, 110),
        (70, 110),
        (70, 110),
        (70, 110)
    ]

    dimensions_double = [
        (65, 60),
        (70, 60),
        (65, 60),
        (65, 55),
        (65, 60),
        (65, 60),
        (60, 60),
        (50, 60)
    ]

    if type_cta == "simple":

        positions_base = positions_simple
        dimensions_base = dimensions_simple
        fichier_cta = "cta_simple_flux.png"

    else:

        positions_base = positions_double
        dimensions_base = dimensions_double
        fichier_cta = "cta_double_flux.png"

    # =====================================
    # 6. VARIABLES DU JEU
    # =====================================

    composant_selectionne = None

    composants_places = {}
    objets_places = {}

    # =====================================
    # 7. NETTOYER LA FENETRE
    # =====================================

    for widget in app.winfo_children():
        widget.destroy()

    # =====================================
    # 8. ORGANISATION DE LA PAGE
    # =====================================

    page = ctk.CTkFrame(
        app,
        fg_color="transparent"
    )

    page.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )

    page.grid_columnconfigure(0, weight=0)
    page.grid_columnconfigure(1, weight=1)
    page.grid_columnconfigure(2, weight=0)

    page.grid_rowconfigure(0, weight=1)

    # =====================================
    # 9. COLONNE GAUCHE
    # =====================================

    zone_composants = ctk.CTkScrollableFrame(
        page,
        width=220
    )

    zone_composants.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5
    )

    ctk.CTkLabel(
        zone_composants,
        text="Composants",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    texte_selection = ctk.CTkLabel(
        zone_composants,
        text="Choisis un composant",
        wraplength=190
    )

    texte_selection.pack(pady=10)

    # =====================================
    # 10. COLONNE CENTRALE
    # =====================================

    zone_centrale = ctk.CTkScrollableFrame(
        page,
        fg_color="transparent"
    )

    zone_centrale.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=10
    )

    ctk.CTkLabel(
        zone_centrale,
        text="Construction CTA " + type_cta,
        font=("Arial", 30, "bold")
    ).pack(pady=(15, 10))

    # =====================================
    # 11. IMAGE DE LA CTA
    # =====================================

    chemin_cta = dossier_assets / fichier_cta

    canvas = None
    largeur_image = 800
    hauteur_image = 350

    if chemin_cta.exists():

        with Image.open(chemin_cta) as source:
            image_cta = source.convert("RGBA")

        app.update_idletasks()

        largeur_disponible = (
            app.winfo_width() - 570
        )

        # Double flux agrandie de 20 %

        if type_cta == "double":

            largeur_voulue = max(
                500,
                min(
                    1100,
                    int(largeur_disponible * 1.20)
                )
            )

        else:

            largeur_voulue = max(
                500,
                min(1000, largeur_disponible)
            )

        largeur_orig, hauteur_orig = (
            image_cta.size
        )

        hauteur_voulue = max(
            1,
            round(
                hauteur_orig
                * largeur_voulue
                / largeur_orig
            )
        )

        image_cta = image_cta.resize(
            (largeur_voulue, hauteur_voulue),
            Image.Resampling.LANCZOS
        )

        largeur_image, hauteur_image = (
            image_cta.size
        )

        canvas = tk.Canvas(
            zone_centrale,
            width=largeur_image,
            height=hauteur_image,
            bg="#242424",
            highlightthickness=0
        )

        canvas.pack(pady=(65, 35))

        image_fond = ImageTk.PhotoImage(
            image_cta
        )

        canvas.create_image(
            0,
            0,
            image=image_fond,
            anchor="nw"
        )

        canvas.image_fond = image_fond

    else:

        ctk.CTkLabel(
            zone_centrale,
            text="Image introuvable : " + fichier_cta,
            text_color="red"
        ).pack(pady=30)

    # =====================================
    # 12. ADAPTER LES COORDONNEES
    # =====================================

    facteur_x = largeur_image / 800
    facteur_y = hauteur_image / 350

    positions = []

    for x, y in positions_base:

        positions.append((
            x * facteur_x,
            y * facteur_y
        ))

    dimensions_cases = []

    for largeur, hauteur in dimensions_base:

        dimensions_cases.append((
            largeur * facteur_x,
            hauteur * facteur_y
        ))

    # =====================================
    # 13. TAILLE DES IMAGES
    # =====================================

    def creer_image_adaptee(nom, numero_case):

        originale = images_originales.get(nom)

        if originale is None:
            return None

        largeur_case, hauteur_case = (
            dimensions_cases[numero_case]
        )

        largeur_max = max(
            1,
            round(largeur_case * 0.84)
        )

        hauteur_max = max(
            1,
            round(hauteur_case * 0.84)
        )

        image = originale.copy()

        # Enlever les marges transparentes

        alpha = image.getchannel("A")
        boite = alpha.getbbox()

        if boite is not None:
            image = image.crop(boite)

        largeur_orig, hauteur_orig = image.size

        facteur = min(
            largeur_max / largeur_orig,
            hauteur_max / hauteur_orig
        )

        nouvelle_largeur = max(
            1,
            round(largeur_orig * facteur)
        )

        nouvelle_hauteur = max(
            1,
            round(hauteur_orig * facteur)
        )

        image = image.resize(
            (nouvelle_largeur, nouvelle_hauteur),
            Image.Resampling.LANCZOS
        )

        return ImageTk.PhotoImage(image)

    # =====================================
    # 14. ZONE RESULTAT
    # =====================================

    zone_resultat = ctk.CTkFrame(
        zone_centrale
    )

    zone_resultat.pack(
        fill="x",
        padx=20,
        pady=(30, 15)
    )

    ctk.CTkLabel(
        zone_resultat,
        text="Résultat",
        font=("Arial", 24, "bold")
    ).pack(pady=(12, 5))

    texte_resultats_composants = ctk.CTkLabel(
        zone_resultat,
        text="Aucun composant placé pour le moment.",
        justify="left",
        anchor="w",
        wraplength=650,
        font=("Arial", 13)
    )

    texte_resultats_composants.pack(
        fill="x",
        padx=20,
        pady=(10, 15)
    )

    texte_verification = ctk.CTkLabel(
        zone_resultat,
        text="",
        justify="center",
        wraplength=650,
        font=("Arial", 14, "bold")
    )

    texte_verification.pack(
        fill="x",
        padx=20,
        pady=(0, 12)
    )

    # =====================================
    # 15. COLONNE DROITE
    # =====================================

    zone_calculs = ctk.CTkScrollableFrame(
        page,
        width=220
    )

    zone_calculs.grid(
        row=0,
        column=2,
        sticky="nsew",
        padx=5
    )

    ctk.CTkLabel(
        zone_calculs,
        text="Calculs HVAC",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    ctk.CTkLabel(
        zone_calculs,
        text=(
            f"Projet : {projet['nom']}\n"
            f"Mode : {mode}\n\n"
            f"Débit : {debit:.0f} m³/h\n"
            f"T° extérieure : {temperature} °C\n"
            f"T° cible : {temperature_cible} °C\n"
            f"Humidité extérieure : {humidite} %\n"
            f"Humidité cible : {humidite_cible} %\n"
            f"Pression : {pression} Pa"
        ),
        justify="left",
        wraplength=190
    ).pack(padx=10, pady=15)

    # =====================================
    # 16. DESCRIPTION DES COMPOSANTS
    # =====================================

    def description_composant(nom):

        description = obtenir_description(nom)

        if nom == "Filtre":

            description += (
                "\nPerte de charge calculée : "
                f"{perte_filtre_pa:.2f} Pa.\n"
                "Modèle pédagogique à surface "
                "de filtre constante."
            )

        elif nom == "Ventilateur":

            description += (
                "\nPuissance estimée : "
                f"{ventilateur_kw:.2f} kW."
            )

        elif nom == "Batterie chaude":

            description += (
                "\nBesoin de chauffage estimé : "
                f"{chauffage_kw:.2f} kW."
            )

        elif nom == "Batterie froide":

            description += (
                "\nBesoin de refroidissement estimé : "
                f"{froid_kw:.2f} kW."
            )

        elif nom == "Récupérateur":

            description += (
                "\nTempérature théorique après "
                f"récupération : "
                f"{temperature_recup:.2f} °C."
            )

        elif nom == "Humidificateur":

            description += (
                "\nCalcul d'humidification "
                "à ajouter plus tard."
            )

        return description

    # =====================================
    # 17. ACTUALISER LES RESULTATS
    # =====================================

    def actualiser_resultats():

        if not composants_places:

            texte_resultats_composants.configure(
                text="Aucun composant placé pour le moment."
            )
            return

        lignes = []

        for numero_case in sorted(composants_places):

            nom = composants_places[numero_case]

            lignes.append(
                f"{nom}\n"
                f"{description_composant(nom)}"
            )

        texte_resultats_composants.configure(
            text="\n\n".join(lignes)
        )

    # =====================================
    # 18. SELECTIONNER UN COMPOSANT
    # =====================================

    def choisir_composant(nom):

        nonlocal composant_selectionne

        composant_selectionne = nom

        texte_selection.configure(
            text=(
                f"Sélectionné : {nom}\n"
                "Clique sur une case en damier."
            )
        )

    # =====================================
    # 19. PLACER UN COMPOSANT
    # =====================================

    def placer_composant(numero_case, nom=None):

        # Le nom est donné lors du chargement.
        # Sinon, on utilise le composant
        # sélectionné par le joueur.

        if nom is None:
            nom = composant_selectionne

        if nom is None or canvas is None:
            return

        if not 0 <= numero_case < len(positions):
            return

        image = creer_image_adaptee(
            nom,
            numero_case
        )

        if image is None:
            return

        x, y = positions[numero_case]

        # Retirer l'ancien composant
        # si la case était déjà occupée.

        if numero_case in objets_places:

            canvas.delete(
                objets_places[numero_case]
            )

            del objets_places[numero_case]
            del composants_places[numero_case]

            images_placement.pop(
                numero_case,
                None
            )

        objet = canvas.create_image(
            x,
            y,
            image=image,
            anchor="center"
        )

        objets_places[numero_case] = objet
        composants_places[numero_case] = nom

        # Garder l'image en mémoire
        images_placement[numero_case] = image

        actualiser_resultats()

        texte_verification.configure(text="")

    # =====================================
    # 20. CLIC SUR LA CTA
    # =====================================

    def clic_sur_cta(event):

        if canvas is None:
            return

        if composant_selectionne is None:

            texte_selection.configure(
                text="Choisis d'abord un composant."
            )
            return

        if not positions:
            return

        distances = []

        for px, py in positions:

            distance = (
                (event.x - px) ** 2
                + (event.y - py) ** 2
            )

            distances.append(distance)

        numero_case = distances.index(
            min(distances)
        )

        tolerance = (
            40 * largeur_image / 800
        )

        if distances[numero_case] > tolerance ** 2:

            texte_selection.configure(
                text="Clique au centre d'une case."
            )
            return

        placer_composant(numero_case)

    if canvas is not None:

        canvas.bind(
            "<Button-1>",
            clic_sur_cta
        )

    # =====================================
    # 21. BOUTONS DES COMPOSANTS
    # =====================================

    for nom in fichiers_composants:

        ctk.CTkButton(
            zone_composants,
            text=nom,
            image=images_boutons[nom],
            compound="left",
            width=195,
            height=70,
            command=lambda n=nom: choisir_composant(n)
        ).pack(pady=6)

    # =====================================
    # 22. SUPPRIMER LE DERNIER
    # =====================================

    def supprimer_dernier():

        if not composants_places:
            return

        derniere_case = list(
            composants_places.keys()
        )[-1]

        if canvas is not None:

            canvas.delete(
                objets_places[derniere_case]
            )

        del objets_places[derniere_case]
        del composants_places[derniere_case]

        images_placement.pop(
            derniere_case,
            None
        )

        actualiser_resultats()

        texte_verification.configure(text="")

    # =====================================
    # 23. REINITIALISER
    # =====================================

    def reinitialiser():

        if canvas is not None:

            for objet in objets_places.values():
                canvas.delete(objet)

        objets_places.clear()
        composants_places.clear()
        images_placement.clear()

        actualiser_resultats()

        texte_verification.configure(text="")

    # =====================================
    # 24. SAUVEGARDER LA PARTIE
    # =====================================

    def enregistrer_partie():

        try:

            sauvegarder(
                projet,
                composants_places
            )

            messagebox.showinfo(
                "Sauvegarde",
                "✅ Partie sauvegardée !\n\n"
                "Tu pourras la reprendre plus tard."
            )

        except OSError as erreur:

            messagebox.showerror(
                "Erreur",
                "Impossible de sauvegarder.\n"
                + str(erreur)
            )

    # =====================================
    # 25. VERIFIER LA CTA
    # =====================================

    def verifier_cta():

        # Vérifier l'ordre des composants

        erreurs = verifier_construction(
            type_cta,
            composants_places,
            temperature,
            temperature_cible
        )

        # Analyser le mode hiver / été /
        # mi-saison selon les températures

        explication = analyser_mode(
            mode,
            temperature,
            temperature_cible
        )

        if erreurs:

            message = (
                "❌ CONCEPTION INCORRECTE\n\n"
                + "\n".join(erreurs)
                + "\n\n"
                + explication
            )

            texte_verification.configure(
                text=message,
                text_color="#FF6B6B"
            )

        else:

            nombre_cases = len(positions)

            message = (
                "✅ FÉLICITATIONS !\n\n"
                "Votre CTA est correctement "
                "assemblée.\n"
                f"Les {nombre_cases} composants "
                "sont aux bons emplacements.\n\n"
                + explication
            )

            texte_verification.configure(
                text=message,
                text_color="#4ADE80"
            )

    # =====================================
    # 26. BOUTONS DE CONTROLE
    # =====================================

    zone_boutons = ctk.CTkFrame(
        zone_centrale,
        fg_color="transparent"
    )

    zone_boutons.pack(pady=(15, 10))

    ctk.CTkButton(
        zone_boutons,
        text="Supprimer le dernier",
        command=supprimer_dernier,
        width=170
    ).pack(
        side="left",
        padx=5
    )

    ctk.CTkButton(
        zone_boutons,
        text="Réinitialiser",
        command=reinitialiser,
        width=140
    ).pack(
        side="left",
        padx=5
    )

    # =====================================
    # 27. BOUTON SAUVEGARDER
    # =====================================

    ctk.CTkButton(
        zone_centrale,
        text="💾 Sauvegarder ma partie",
        command=enregistrer_partie,
        width=230,
        height=45
    ).pack(pady=10)

    # =====================================
    # 28. BOUTON VERIFIER
    # =====================================

    ctk.CTkButton(
        zone_centrale,
        text="✅ Vérifier ma CTA",
        command=verifier_cta,
        width=220,
        height=45,
        fg_color="#25834A",
        hover_color="#1D683A",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    # =====================================
    # 29. RETOUR AU MENU
    # =====================================

    ctk.CTkButton(
        zone_centrale,
        text="Retour au menu",
        command=retour_menu,
        width=200,
        height=40
    ).pack(pady=(10, 25))

    # =====================================
    # 30. CHARGER UNE PARTIE SAUVEGARDEE
    # =====================================

    if composants_restaures is not None:

        for numero_case, nom in sorted(
            composants_restaures.items()
        ):

            placer_composant(
                numero_case,
                nom
            )
