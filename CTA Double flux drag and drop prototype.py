from tkinter import messagebox, ttk
from tkinter import *
from PIL import Image, ImageTk

fenetre_principale = Tk()
fenetre_principale.title("Simulation CTA Double Flux - Vérification de l'ordre")
fenetre_principale.geometry("1250x750")
fenetre_principale.config(bg="#f4f6f7")

# --- DONNÉES ---
MODULES_DISPONIBLES = {
    "Filtre Extraction": "filtre.jfif",
    "Ventilateur Extraction": "ventilo.jfif",
    "Récupérateur": "recuperateurs_chaleur.png",
    "Filtre Air Neuf": "filtration.jpg",
    "Batterie Froide": "batterie froide.jfif",
    "Batterie Chaude": "batterie chaude.jfif",
    "Ventilateur Soufflage": "ventilo.jfif",
    "Humidificateur": "humidificateur.jfif",
}

ORDRE_ATTENDU_MODULES = {
    "1": "Filtre Extraction",
    "2": "Récupérateur",
    "3": "Ventilateur Extraction",
    "4": "Filtre Air Neuf",
    "5": "Batterie Froide",
    "6": "Batterie Chaude",
    "7": "Ventilateur Soufflage",
    "8": "Humidificateur",
}

CONFIGURATION_EMPLACEMENTS = {
    "1": {"x": 220, "y": 123, "largeur": 40, "hauteur": 90, "occupant": None},
    "2": {"x": 345, "y": 170, "largeur": 100, "hauteur": 180, "occupant": None},
    "3": {"x": 415, "y": 123, "largeur": 35, "hauteur": 90, "occupant": None},
    "4": {"x": 240, "y": 215, "largeur": 110, "hauteur": 90, "occupant": None},
    "5": {"x": 450, "y": 215, "largeur": 105, "hauteur": 90, "occupant": None},
    "6": {"x": 554, "y": 215, "largeur": 105, "hauteur": 90, "occupant": None},
    "7": {"x": 680, "y": 215, "largeur": 78, "hauteur": 90, "occupant": None},
    "8": {"x": 750, "y": 215, "largeur": 55, "hauteur": 90, "occupant": None},
}

dictionnaire_etats_modules = {}
dictionnaire_widgets_modules = {}
dictionnaire_boutons_panel = {}
dictionnaire_images = {}

donnees_glissement = {"nom_module_en_cours": None}


# --- INTERFACE GRAPHIQUE DE BASE ---
try:
    image_cta_pil = Image.open("CTA_double.png").resize((950, 350))
    dictionnaire_images["fond_cta"] = ImageTk.PhotoImage(image_cta_pil)
    zone_centrale_cta = Label(fenetre_principale, image=dictionnaire_images["fond_cta"], bd=0)
except Exception:
    zone_centrale_cta = Frame(fenetre_principale, width=950, height=350, bg="#ecf0f1")

zone_centrale_cta.place(relx=0.55, rely=0.45, anchor="center", width=950, height=350)

Label(
    fenetre_principale,
    text="Simulation CTA Double Flux - Vérification de l'ordre",
    bg="#f4f6f7",
    font=("Arial", 11, "bold"),
    fg="#2c3e50"
).place(relx=0.55, rely=0.08, anchor="center")

indicateur_lumineux = Label(fenetre_principale, text="🔴", bg="#f4f6f7", font=("Arial", 22))
indicateur_lumineux.place(relx=0.55, rely=0.82, anchor="center")

label_statut = Label(
    fenetre_principale,
    text="État : Modules mal installés ou manquants",
    bg="#f4f6f7",
    fg="#c0392b",
    font=("Arial", 10, "italic"),
)
label_statut.place(relx=0.55, rely=0.89, anchor="center")

cadre_panneau_lateral = LabelFrame(
    fenetre_principale,
    text=" Modules disponibles ",
    bg="#ffffff",
    font=("Arial", 10, "bold"),
    bd=2,
    relief="groove",
)
cadre_panneau_lateral.place(relx=0.08, rely=0.45, anchor="center", width=230, height=580)


# --- FONCTIONS UTILITAIRES ---
def charger_et_redimensionner_image(nom_fichier, largeur, hauteur):
    try:
        image_pil = Image.open(nom_fichier).convert("RGBA").resize((largeur, hauteur), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image_pil)
    except Exception:
        return None


def verifier_montage_reel():
    for identifiant_slot, nom_attendu in ORDRE_ATTENDU_MODULES.items():
        if CONFIGURATION_EMPLACEMENTS[identifiant_slot]["occupant"] != nom_attendu:
            return False
    return True


