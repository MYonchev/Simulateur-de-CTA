import os
import tkinter as tk
from tkinter import messagebox, ttk

# --- CONFIGURATION DU DOSSIER ASSETS ---
ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
  os.makedirs(ASSETS_DIR)

"""
image de secours voir si c'est nécessaire

"""
# Fonction utilitaire pour créer des images de secours si les fichiers n'existent pas
def creer_image_secours(nom_fichier, texte, couleur):
  chemin = os.path.join(ASSETS_DIR, nom_fichier)
  if not os.path.exists(chemin):
    try:
      from PIL import Image, ImageDraw, ImageFont

      img = Image.new("RGBA", (140, 50), color=couleur)
      d = ImageDraw.Draw(img)
      d.rectangle([0, 0, 139, 49], outline="white", width=2)
      d.text((10, 18), texte, fill="white")
      img.save(chemin)
    except ImportError:
      pass


root = tk.Tk()
root.setTitle = "Simulation CTA - Montage des Modules"
root.geometry("850x600")
root.config(bg="#f4f6f7")

# --- DÉFINITION DE L'ORDRE ATTENDU DANS LA CTA ---
# Ordre logique de bas en haut ou de gauche à droite dans la CTA
ORDRE_ATTENDU = [
    "Filtre G4",
    "Humidificateur",
    "Batterie Froide",
    "Batterie Chaude",
    "Moteur 1",
    "Moteur 2",
]

# Données des modules avec leurs couleurs de secours et noms de fichiers d'images
modules_data = {
    "Filtre G4": {"couleur": "#e74c3c", "img": "filtre_g4.png"},
    "Humidificateur": {"couleur": "#1abc9c", "img": "humidificateur.png"},
    "Batterie Froide": {"couleur": "#3498db", "img": "batterie_froide.png"},
    "Batterie Chaude": {"couleur": "#e67e22", "img": "batterie_chaude.png"},
    "Moteur 1": {"couleur": "#9b59b6", "img": "moteur1.png"},
    "Moteur 2": {"couleur": "#34495e", "img": "moteur2.png"},
}
"""
image de secours voir si c'est nécessaire

"""

# Création des images de secours si elles n'existent pas
for nom, info in modules_data.items():
  creer_image_secours(info["img"], nom, info["couleur"])

# Dictionnaires de stockage
etats_modules = {}  # nom -> True/False (dans la CTA ou non)
objets_modules = {}  # nom -> widget Label
images_tk = {}  # Cache pour éviter que le Garbage Collector supprime les images

# --- ZONE CTA (Emplacement d'accueil) ---
zone_cta = tk.Frame(root, width=280, height=450, bg="#ecf0f1", bd=3, relief="solid")
zone_cta.place(relx=0.65, rely=0.48, anchor="center")

titre_cta = tk.Label(
    root,
    text="Emplacement CTA (Ordre requis)",
    bg="#f4f6f7",
    font=("Arial", 11, "bold"),
)
titre_cta.place(relx=0.65, rely=0.18, anchor="center")

# Voyant lumineux et message d'erreur
light = tk.Label(root, text="🔴", bg="#f4f6f7", font=("Arial", 20))
light.place(relx=0.88, rely=0.48, anchor="center")

label_statut = tk.Label(
    root,
    text="État : Modules mal installés ou manquants",
    bg="#f4f6f7",
    fg="#c0392b",
    font=("Arial", 10, "italic"),
)
label_statut.place(relx=0.65, rely=0.78, anchor="center")


# --- FONCTION DE MISE À JOUR ET VÉRIFICATION ---
def verifier_montage():
  # Récupérer les modules actuellement placés dans la CTA, triés par leur position verticale (rely)
  modules_places = []
  for nom, w in objets_modules.items():
    if etats_modules[nom] == True:
      # On stocke le widget et son nom avec sa position y actuelle
      modules_places.append((w.winfo_y(), nom))

  # Trier par ordre de haut en bas dans la CTA
  modules_places.sort(key=lambda x: x[0])
  ordre_actuel = [nom for _, nom in modules_places]

  # Vérification
  if ordre_actuel == ORDRE_ATTENDU:
    light.config(text="🟢")
    label_statut.config(
        text="Montage correct ! Prêt à valider.", fg="#27ae60"
    )
    return True
  else:
    light.config(text="🔴")
    if len(ordre_actuel) < len(ORDRE_ATTENDU):
      label_statut.config(
          text="Il manque des modules dans la CTA.", fg="#c0392b"
      )
    else:
      label_statut.config(
          text="Erreur : Ordre des modules incorrect !", fg="#c0392b"
      )
    return False


