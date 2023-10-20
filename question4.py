# Import necessary libraries and modules
import customtkinter as ctk
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# Function to return to the menu
def return_to_menu():
    # Hide the current window
    app6.withdraw()
    # Open another Python script named "fenetre2.py"
    os.popen("python fenetre2.py")

# Define colors for different neighborhoods
neighborhood_colors = {
    'City Island': 'skyblue',
    'Staten Island': 'olive',
    'Bronx': 'lightgreen',
    'Queens': 'orange',
    'Manhattan': 'blue',
    'Brooklyn': 'orchid'
}

# Set customtkinter appearance and color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create the main CTk window
app6 = ctk.CTk()
app6.title("Second Window")

# Configure grid row and column weights
app6.grid_rowconfigure(0, weight=0)
app6.grid_rowconfigure(1, weight=1)
app6.grid_columnconfigure(0, weight=0)
app6.grid_columnconfigure(1, weight=1)

# Get the screen width and height
screen_width = app6.winfo_screenwidth()
screen_height = app6.winfo_screenheight()

# Calculate coordinates to center the window
horizontal_centering = (screen_width - 1200) // 2
vertical_centering = (screen_height - 600) // 2
app6.geometry(f"1200x600+{horizontal_centering}+{vertical_centering}")

# Frame 1
frame1 = ctk.CTkFrame(master=app6, width=100, height=50)
frame1.grid(column=0, row=0, sticky="nswe")

# Load the menu icon
icon_menu = ctk.CTkImage(light_image=Image.open("icon_menu.png"), size = (30,30))

# Create the menu button
button_menu = ctk.CTkButton(frame1, image=icon_menu, text="", command=return_to_menu, fg_color="transparent")
button_menu.pack(expand=True)

# Frame 2
frame2 = ctk.CTkFrame(master=app6, width=1100, height=50)
frame2.grid(column=1, row=0, sticky="nswe")

# Label inside frame 2
label = ctk.CTkLabel(master=frame2, text="What are the highest-rated neighborhoods in New York?", font=('Helvetica', 20))
label.pack(expand=True)

# Frame 3
frame3 = ctk.CTkFrame(master=app6, width=1100, height=550)
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

# Group by neighborhood and calculate the average review rate
neighborhood_review_rate_avg = df.groupby('neighbourhood')['review rate number'].mean()
neighborhood_review_rate_avg2 = df.groupby('neighbourhood group')['review rate number'].mean()

# Sort the neighborhood data by review rate in descending order
sorted_data = neighborhood_review_rate_avg.sort_values(ascending=False)
sorted_data2 = neighborhood_review_rate_avg2.sort_values(ascending=False)

# Calculate overall statistics
overall_review_rate_avg = df['review rate number'].mean()
overall_review_rate_median = df['review rate number'].median()
std_deviation_rating = df['review rate number'].std()

# Define how many top neighborhoods to display
top_n = 20
top_listings = sorted_data.head(top_n)
top_listings2 = sorted_data2.head(top_n)

# Create a dictionary to keep track of used legend labels
legend_labels = {}

# Create a bar plot to visualize the top neighborhoods by review rate
fig, ax = plt.subplots(figsize=(20, 11))

for neighborhood, review_rate in top_listings.items():
    group_name = df[df['neighbourhood'] == neighborhood]['neighbourhood group'].values[0]
    group_color = neighborhood_colors.get(group_name, 'gray')
    label = f'Neighbourhood group: {group_name}'

    if group_name not in legend_labels:
        plt.bar(neighborhood, review_rate, color=group_color, label=label)
        legend_labels[group_name] = True
    else:
        plt.bar(neighborhood, review_rate, color=group_color)

# Add horizontal lines and labels to the plot
ax.axhline(overall_review_rate_avg, color='blue', linestyle='--', label='Overall Average Review Rate')
ax.axhline(overall_review_rate_median, color='green', linestyle='--', label='The Median Average Review Rate')
ax.axhline(overall_review_rate_avg + std_deviation_rating, color='red', linestyle='--',
            label='Avg Review Rate + Std Deviation')
plt.axhline(overall_review_rate_avg - std_deviation_rating, color='purple', linestyle='--',
            label='Avg Review Rate - Std Deviation')

# Set plot titles and labels
plt.title(f'Top {top_n} Listings with Highest Average Review Rate by Neighbourhood', fontsize=20,
          fontdict={'fontweight': 'bold'})
plt.xlabel('Neighbourhood', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.ylabel('Review Rate Number', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.xticks(rotation=45)

# Display the legend
plt.legend()

# Embed the plot in the Tkinter frame
canvas = FigureCanvasTkAgg(fig, master=frame3)
canvas.get_tk_widget().pack(expand=True)

# Create the main window
app6.mainloop()

