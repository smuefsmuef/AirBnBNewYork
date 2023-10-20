import customtkinter as ctk
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# Function to return to the menu
def return_to_menu():
    app3.withdraw()
    os.popen("python fenetre2.py")

# Set customtkinter appearance and color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create the main CTk window
app3 = ctk.CTk()
app3.title("Second Window")

# Configure grid row and column weights
app3.grid_rowconfigure(0, weight=0)
app3.grid_rowconfigure(1, weight=1)
app3.grid_columnconfigure(0, weight=0)
app3.grid_columnconfigure(1, weight=1)

# Get the screen width and height
screen_width = app3.winfo_screenwidth()
screen_height = app3.winfo_screenheight()

# Calculate coordinates to center the window
horizontal_centering = (screen_width - 1200) // 2
vertical_centering = (screen_height - 600) // 2
app3.geometry(f"1200x600+{horizontal_centering}+{vertical_centering}")

# Frame 1
frame1 = ctk.CTkFrame(master=app3, width=100, height=50)
frame1.grid(column=0, row=0, sticky="nswe")

# Load the menu icon
icon_menu = ctk.CTkImage(light_image=Image.open("icon_menu.png"), size = (30,30))

# Create the menu button
button_menu = ctk.CTkButton(frame1, image=icon_menu, text="", command=return_to_menu, fg_color="transparent")
button_menu.pack(expand=True)

# Frame 2
frame2 = ctk.CTkFrame(master=app3, width=1100, height=50)
frame2.grid(column=1, row=0, sticky="nswe")

# Label inside frame 2
label = ctk.CTkLabel(master=frame2, text="What service fee should I put on my home?", font=('Helvetica', 20))
label.pack(expand=True)

# Frame 3
frame3 = ctk.CTkFrame(master=app3, width=1100, height=550)
frame3.grid(column=1, row=1, sticky="nswe")

# Data cleaning and visualization

# Data Cleaning
df = pd.read_csv("Airbnb_Open_Data.csv", dtype={
    "NAME": str,
    "host_identity_verified": str,
    "host name": str,
    "neighbourhood group": str,
    "neighbourhood": str,
    "country": str,
    "instant_bookable": str,
    "cancellation_policy": str,
    "room type": str,
    "price": str,
    "service fee": str,
    "last review": str,
    "house_rules": str,
    "license": str,
})

# Clean 'price' column: remove '$' and commas, and convert to float
df["price"] = df["price"].str.strip().str.replace("$", "").str.replace(",", "")
df["price"] = df["price"].astype(float)

# Clean 'service fee' column: remove '$' and convert to float
df["service fee"] = df["service fee"].str.strip().str.replace("$", "")
df["service fee"] = df["service fee"].astype(float)

# Clean 'instant_bookable' column: standardize values to True and False
df["instant_bookable"] = df["instant_bookable"].str.strip().str.replace("FALSE", "False").str.replace("TRUE", "True")
df["instant_bookable"] = df["instant_bookable"].astype(bool)

# Convert 'last review' column to datetime format
df["last review"] = pd.to_datetime(df["last review"], format='%m/%d/%Y')

# Replace values in the 'host_identity_verified' column
df["host_identity_verified"] = df["host_identity_verified"].replace("verified", "True")
df["host_identity_verified"] = df["host_identity_verified"].replace("unconfirmed", "False")
df["host_identity_verified"] = df["host_identity_verified"].fillna("undefined")

# Clean values in 'neighbourhood group' column
df["neighbourhood group"] = df["neighbourhood group"].str.replace("manhatan", "Manhattan").str.replace("brookln", "Brooklyn")

# Use the ggplot style for the plot
plt.style.use('ggplot')

# Create a figure and axes for the scatter plot
fig, ax = plt.subplots(figsize=(18, 11))

# Create a scatter plot with color mapping based on 'room type'
scatter = ax.scatter(df["price"], df["service fee"], c="#FF5A5F", s=30, alpha=0.7)

# Add a title to the plot
ax.set_title("Relationship between price and service fee", fontsize=20,
          fontdict={'fontweight': 'bold'})

# Add axis labels
ax.set_xlabel("Price", fontdict={'fontsize': 14, 'fontweight': 'bold'})
ax.set_ylabel("Service Fee", fontdict={'fontsize': 14, 'fontweight': 'bold'})

# Embed the plot in a Tkinter frame
graph = FigureCanvasTkAgg(fig, master=frame3)
canvas = graph.get_tk_widget()
canvas.pack(expand=True)


# Create the main window
app3.mainloop()