# --- GESTION DU CLIC SUR UN MODULE ---
def basculer_module(nom):
  est_place = etats_modules[nom]
  w = objets_modules[nom]

  if not est_place:
    # On le place dans la CTA (en cherchant la prochaine place libre de bas en haut)
    nb_deja_places = sum(1 for v in etats_modules.values() if v)
    if nb_deja_places >= len(ORDRE_ATTENDU):
      messagebox.showwarning(
          "CTA Pleine", "Tous les emplacements de la CTA sont occupés !"
      )
      return

    etats_modules[nom] = True
    # Calcul d'une position empilée dans la CTA
    w.place(relx=0.65, rely=0.28 + (nb_deja_places * 0.08), anchor="center")
  else:
    # On le remet à sa position initiale à gauche
    etats_modules[nom] = False
    index_origine = list(modules_data.keys()).index(nom)
    w.place(relx=0.18, rely=0.25 + (index_origine * 0.09), anchor="center")

  verifier_montage()


# --- LISTE DÉROULANTE (Sélection rapide) ---
label_combo = tk.Label(
    root,
    text="Sélectionner un module à ajouter :",
    bg="#f4f6f7",
    font=("Arial", 9, "bold"),
)
label_combo.place(relx=0.18, rely=0.83, anchor="center")

combo_modules = ttk.Combobox(
    root, values=list(modules_data.keys()), state="readonly", width=18
)
combo_modules.place(relx=0.18, rely=0.88, anchor="center")


def ajouter_depuis_combo(event):
  selection = combo_modules.get()
  if selection and not etats_modules[selection]:
    basculer_module(selection)
  combo_modules.set("")  # Reset la sélection


combo_modules.bind("<<ComboboxSelected>>", ajouter_depuis_combo)


# --- CRÉATION DES MODULES (PANNEAU DE GAUCHE) ---
for i, (nom, info) in enumerate(modules_data.items()):
  # Chargement de l'image
  chemin_img = os.path.join(ASSETS_DIR, info["img"])
  try:
    img = tk.PhotoImage(file=chemin_img)
    images_tk[nom] = img
    m = tk.Label(root, image=img, bg="#f4f6f7", cursor="hand2")
  except Exception:
    # Fallback texte si l'image ne charge pas
    m = tk.Label(
        root,
        text=nom,
        bg=info["couleur"],
        fg="white",
        font=("Arial", 9, "bold"),
        width=15,
        height=2,
        cursor="hand2",
    )

  # Position initiale à gauche
  m.place(relx=0.18, rely=0.25 + (i * 0.09), anchor="center")

  etats_modules[nom] = False
  objets_modules[nom] = m

  # Associer le clic sur le module (fermeture de closure avec un lambda)
  m.bind("<Button-1>", lambda e, n=nom: basculer_module(n))


# --- BOUTON APROUVER ---
def valider_installation():
  if verifier_montage():
    messagebox.showinfo(
        "Succès",
        "Installation validée avec succès !\nPassage à la fenêtre"
        " suivante...",
    )
    # Ici, vous pouvez détruire la fenêtre actuelle et lancer la suite :
    # root.destroy()
    # lancer_fenetre_suivante()
  else:
    messagebox.showerror(
        "Erreur d'installation",
        "Impossible de valider : l'ordre des modules dans la CTA est incorrect"
        " ou incomplet.",
    )


btn_approuver = tk.Button(
    root,
    text="Approuver l'installation",
    bg="#2ecc71",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5,
    command=valider_installation,
)
btn_approuver.place(relx=0.65, rely=0.92, anchor="center")

root.mainloop()


"""
# à propos de ce code:
-la fenetre de scrolling(pas nécessaire à l'état actuel) suprime si pas nécessaire
-images de secours vérifier si c'est nécessaire
-réparer l'importation des images pour qu'elles soient bien dans le dossier assets
-!!!!!!! comprendre le code car il est long et cécessite une relecture et une compréhension pour pouvoir le modifier et l'adapter à nos besoins!!!!!


---------------------------------------------------
-regarder discord pour mettre plus de modules de la CTA (voir discord,(humidificateur,2 moteurs ,batterie chaude/froide,etc...)) et utilise le modelde la CTA dispo sur discord.
-faire un ordre de passage des modules dans la CTA, pour pouvoir faire des erreur exemple(modules installé dans le mauvais ordre ou module manquant)
-insérer des images pour transformer les module (carré) en modules( réalité).Les images doive être stocké dans un bibliothèques nommé assets.
-faire un bouton approuver pur valider l'installation des modules dans la CTA et passer à la prochaine fenêtre.
-si possible faire une liste déroulante ou on peut choisir le type de module à installer dans la CTA.
-drag and drop (dernier recours)

ici on a utilisé un dictionaire externe pour stocker l'état de chaque module, ce qui est une bonne pratique pour éviter d'ajouter des attributs personnalisés aux widgets


 Tkinter. Cela permet de garder le code plus propre et de mieux gérer l'état des modules.
"""