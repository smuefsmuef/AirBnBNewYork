import customtkinter as ctk
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# Function to return to the menu
def return_to_menu():
    app4.withdraw()
    os.popen("python fenetre2.py")

# Color mapping for different neighborhoods
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
app4 = ctk.CTk()
app4.title("Second Window")

# Configure grid row and column weights
app4.grid_rowconfigure(0, weight=0)
app4.grid_rowconfigure(1, weight=1)
app4.grid_columnconfigure(0, weight=0)
app4.grid_columnconfigure(1, weight=1)

# Get the screen width and height
screen_width = app4.winfo_screenwidth()
screen_height = app4.winfo_screenheight()

# Calculate coordinates to center the window
horizontal_centering = (screen_width - 1200) // 2
vertical_centering = (screen_height - 600) // 2
app4.geometry(f"1200x600+{horizontal_centering}+{vertical_centering}")

# Frame 1
frame1 = ctk.CTkFrame(master=app4, width=100, height=50)
frame1.grid(column=0, row=0, sticky="nswe")

# Load the menu icon
icon_menu = ctk.CTkImage(light_image=Image.open("icon_menu.png"), size=(30, 30))

# Create the menu button
button_menu = ctk.CTkButton(frame1, image=icon_menu, text="", command=return_to_menu, fg_color="transparent")
button_menu.pack(expand=True)

# Frame 2
frame2 = ctk.CTkFrame(master=app4, width=1100, height=50)
frame2.grid(column=1, row=0, sticky="nswe")

# Label inside frame 2
label = ctk.CTkLabel(master=frame2, text="What are the most and least expensive neighborhoods in New York City?",
                     font=('Helvetica', 20))
label.pack(expand=True)

# Frame 3
frame3 = ctk.CTkFrame(master=app4, width=1100, height=550)
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
df["neighbourhood group"] = df["neighbourhood group"].str.replace("manhatan", "Manhattan").str.replace("brookln",
                                                                                                      "Brooklyn")

neighborhood_prices = df.groupby('neighbourhood')['price'].mean()
neighborhood_group_df = df[['neighbourhood', 'neighbourhood group']].drop_duplicates()

neighborhood_prices = neighborhood_prices.sort_values(ascending=False)

# Get the neighborhoods with the highest and lowest average prices
highest_avg_price = neighborhood_prices.tail(10).sort_values(ascending=False)
lowest_avg_price = neighborhood_prices.head(10).sort_values(ascending=False)

# Create a dictionary to keep track of used legend labels
legend_labels = {}

# Plot the data
fig, ax = plt.subplots(figsize=(20, 11))
sorted_neighborhoods = pd.concat([lowest_avg_price, highest_avg_price])

for neighborhood, price in sorted_neighborhoods.items():
    group_name = \
        neighborhood_group_df[neighborhood_group_df['neighbourhood'] == neighborhood]['neighbourhood group'].values[
            0]
    group_color = neighborhood_colors.get(group_name, 'gray')
    label = f'Neighbourhood group: {group_name}'

    # Check if the label has already been used
    if label not in legend_labels:
        plt.barh(neighborhood, price, color=group_color, label=label)
        legend_labels[label] = True
    else:
        plt.barh(neighborhood, price, color=group_color)

# Add backgrounds to show top 10/lowest 10
top_region_y = sorted_neighborhoods.index[0]
bottom_region_y = sorted_neighborhoods.index[9]
top_region_y_neg = sorted_neighborhoods.index[-1]
bottom_region_y_neg = sorted_neighborhoods.index[-10]
ax.axhspan(bottom_region_y, top_region_y, facecolor='lightblue', alpha=0.3, zorder=0,
           label='Highest 10 Neighbourhoods')
ax.axhspan(top_region_y_neg, bottom_region_y_neg, facecolor='lightcoral', alpha=0.2, zorder=0,
           label='Lowest 10 Neighbourhoods')

# other data
average_price_all = neighborhood_prices.mean()
std_deviation_all = neighborhood_prices.std()
plt.axvline(average_price_all, color='green', linestyle='--', label='Average Price (All Neighborhoods)')
plt.axvline(average_price_all + std_deviation_all, color='red', linestyle='--', label='Avg Price + Std Deviation')
plt.axvline(average_price_all - std_deviation_all, color='purple', linestyle='--',
            label='Avg Price - Std Deviation')

plt.xlabel('Average Listing Price', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.ylabel('Neighbourhood', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.title('10 Neighbourhoods in New York City with Highest and Lowest Average Listing Prices', fontsize=20,
          fontdict={'fontweight': 'bold'})
plt.legend()

# Embed the plot in the Tkinter frame
canvas = FigureCanvasTkAgg(fig, master=frame3)
canvas.get_tk_widget().pack(expand=True)

# Create the main window
app4.mainloop()
