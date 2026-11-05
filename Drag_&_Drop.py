import tkinter as ttk
import tkinter as tk

# Dictionnaire pour stocker l'état de chaque module (True ou False)
# On utilise l'objet widget lui-même comme clé !
etats_modules = {}

# Fonction pour gérer le clic sur un module
def gerer_clic(e):
    w = e.widget
    
    # On récupère l'état actuel du module dans notre dictionnaire
    est_place = etats_modules[w]
    
    # Si le module n'est pas dans la CTA, on l'y place
    if est_place == False:
        etats_modules[w] = True  # On met à jour l'état
        w.place(relx=0.7, rely=0.3 + (w.i * 0.12), anchor="center")
    # Sinon, on le remet à sa position de départ à gauche
    else:
        etats_modules[w] = False  # On met à jour l'état
        w.place(relx=0.15, rely=0.2 + (w.i * 0.15), anchor="center")
        
    # On vérifie si TOUS les modules sont bien placés
    tous_places = True
    for m in modules:
        if etats_modules[m] == False:
            tous_places = False
            
    # On change la couleur du voyant selon le résultat
    if tous_places == True:
        light.config(bg="green")
    else:
        light.config(bg="red")

root = tk.Tk()
root.geometry("600x480")

# Zone CTA (encadré gris) placée au centre-droit
zone_cta = tk.Frame(root, width=220, height=260, bg="#ecf0f1", bd=2, relief="solid")
zone_cta.place(relx=0.7, rely=0.45, anchor="center")

# Titre de la CTA positionné avec relx/rely/anchor
titre = tk.Label(root, text="Emplacement CTA", bg="#ecf0f1", font=("Arial", 9, "bold"))
titre.place(relx=0.7, rely=0.22, anchor="center")

# Voyant lumineux positionné avec relx/rely/anchor
light = tk.Label(root, text="🟢", bg="red", font=("Arial", 16))
light.place(relx=0.7, rely=0.82, anchor="center")

# Création des 4 modules en boucle
modules = []
data = [
    ("#e74c3c", "Filtre G4"),
    ("#e67e22", "Bat. Chaude"),
    ("#f1c40f", "Bat. Froide"),
    ("#3498db", "Ventilateur"),
]

for i, (c, n) in enumerate(data):
    m = tk.Label(root, text=n, bg=c, fg="white", font=("Arial", 9, "bold"), width=13, height=2)
    # Position de départ à gauche avec relx/rely/anchor
    m.place(relx=0.15, rely=0.2 + (i * 0.15), anchor="center")
    
    m.i = i      # Numéro d'index (0, 1, 2 ou 3)
    
    # On initialise l'état de ce module précis dans le dictionnaire externe à False
    etats_modules[m] = False 
    
    m.bind("<Button-1>", gerer_clic)
    modules.append(m)

root.mainloop()
"""
-regarder discord pour mettre plus de modules de la CTA (voir discord,(humidificateur,2 moteurs ,batterie chaude/froide,etc...)) et utilise le modelde la CTA dispo sur discord.
-faire un ordre de passage des modules dans la CTA, pour pouvoir faire des erreur exemple(modules installé dans le mauvais ordre ou module manquant)
-insérer des images pour transformer les module (carré) en modules( réalité).Les images doive être stocké dans un bibliothèques nommé assets.
-faire un bouton approuver pur valider l'installation des modules dans la CTA et passer à la prochaine fenêtre.
-si possible faire une liste déroulante ou on peut choisir le type de module à installer dans la CTA.
-drag and drop (dernier recours)

ici on a utilisé un dictionaire externe pour stocker l'état de chaque module, ce qui est une bonne pratique pour éviter d'ajouter des attributs personnalisés aux widgets


 Tkinter. Cela permet de garder le code plus propre et de mieux gérer l'état des modules.
"""
