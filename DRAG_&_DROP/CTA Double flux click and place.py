from tkinter import messagebox, ttk
from tkinter import *
from PIL import Image, ImageTk

fenetre_principale = Tk()
fenetre_principale.title("Simulation CTA Double Flux - Placement par Clic")
fenetre_principale.geometry("1250x750")
fenetre_principale.config(bg="#f4f6f7")

# --- DONNÉES (les images doivent être dans le même dossier que le script) ---
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

dictionnaire_images = {}
dictionnaire_widgets_modules = {}
dictionnaire_boutons_panel = {}


# --- INTERFACE GRAPHIQUE DE BASE ---
try:
    image_cta_pil = Image.open("CTA_double.png").resize((950, 350))
    dictionnaire_images["fond_cta"] = ImageTk.PhotoImage(image_cta_pil)
    zone_centrale_cta = Label(fenetre_principale, image=dictionnaire_images["fond_cta"], bd=0)
except Exception:
    zone_centrale_cta = Frame(fenetre_principale, width=950, height=350, bg="#ecf0f1")

zone_centrale_cta.place(relx=0.55, rely=0.45, anchor="center", width=950, height=350)

Label(fenetre_principale, text="Simulation CTA Double Flux - Placement par Clic", bg="#f4f6f7", font=("Arial", 11, "bold"), fg="#2c3e50").place(relx=0.55, rely=0.08, anchor="center")

indicateur_lumineux = Label(fenetre_principale, text="🔴", bg="#f4f6f7", font=("Arial", 22))
indicateur_lumineux.place(relx=0.55, rely=0.82, anchor="center")

label_statut = Label(fenetre_principale, text="État : Modules mal installés ou manquants", bg="#f4f6f7", fg="#c0392b", font=("Arial", 10, "italic"))
label_statut.place(relx=0.55, rely=0.89, anchor="center")

cadre_panneau_lateral = LabelFrame(fenetre_principale, text=" Modules disponibles ", bg="#ffffff", font=("Arial", 10, "bold"), bd=2, relief="groove")
cadre_panneau_lateral.place(relx=0.08, rely=0.45, anchor="center", width=230, height=580)


# --- FONCTIONS UTILITAIRES ---
def charger_et_redimensionner_image(nom_fichier, largeur, hauteur):
    try:
        image_pil = Image.open(nom_fichier).convert("RGBA").resize((largeur, hauteur), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image_pil)
    except Exception:
        return None


def verifier_conformite_montage():
    nombre_places_occupees = sum(1 for emplacement in CONFIGURATION_EMPLACEMENTS.values() if emplacement["occupant"] is not None)
    
    if nombre_places_occupees < 8:
        indicateur_lumineux.config(text="🔴" if nombre_places_occupees == 0 else "🟠")
        message_etat = "La CTA est vide." if nombre_places_occupees == 0 else f"Modules positionnés ({nombre_places_occupees}/8 en place)."
        label_statut.config(text=message_etat, fg="#c0392b")
        return False

    ordre_est_correct = all(CONFIGURATION_EMPLACEMENTS[id_emplacement]["occupant"] == nom_attendu for id_emplacement, nom_attendu in ORDRE_ATTENDU_MODULES.items())
    
    if ordre_est_correct:
        indicateur_lumineux.config(text="🟢")
        label_statut.config(text="Parfait ! Tous les modules sont à la bonne place.", fg="#27ae60")
        return True
    else:
        indicateur_lumineux.config(text="🟠")
        label_statut.config(text="Tous les slots sont pris, mais l'ordre est incorrect.", fg="#d35400")
        return False


# --- GESTION DES CLICS ---
def selectionner_module(nom_module):
    identifiant_slot_libre = next((id_slot for id_slot, infos in CONFIGURATION_EMPLACEMENTS.items() if infos["occupant"] is None), None)
    
    if not identifiant_slot_libre:
        messagebox.showwarning("Attention", "Tous les emplacements sont déjà occupés !")
        return

    CONFIGURATION_EMPLACEMENTS[identifiant_slot_libre]["occupant"] = nom_module
    dictionnaire_boutons_panel[nom_module].config(state="disabled", bg="#d5d8dc", text=f" {nom_module}\n (Placé)")

    if nom_module not in dictionnaire_widgets_modules:
        widget_module = Label(fenetre_principale, bg="#ffffff", bd=0, cursor="hand2")
        widget_module.nom_module_associe = nom_module
        widget_module.identifiant_slot_associe = identifiant_slot_libre
        widget_module.bind("<Button-1>", gerer_clic_retrait_module)
        dictionnaire_widgets_modules[nom_module] = widget_module
    
    widget_module = dictionnaire_widgets_modules[nom_module]
    infos_emplacement = CONFIGURATION_EMPLACEMENTS[identifiant_slot_libre]
    
    image_tk = charger_et_redimensionner_image(MODULES_DISPONIBLES[nom_module], infos_emplacement["largeur"], infos_emplacement["hauteur"])
    if image_tk:
        dictionnaire_images[f"cta_{nom_module}"] = image_tk
        widget_module.config(image=image_tk)

    position_x = (zone_centrale_cta.winfo_rootx() - fenetre_principale.winfo_rootx()) + infos_emplacement["x"]
    position_y = (zone_centrale_cta.winfo_rooty() - fenetre_principale.winfo_rooty()) + infos_emplacement["y"]
    widget_module.place(x=position_x, y=position_y, anchor="center")

    verifier_conformite_montage()


def gerer_clic_retrait_module(evenement_clic):
    nom_module = evenement_clic.widget.nom_module_associe
    identifiant_slot = evenement_clic.widget.identifiant_slot_associe
    retirer_module(nom_module, identifiant_slot)


def retirer_module(nom_module, identifiant_slot):
    CONFIGURATION_EMPLACEMENTS[identifiant_slot]["occupant"] = None

    if nom_module in dictionnaire_widgets_modules:
        dictionnaire_widgets_modules[nom_module].place_forget()
        del dictionnaire_widgets_modules[nom_module]

    if nom_module in dictionnaire_boutons_panel:
        dictionnaire_boutons_panel[nom_module].config(state="normal", bg="#f8f9f9", text=f" {nom_module}")

    verifier_conformite_montage()


def valider_installation_globale():
    nombre_places_occupees = sum(1 for emplacement in CONFIGURATION_EMPLACEMENTS.values() if emplacement["occupant"] is not None)
    if nombre_places_occupees < 8:
        messagebox.showerror("Incomplet", f"Il manque des modules ({nombre_places_occupees}/8 placés).")
    elif verifier_conformite_montage():
        messagebox.showinfo("Succès", "Bravo ! L'ordre des modules dans la CTA est parfaitement correct !")
    else:
        messagebox.showerror("Erreur d'ordre", "L'ordre des modules dans les emplacements n'est pas correct.")


def fabriquer_commande_bouton(nom_module):
    def action_clic():
        selectionner_module(nom_module)
    return action_clic


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
        anchor="w",
        command=fabriquer_commande_bouton(nom_module)
    )
    bouton_module.place(relx=0.03, rely=0.02 + (index * 0.12), relwidth=0.94, height=45)
    dictionnaire_boutons_panel[nom_module] = bouton_module


# --- BOUTON DE VALIDATION GLOBAL ---
Button(
    fenetre_principale, text="Valider l'installation", bg="#2ecc71", fg="white",
    font=("Arial", 11, "bold"), padx=10, pady=5, command=valider_installation_globale
).place(relx=0.55, rely=0.95, anchor="center")

fenetre_principale.mainloop()