def verifier_montage():
    nombre_places_occupees = sum(1 for emplacement in CONFIGURATION_EMPLACEMENTS.values() if emplacement["occupant"] is not None)
    
    if nombre_places_occupees == 8:
        if verifier_montage_reel():
            indicateur_lumineux.config(text="🟢")
            label_statut.config(text="Parfait ! Tous les modules sont à la bonne place.", fg="#27ae60")
            return True
        else:
            indicateur_lumineux.config(text="🟠")
            label_statut.config(text="Tous les slots sont pris, mais l'ordre est incorrect.", fg="#d35400")
            return False
    elif nombre_places_occupees > 0:
        indicateur_lumineux.config(text="🔴")
        label_statut.config(text=f"Modules positionnés ({nombre_places_occupees}/8 en place).", fg="#c0392b")
        return False
    else:
        indicateur_lumineux.config(text="🔴")
        label_statut.config(text="La CTA est vide.", fg="#c0392b")
        return False


# --- GESTION DU DRAG & DROP (SANS LAMBDA) ---
def demarrer_glissement(evenement):
    nom_module = evenement.widget.nom_module_associe
    donnees_glissement["nom_module_en_cours"] = nom_module


def en_cours_de_glissement(evenement):
    nom_module = donnees_glissement["nom_module_en_cours"]
    if not nom_module:
        return
    
    if not dictionnaire_etats_modules[nom_module]:
        dictionnaire_etats_modules[nom_module] = True
        creer_widget_cta(nom_module)
        if nom_module in dictionnaire_boutons_panel:
            dictionnaire_boutons_panel[nom_module].config(state="disabled", bg="#d5d8dc", text=f" {nom_module}\n (Déjà pris)")

    widget_cta = dictionnaire_widgets_modules[nom_module]
    position_x_relative = fenetre_principale.winfo_pointerx() - fenetre_principale.winfo_rootx()
    position_y_relative = fenetre_principale.winfo_pointery() - fenetre_principale.winfo_rooty()
    widget_cta.place(x=position_x_relative, y=position_y_relative, anchor="center")


def arreter_glissement(evenement):
    nom_module = donnees_glissement["nom_module_en_cours"]
    if not nom_module:
        return
    
    widget_cta = dictionnaire_widgets_modules[nom_module]
    x_relatif_cta = fenetre_principale.winfo_pointerx() - zone_centrale_cta.winfo_rootx()
    y_relatif_cta = fenetre_principale.winfo_pointery() - zone_centrale_cta.winfo_rooty()
    
    largeur_cta = zone_centrale_cta.winfo_width()
    hauteur_cta = zone_centrale_cta.winfo_height()
    
    if 0 <= x_relatif_cta <= largeur_cta and 0 <= y_relatif_cta <= hauteur_cta:
        # Trouver l'emplacement le plus proche
        slot_le_plus_proche = min(
            CONFIGURATION_EMPLACEMENTS.keys(),
            key=lambda id_slot: abs(CONFIGURATION_EMPLACEMENTS[id_slot]["x"] - x_relatif_cta) + abs(CONFIGURATION_EMPLACEMENTS[id_slot]["y"] - y_relatif_cta)
        )
        
        # Libérer l'ancien slot si le module y était déjà
        for id_slot, data in CONFIGURATION_EMPLACEMENTS.items():
            if data["occupant"] == nom_module:
                data["occupant"] = None

        # Si le slot choisi contenait déjà un autre module, on le renvoie au panneau
        occupant_precedent = CONFIGURATION_EMPLACEMENTS[slot_le_plus_proche]["occupant"]
        if occupant_precedent and occupant_precedent != nom_module:
            dictionnaire_etats_modules[occupant_precedent] = False
            if occupant_precedent in dictionnaire_widgets_modules:
                dictionnaire_widgets_modules[occupant_precedent].place_forget()
                del dictionnaire_widgets_modules[occupant_precedent]
            if occupant_precedent in dictionnaire_boutons_panel:
                dictionnaire_boutons_panel[occupant_precedent].config(state="normal", bg="#f8f9f9", text=f" {occupant_precedent}")

        # Placer le module dans le nouveau slot
        CONFIGURATION_EMPLACEMENTS[slot_le_plus_proche]["occupant"] = nom_module
        infos_emplacement = CONFIGURATION_EMPLACEMENTS[slot_le_plus_proche]

        mettre_a_jour_image_module(widget_cta, nom_module, infos_emplacement["largeur"], infos_emplacement["hauteur"])
        
        target_root_x = (zone_centrale_cta.winfo_rootx() - fenetre_principale.winfo_rootx()) + infos_emplacement["x"]
        target_root_y = (zone_centrale_cta.winfo_rooty() - fenetre_principale.winfo_rooty()) + infos_emplacement["y"]
        
        widget_cta.place(x=target_root_x, y=target_root_y, anchor="center")
    else:
        # Si on lâche hors de la zone CTA, on annule le placement
        dictionnaire_etats_modules[nom_module] = False
        for id_slot, data in CONFIGURATION_EMPLACEMENTS.items():
            if data["occupant"] == nom_module:
                data["occupant"] = None
        widget_cta.place_forget()
        del dictionnaire_widgets_modules[nom_module]
        if nom_module in dictionnaire_boutons_panel:
            dictionnaire_boutons_panel[nom_module].config(state="normal", bg="#f8f9f9", text=f" {nom_module}")

    donnees_glissement["nom_module_en_cours"] = None
    verifier_montage()


