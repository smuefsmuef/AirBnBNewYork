# Import necessary libraries
import customtkinter as ctk
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# Function to return to the menu
def return_to_menu():
    app5.withdraw()  # Hide the current window
    os.popen("python fenetre2.py")  # Open another Python script named "fenetre2.py"

# Set customtkinter appearance and color theme
ctk.set_appearance_mode("System")  # Choose the appearance mode (system, light, dark)
ctk.set_default_color_theme("blue")  # Set the color theme (blue, dark-blue, green)

# Create the main CTk window
app5 = ctk.CTk()
app5.title("Second Window")

# Configure grid row and column weights
app5.grid_rowconfigure(0, weight=0)  # Configure row 0 with no weight
app5.grid_rowconfigure(1, weight=1)  # Configure row 1 to expand
app5.grid_columnconfigure(0, weight=0)  # Configure column 0 with no weight
app5.grid_columnconfigure(1, weight=1)  # Configure column 1 to expand

# Get the screen width and height
screen_width = app5.winfo_screenwidth()
screen_height = app5.winfo_screenheight()

# Calculate coordinates to center the window
horizontal_centering = (screen_width - 1200) // 2
vertical_centering = (screen_height - 600) // 2
app5.geometry(f"1200x600+{horizontal_centering}+{vertical_centering}")

# Frame 1
frame1 = ctk.CTkFrame(master=app5, width=100, height=50)
frame1.grid(column=0, row=0, sticky="nswe")  # Attach frame to column 0, row 0, and make it sticky to north, south, west, and east

# Load the menu icon
icon_menu = ctk.CTkImage(light_image=Image.open("icon_menu.png"), size=(30, 30))

# Create the menu button
button_menu = ctk.CTkButton(frame1, image=icon_menu, text="", command=return_to_menu, fg_color="transparent")
button_menu.pack(expand=True)  # Expand the button within its container

# Frame 2
frame2 = ctk.CTkFrame(master=app5, width=1100, height=50)
frame2.grid(column=1, row=0, sticky="nswe")

# Label inside frame 2
label = ctk.CTkLabel(master=frame2, text="Does having a verified status positively impact my reviews?", font=('Helvetica', 20))
label.pack(expand=True)

# Frame 3
frame3 = ctk.CTkFrame(master=app5, width=1100, height=550)
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

# Filter and calculate data for visualization
filtered_data = df[df['review rate number'] > 4]
verified_data = filtered_data[filtered_data['host_identity_verified'] == "True"]
unconfirmed_data = filtered_data[filtered_data['host_identity_verified'] == "False"]
undefined_data = filtered_data[filtered_data['host_identity_verified'] == "undefined"]

num_reviews_verified = verified_data['number of reviews'].sum()
num_reviews_undefined = undefined_data['number of reviews'].sum()
num_reviews_unconfirmed = unconfirmed_data['number of reviews'].sum()

total_reviews = filtered_data['number of reviews'].sum()

percentage_reviews_verified = (num_reviews_verified / total_reviews) * 100
percentage_reviews_unverified = (num_reviews_undefined / total_reviews) * 100
percentage_reviews_unconfirmed = (num_reviews_unconfirmed / total_reviews) * 100

# Create a pie chart
fig, ax = plt.subplots(figsize=(20, 11))
labels = ['Verified', 'Undefined', 'Not verified']
sizes = [percentage_reviews_verified, percentage_reviews_unverified, percentage_reviews_unconfirmed]
colors = ['lightcoral', 'skyblue', 'lightgreen']

ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Percentage of Positive Reviews (>4) by Host Verification Status', fontsize=20, fontdict={'fontweight': 'bold'})

# Embed the plot in the Tkinter frame
canvas = FigureCanvasTkAgg(fig, master=frame3)
canvas.get_tk_widget().pack(expand=True)  # Expand the canvas within its container

# Create the main window
app5.mainloop()

