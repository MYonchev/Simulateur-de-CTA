from tkinter import messagebox, ttk
from tkinter import *
from PIL import Image, ImageTk

fenetre = Tk()
fenetre.title("Simulation CTA Simple Flux")
fenetre.geometry("1250x750")
fenetre.config(bg="#f4f6f7")

MODULES_DISPONIBLES = {
    "Filtre G4": "filtre.jfif",
    "Humidificateur": "humidificateur.jfif",
    "Batterie Froide": "batterie froide.jfif",
    "Batterie Chaude": "batterie chaude.jfif",
    "Moteur 1": "ventilo.jfif",
    "Moteur 2": "ventilo.jfif",
}

ORDRE_ATTENDU = {
    "1": "Filtre G4",
    "2": "Batterie Froide",
    "3": "Batterie Chaude",
    "4": "Humidificateur",
    "5": "Moteur 1",
    "6": "Moteur 2",
}

EMPLACEMENTS = {
    "1": {"x": 245, "y": 163, "l": 40, "h": 160, "occupant": None},
    "2": {"x": 310, "y": 163, "l": 85, "h": 160, "occupant": None},
    "3": {"x": 395, "y": 163, "l": 90, "h": 160, "occupant": None},
    "4": {"x": 510, "y": 163, "l": 145, "h": 160, "occupant": None},
    "5": {"x": 621, "y": 163, "l": 75, "h": 160, "occupant": None},
    "6": {"x": 710, "y": 163, "l": 95, "h": 160, "occupant": None},
}

etats_modules = {}
widgets_modules = {}
boutons_panel = {}
images_stock = {}

try:
    img_pil = Image.open("CTA.png").resize((950, 350))
    images_stock["fond"] = ImageTk.PhotoImage(img_pil)
    zone_cta = Label(fenetre, image=images_stock["fond"], bd=0)
except:
    zone_cta = Frame(fenetre, width=950, height=350, bg="#ecf0f1")

zone_cta.place(relx=0.55, rely=0.45, anchor="center", width=950, height=350)

Label(fenetre, text="Simulation CTA Simple Flux - 6 Modules", bg="#f4f6f7", font=("Arial", 11, "bold"), fg="#2c3e50").place(relx=0.55, rely=0.08, anchor="center")
indicateur = Label(fenetre, text="🔴", bg="#f4f6f7", font=("Arial", 22))
indicateur.place(relx=0.55, rely=0.82, anchor="center")
statut = Label(fenetre, text="État : Modules mal installés ou manquants", bg="#f4f6f7", fg="#c0392b", font=("Arial", 10, "italic"))
statut.place(relx=0.55, rely=0.89, anchor="center")

cadre_panel = LabelFrame(fenetre, text=" Modules disponibles ", bg="#ffffff", font=("Arial", 10, "bold"), bd=2, relief="groove")
cadre_panel.place(relx=0.08, rely=0.45, anchor="center", width=230, height=580)

def charger_image(nom_fichier, l, h):
    try:
        return ImageTk.PhotoImage(Image.open(nom_fichier).convert("RGBA").resize((l, h), Image.Resampling.LANCZOS))
    except:
        return None

def verifier_montage():
    places_occupees = sum(1 for e in EMPLACEMENTS.values() if e["occupant"] is not None)
    total = len(ORDRE_ATTENDU)
    
    if places_occupees == total:
        correct = all(EMPLACEMENTS[s]["occupant"] == ORDRE_ATTENDU[s] for s in ORDRE_ATTENDU)
        if correct:
            indicateur.config(text="🟢")
            statut.config(text="Parfait ! Tous les modules sont à la bonne place.", fg="#27ae60")
            return True
        else:
            indicateur.config(text="🟠")
            statut.config(text="Tous les slots sont pris, mais l'ordre est incorrect.", fg="#d35400")
            return False
    else:
        indicateur.config(text="🔴" if places_occupees == 0 else "🟠")
        msg = "La CTA est vide." if places_occupees == 0 else f"Modules positionnés ({places_occupees}/{total} en place)."
        statut.config(text=msg, fg="#c0392b")
        return False

def selectionner_module(nom):
    if etats_modules.get(nom, False): return
    slot_libre = next((s for s, inf in EMPLACEMENTS.items() if inf["occupant"] is None), None)
    
    if not slot_libre:
        messagebox.showwarning("Attention", "Tous les emplacements sont occupés !")
        return

    etats_modules[nom] = True
    EMPLACEMENTS[slot_libre]["occupant"] = nom
    boutons_panel[nom].config(state="disabled", bg="#d5d8dc", text=f" {nom}\n (Placé)")

    inf = EMPLACEMENTS[slot_libre]
    if nom not in widgets_modules:
        w = Label(fenetre, bg="#ffffff", bd=0, cursor="hand2")
        w.nom = nom
        w.bind("<Button-1>", gerer_retrait)
        widgets_modules[nom] = w
    
    w = widgets_modules[nom]
    w.slot = slot_libre
    
    img_tk = charger_image(MODULES_DISPONIBLES[nom], inf["l"], inf["h"])
    if img_tk:
        images_stock[f"cta_{nom}"] = img_tk
        w.config(image=img_tk)

    x = (zone_cta.winfo_rootx() - fenetre.winfo_rootx()) + inf["x"]
    y = (zone_cta.winfo_rooty() - fenetre.winfo_rooty()) + inf["y"]
    w.place(x=x, y=y, anchor="center")
    verifier_montage()

def gerer_retrait(event):
    nom, slot_id = event.widget.nom, event.widget.slot
    etats_modules[nom] = False
    EMPLACEMENTS[slot_id]["occupant"] = None
    if nom in widgets_modules:
        widgets_modules[nom].place_forget()
        del widgets_modules[nom]
    if nom in boutons_panel:
        boutons_panel[nom].config(state="normal", bg="#f8f9f9", text=f" {nom}")
    verifier_montage()

def fabriquer_commande(nom_module):
    def action():
        selectionner_module(nom_module)
    return action

for index, nom_module in enumerate(ORDRE_ATTENDU.values()):
    img_mini = charger_image(MODULES_DISPONIBLES[nom_module], 35, 28)
    if img_mini: images_stock[f"mini_{nom_module}"] = img_mini

    btn = Button(cadre_panel, text=f" {nom_module}", image=images_stock.get(f"mini_{nom_module}"),
                 compound="left", font=("Arial", 7, "bold"), bg="#f8f9f9" if img_mini else "#bdc3c7",
                 anchor="w", command=fabriquer_commande(nom_module))
    btn.place(relx=0.03, rely=0.02 + (index * 0.15), relwidth=0.94, height=40)
    boutons_panel[nom_module] = btn
    etats_modules[nom_module] = False

def valider():
    places = sum(1 for e in EMPLACEMENTS.values() if e["occupant"] is not None)
    if places < len(ORDRE_ATTENDU):
        messagebox.showerror("Incomplet", f"Il manque des modules ({places}/{len(ORDRE_ATTENDU)} placés).")
    elif verifier_montage():
        messagebox.showinfo("Succès", "Bravo ! L'ordre des modules dans la CTA est correct !")
    else:
        messagebox.showerror("Erreur", "L'ordre des modules n'est pas correct.")

Button(fenetre, text="Valider l'installation", bg="#2ecc71", fg="white",
       font=("Arial", 11, "bold"), padx=10, pady=5, command=valider).place(relx=0.55, rely=0.95, anchor="center")

fenetre.mainloop()