def creer_widget_cta(nom_module):
    if nom_module in dictionnaire_widgets_modules:
        widget_cta = dictionnaire_widgets_modules[nom_module]
    else:
        widget_cta = Label(fenetre_principale, bg="#ffffff", cursor="hand2", bd=0)
        widget_cta.nom_module_associe = nom_module
        widget_cta.bind("<Button-1>", demarrer_glissement)
        widget_cta.bind("<B1-Motion>", en_cours_de_glissement)
        widget_cta.bind("<ButtonRelease-1>", arreter_glissement)
        dictionnaire_widgets_modules[nom_module] = widget_cta

    mettre_a_jour_image_module(widget_cta, nom_module, 75, 120)


def mettre_a_jour_image_module(widget_cta, nom_module, largeur, hauteur):
    fichier_image = MODULES_DISPONIBLES[nom_module]
    image_tk = charger_et_redimensionner_image(fichier_image, largeur, hauteur)
    if image_tk:
        dictionnaire_images[f"cta_{nom_module}"] = image_tk
        widget_cta.config(image=image_tk)


# --- CRÉATION AUTOMATISÉE DES BOUTONS LATÉRAUX ---
for index, (nom_module, fichier_image) in enumerate(MODULES_DISPONIBLES.items()):
    image_miniature = charger_et_redimensionner_image(fichier_image, 35, 28)
    if image_miniature:
        dictionnaire_images[f"mini_{nom_module}"] = image_miniature

    bouton_module = Button(
        cadre_panneau_lateral,
        text=f" {nom_module}",
        image=dictionnaire_images.get(f"mini_{nom_module}"),
        compound="left",
        font=("Arial", 7, "bold"),
        bg="#f8f9f9" if image_miniature else "#bdc3c7",
        anchor="w"
    )
    
    # Attacher le nom du module directement à l'objet bouton pour s'passer de lambda
    bouton_module.nom_module_associe = nom_module
    bouton_module.bind("<Button-1>", demarrer_glissement)
    bouton_module.bind("<B1-Motion>", en_cours_de_glissement)
    bouton_module.bind("<ButtonRelease-1>", arreter_glissement)
    
    bouton_module.place(relx=0.03, rely=0.02 + (index * 0.12), relwidth=0.94, height=45)
    dictionnaire_boutons_panel[nom_module] = bouton_module
    dictionnaire_etats_modules[nom_module] = False


# --- BOUTON DE VALIDATION GLOBAL ---
def valider_installation():
    nombre_places_occupees = sum(1 for emplacement in CONFIGURATION_EMPLACEMENTS.values() if emplacement["occupant"] is not None)
    if nombre_places_occupees < 8:
        messagebox.showerror(
            "Incomplet",
            f"Il manque des modules ({nombre_places_occupees}/8 placés)."
        )
    elif verifier_montage_reel():
        messagebox.showinfo(
            "Succès",
            "Bravo ! L'ordre des modules dans la CTA est parfaitement correct !",
        )
    else:
        messagebox.showerror(
            "Erreur d'ordre",
            "L'ordre des modules dans les emplacements n'est pas correct. Vérifiez votre montage.",
        )


bouton_validation = Button(
    fenetre_principale,
    text="Valider l'installation",
    bg="#2ecc71",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5,
    command=valider_installation,
)
bouton_validation.place(relx=0.55, rely=0.95, anchor="center")

fenetre_principale.mainloop()