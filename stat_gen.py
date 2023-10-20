# Import necessary libraries and modules
import customtkinter as ctk
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# Define functions to calculate general statistics for different columns
def create_general_statistics_price(df):
    # minimum price
    min_price = df['price'].min()

    # maximum price
    max_price = df['price'].max()

    # average price
    average_price = df['price'].mean()

    # standart deviation
    std = df['price'].std()

    # Calculate the most popular price (mode)
    mode_price = df['price'].mode().values[0]

    # interquartile range (IQR)
    q1 = df['price'].quantile(0.25)
    q3 = df['price'].quantile(0.75)
    iqr = q3 - q1

    return min_price, max_price, average_price, mode_price, std, iqr


def create_general_statistics_review(df):
    # minimum review
    min_review = df['review rate number'].min()

    # maximum review
    max_review = df['review rate number'].max()

    # average review
    average_review = df['review rate number'].mean()

    # standart deviation
    std = df['review rate number'].std()

    # Calculate the most popular review (mode)
    mode_review = df['review rate number'].mode().values[0]

    # interquartile range (IQR)
    q1 = df['review rate number'].quantile(0.25)
    q3 = df['review rate number'].quantile(0.75)
    iqr = q3 - q1

    return min_review, max_review, average_review, mode_review, std, iqr


def create_general_statistics_construction(df):
    # minimum construction year
    min_year = df['Construction year'].min()

    # maximum construction year
    max_year = df['Construction year'].max()

    # average construction year
    average_year = df['Construction year'].mean()


    return min_year, max_year, average_year

def create_general_statistics_night(df):
    # minimum minimun night
    min_night = df['minimum nights'].min()

    # maximum minimun night
    max_night = df['minimum nights'].max()

    # average minimun night
    average_night = df['minimum nights'].mean()

    # standart deviation
    std = df['minimum nights'].std()

    # Calculate the most popular minimun night (mode)
    mode_night = df['minimum nights'].mode().values[0]

    # interquartile range (IQR)
    q1 = df['minimum nights'].quantile(0.25)
    q3 = df['minimum nights'].quantile(0.75)
    iqr = q3 - q1

    return min_night, max_night, average_night, mode_night, std, iqr


# Function to return to the menu
def return_to_menu():
    # Hide the current window
    app7.withdraw()
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
app7 = ctk.CTk()
app7.title("Second Window")

# Configure grid row and column weights
app7.grid_rowconfigure(0, weight=0)
app7.grid_rowconfigure(1, weight=1)
app7.grid_columnconfigure(0, weight=0)
app7.grid_columnconfigure(1, weight=1)

# Get the screen width and height
screen_width = app7.winfo_screenwidth()
screen_height = app7.winfo_screenheight()

# Calculate coordinates to center the window
horizontal_centering = (screen_width - 1200) // 2
vertical_centering = (screen_height - 600) // 2
app7.geometry(f"1200x600+{horizontal_centering}+{vertical_centering}")

# Frame 1
frame1 = ctk.CTkFrame(master=app7, width=100, height=50)
frame1.grid(column=0, row=0, sticky="nswe")

# Load the menu icon
icon_menu = ctk.CTkImage(light_image=Image.open("icon_menu.png"), size = (30,30))

# Create the menu button
button_menu = ctk.CTkButton(frame1, image=icon_menu, text="", command=return_to_menu, fg_color="transparent")
button_menu.pack(expand=True)

# Frame 2
frame2 = ctk.CTkFrame(master=app7, width=1100, height=50)
frame2.grid(column=1, row=0, sticky="nswe")

# Label inside frame 2
label = ctk.CTkLabel(master=frame2, text="General statistics about data", font=('Helvetica', 20))
label.pack(expand=True)

# Frame 3
frame3 = ctk.CTkFrame(master=app7, width=1100, height=550)
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
# Calculate statistics for different categories from a DataFrame
price_statistics = create_general_statistics_price(df)
review_statistics = create_general_statistics_review(df)
construction_statistics = create_general_statistics_construction(df)
night_statistics = create_general_statistics_night(df)

# Create a figure with four subplots
fig = plt.figure(figsize=(20, 11))

# Create individual subplots
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

# Disable axes for a cleaner appearance
ax1.axis('off')
ax2.axis('off')
ax3.axis('off')
ax4.axis('off')

# Data for the tables
table_data_price = [
    ["Price", "Value"],
    ["Minimum Price", price_statistics[0]],
    ["Maximum Price", price_statistics[1]],
    ["Average Price", round(price_statistics[2], 2)],
    ["Most popular Price", price_statistics[3]],
    ["Standard Deviation", round(price_statistics[4], 2)],
    ["Interquartile range", price_statistics[5]]
]

table_data_review = [
    ["Review", "Value"],
    ["Minimum Review", review_statistics[0]],
    ["Maximum Review", review_statistics[1]],
    ["Average Review", round(review_statistics[2], 2)],
    ["Most popular Review", review_statistics[3]],
    ["Standard Deviation", round(review_statistics[4], 2)],
    ["Interquartile range", review_statistics[5]]
]

table_data_construction = [
    ["Construction year", "Value"],
    ["Minimum Year", construction_statistics[0]],
    ["Maximum Year", construction_statistics[1]],
    ["Average Year", round(construction_statistics[2], 0)]
]

table_data_night = [
    ["Minimum night", "Value"],
    ["Minimum night", night_statistics[0]],
    ["Maximum night", night_statistics[1]],
    ["Average night", round(night_statistics[2], 2)],
    ["Most popular night", night_statistics[3]],
    ["Standard Deviation", round(night_statistics[4], 2)],
    ["Interquartile range", night_statistics[5]]
]

# Create the four tables
table1 = ax1.table(cellText=table_data_price, loc='center', cellLoc='center', colLabels=None)
table2 = ax2.table(cellText=table_data_review, loc='center', cellLoc='center', colLabels=None)
table3 = ax3.table(cellText=table_data_construction, loc='center', cellLoc='center', colLabels=None)
table4 = ax4.table(cellText=table_data_night, loc='center', cellLoc='center', colLabels=None)

# Disable automatic font size adjustment
table1.auto_set_font_size(False)
table2.auto_set_font_size(False)
table3.auto_set_font_size(False)
table4.auto_set_font_size(False)

# Set the font size for the cells
table1.set_fontsize(11)
table2.set_fontsize(11)
table3.set_fontsize(11)
table4.set_fontsize(11)

# Embed the plot in the Tkinter frame
canvas = FigureCanvasTkAgg(fig, master=frame3)
canvas.get_tk_widget().pack(expand=True)

# Create the main window
app7.mainloop()
