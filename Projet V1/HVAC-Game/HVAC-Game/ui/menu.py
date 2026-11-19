
import customtkinter as ctk


def afficher_menu(app, ouvrir_construction):

    # Effacer l'ancien menu
    for widget in app.winfo_children():
        widget.destroy()

    # Page défilante
    page = ctk.CTkScrollableFrame(
        app,
        fg_color="#242424"
    )
    page.pack(fill="both", expand=True)

    # Contenu centré
    contenu = ctk.CTkFrame(
        page,
        fg_color="transparent"
    )
    contenu.pack(padx=25, pady=20)

    # Titre
    ctk.CTkLabel(
        contenu,
        text="HVAC GAME",
        font=("Arial", 32, "bold")
    ).pack(pady=(0, 5))

    ctk.CTkLabel(
        contenu,
        text="Configuration de votre centrale de traitement d'air",
        text_color="#BBBBBB"
    ).pack(pady=(0, 20))

    # Fonction pour créer une section
    def section(titre, colonnes):
        cadre = ctk.CTkFrame(
            contenu,
            fg_color="#2B2B2B",
            corner_radius=12
        )
        cadre.pack(fill="x", pady=8)

        ctk.CTkLabel(
            cadre,
            text=titre,
            font=("Arial", 20, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=colonnes,
            sticky="w",
            padx=20,
            pady=(15, 15)
        )

        for i in range(colonnes):
            cadre.grid_columnconfigure(
                i, weight=1, uniform="col"
            )

        return cadre

    # Fonction pour créer un champ
    def champ(cadre, texte, valeur, ligne, colonne):
        zone = ctk.CTkFrame(
            cadre,
            fg_color="transparent"
        )
        zone.grid(
            row=ligne,
            column=colonne,
            sticky="ew",
            padx=12,
            pady=8
        )

        ctk.CTkLabel(
            zone,
            text=texte
        ).pack(anchor="w", pady=(0, 5))

        entree = ctk.CTkEntry(
            zone,
            height=38
        )
        entree.insert(0, valeur)
        entree.pack(fill="x")

        return entree

    # ===================================
    # 1. INFORMATIONS DU PROJET
    # ===================================

    cadre_projet = section(
        "1. Informations du projet", 2
    )

    nom = champ(
        cadre_projet, "Nom du projet", "", 1, 0
    )

    reference = champ(
        cadre_projet, "Référence", "", 1, 1
    )

    # ===================================
    # 2. TYPE DE CTA
    # ===================================

    cadre_cta = section(
        "2. Type de centrale", 2
    )

    type_cta = ctk.StringVar(value="double")

    bouton_simple = ctk.CTkButton(
        cadre_cta,
        text="CTA simple flux",
        height=65
    )
    bouton_simple.grid(
        row=1, column=0,
        sticky="ew", padx=12, pady=12
    )

    bouton_double = ctk.CTkButton(
        cadre_cta,
        text="CTA double flux",
        height=65
    )
    bouton_double.grid(
        row=1, column=1,
        sticky="ew", padx=12, pady=12
    )

    def choisir_cta(choix):
        type_cta.set(choix)

        bouton_simple.configure(
            fg_color="#1F6AA5" if choix == "simple" else "#444444"
        )

        bouton_double.configure(
            fg_color="#1F6AA5" if choix == "double" else "#444444"
        )

    bouton_simple.configure(
        command=lambda: choisir_cta("simple")
    )

    bouton_double.configure(
        command=lambda: choisir_cta("double")
    )

    choisir_cta("double")

    # ===================================
    # 3. CONDITIONS DE FONCTIONNEMENT
    # ===================================

    cadre_conditions = section(
        "3. Conditions de fonctionnement", 3
    )

    debit = champ(
        cadre_conditions,
        "Débit d'air (m³/h)",
        "12500", 1, 0
    )

    temperature = champ(
        cadre_conditions,
        "Température extérieure (°C)",
        "-5", 1, 1
    )

    temperature_cible = champ(
        cadre_conditions,
        "Température de soufflage (°C)",
        "20", 1, 2
    )

    humidite = champ(
        cadre_conditions,
        "Humidité extérieure (%)",
        "80", 2, 0
    )

    humidite_cible = champ(
        cadre_conditions,
        "Humidité cible (%)",
        "45", 2, 1
    )

    pression = champ(
        cadre_conditions,
        "Pression disponible (Pa)",
        "650", 2, 2
    )

    # ===================================
    # 4. MODE DE FONCTIONNEMENT
    # ===================================

    cadre_mode = section(
        "4. Mode de fonctionnement", 3
    )

    mode = ctk.StringVar(value="Hiver")
    boutons_mode = {}

    for colonne, nom_mode in enumerate(
        ["Hiver", "Été", "Mi-saison"]
    ):
        bouton = ctk.CTkButton(
            cadre_mode,
            text=nom_mode,
            height=50
        )
        bouton.grid(
            row=1,
            column=colonne,
            sticky="ew",
            padx=12,
            pady=12
        )
        boutons_mode[nom_mode] = bouton

    def choisir_mode(choix):
        mode.set(choix)

        for nom_mode, bouton in boutons_mode.items():
            bouton.configure(
                fg_color=(
                    "#1F6AA5"
                    if nom_mode == choix
                    else "#444444"
                )
            )

    for nom_mode, bouton in boutons_mode.items():
        bouton.configure(
            command=lambda m=nom_mode: choisir_mode(m)
        )

    choisir_mode("Hiver")

    # ===================================
    # 5. BOUTON CONTINUER
    # ===================================

    message = ctk.CTkLabel(
        contenu,
        text="",
        text_color="#FF5555"
    )
    message.pack(pady=5)

    def continuer():
        try:
            projet = {
                "nom": nom.get().strip(),
                "reference": reference.get().strip(),
                "type_cta": type_cta.get(),
                "debit": float(
                    debit.get().replace(",", ".")
                ),
                "temperature": float(
                    temperature.get().replace(",", ".")
                ),
                "temperature_cible": float(
                    temperature_cible.get().replace(",", ".")
                ),
                "humidite": float(
                    humidite.get().replace(",", ".")
                ),
                "humidite_cible": float(
                    humidite_cible.get().replace(",", ".")
                ),
                "pression": float(
                    pression.get().replace(",", ".")
                ),
                "mode": mode.get()
            }

            if not projet["nom"] or not projet["reference"]:
                message.configure(
                    text="Indique le nom et la référence du projet."
                )
                return

            if projet["debit"] <= 0 or projet["pression"] < 0:
                message.configure(
                    text="Vérifie le débit et la pression."
                )
                return

            if not (
                0 <= projet["humidite"] <= 100
                and 0 <= projet["humidite_cible"] <= 100
            ):
                message.configure(
                    text="Les humidités doivent être entre 0 et 100 %."
                )
                return

            ouvrir_construction(projet)

        except ValueError:
            message.configure(
                text="Entre des valeurs numériques valides."
            )

    ctk.CTkButton(
        contenu,
        text="Continuer vers la construction →",
        command=continuer,
        width=320,
        height=48,
        font=("Arial", 16, "bold")
    ).pack(pady=(10, 20))
