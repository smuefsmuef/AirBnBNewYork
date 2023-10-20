# Importation des modules nécessaires
from CTkMessagebox import CTkMessagebox  # Importe une boîte de dialogue personnalisée
import customtkinter as ctk  # Importe le module customtkinter pour créer l'interface graphique
import os  # Importe le module os pour exécuter un autre script Python

# Configure l'apparence et le thème de l'interface
ctk.set_appearance_mode("System")  # Modes : system (par défaut), light, dark
ctk.set_default_color_theme("blue")  # Thèmes : blue (par défaut), dark-blue, green

# Crée une instance de la fenêtre principale
app = ctk.CTk()
app.title("Log In")  # Définit le titre de la fenêtre

# Obtient la largeur et la hauteur de l'écran
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calcule les coordonnées x et y pour centrer la fenêtre
centrage_horizontal = (screen_width - 1200) // 2
centrage_vertical = (screen_height - 600) // 2

# Définit la taille et la position de la fenêtre
app.geometry(f"1200x600+{centrage_horizontal}+{centrage_vertical}")

# Définit une fonction pour vérifier le mot de passe
def verification_mdp():
    if champ.get() == "TC1027":
        app.withdraw()  # Masque la fenêtre principale
        os.popen("python fenetre2.py")  # Exécute un autre script Python (fenetre2.py)
    else:
        # Affiche un message d'erreur centré sur l'écran de l'application
        error_box = CTkMessagebox(title="Error", message="Error, wrong password !", icon="cancel")
        
        # Obtient la taille de la fenêtre de l'erreur
        error_width = error_box.winfo_width()
        error_height = error_box.winfo_height()

        # Calcule les coordonnées x et y pour centrer la fenêtre d'erreur
        error_x = (app.winfo_width() - error_width) // 2
        error_y = (app.winfo_height() - error_height) // 2

        # Définit les coordonnées de la fenêtre d'erreur pour la centrer dans l'application
        error_box.geometry(f"+{error_x}+{error_y}")
        error_box.wait_window()  # Attend que la fenêtre d'erreur soit fermée

# Crée un cadre à l'intérieur de la fenêtre principale
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both")

# Crée une étiquette dans le cadre pour le message "Enter your password :"
label = ctk.CTkLabel(master=frame, text="Enter your password : ")
label.pack(pady=(12, 10))

# Crée un champ de saisie pour entrer le mot de passe
champ = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
champ.pack(pady=(12, 10))

# Crée un bouton pour déclencher la vérification du mot de passe
button = ctk.CTkButton(master=frame, text="Log In", command=verification_mdp)
button.pack(pady=(12, 10))

# Lance la boucle principale de l'interface graphique
app.mainloop()
