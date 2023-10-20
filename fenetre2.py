# Import necessary libraries
import customtkinter as ctk
import os

# Function to open the first question window
def open_question1():
    app2.withdraw()  # Hide the current window
    os.popen("python question1.py")  # Run the "question1.py" script

# Function to open the second question window
def open_question2():
    app2.withdraw()  # Hide the current window
    os.popen("python question2.py")  # Run the "question2.py" script

# Function to open the third question window
def open_question3():
    app2.withdraw()  # Hide the current window
    os.popen("python question3.py")  # Run the "question3.py" script

# Function to open the fourth question window
def open_question4():
    app2.withdraw()  # Hide the current window
    os.popen("python question4.py")  # Run the "question4.py" script

# Function to open the statistics window
def open_stat():
    app2.withdraw()  # Hide the current window
    os.popen("python stat_gen.py")  # Run the "stat_gen.py" script

# Initialize the custom Tkinter application
ctk.set_appearance_mode("System")  # Set the appearance mode to "System"
ctk.set_default_color_theme("blue")  # Set the default color theme to "blue"
app2 = ctk.CTk()  # Create a CTk window

# Set the window title
app2.title("Menu")

# Get the width and height of the screen
screen_width = app2.winfo_screenwidth()
screen_height = app2.winfo_screenheight()

# Calculate the x and y coordinates to center the window
centrage_horizontal = (screen_width - 1200) // 2
centrage_vertical = (screen_height - 600) // 2

# Set the window geometry to center it on the screen
app2.geometry(f"1200x600+{centrage_horizontal}+{centrage_vertical}")

# Create a frame within the window
frame = ctk.CTkFrame(master=app2)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Create a label to display "MENU"
Label = ctk.CTkLabel(master=frame, text="MENU", font=('Helvetica', 25))
Label.pack(pady=30)

# Create buttons for different questions and statistics
Button1 = ctk.CTkButton(master=frame, text="What service fee should I put on my home ?", command=open_question1)
Button1.pack(pady=(40, 20), padx=100, ipady=7, fill="x")

Button2 = ctk.CTkButton(master=frame, text="What are the most and least expensive neighborhoods in New York City?",
                       command=open_question2)
Button2.pack(pady=20, padx=100, ipady=7, fill="x")

Button3 = ctk.CTkButton(master=frame, text="Does having a verified status positively impact my reviews?",
                       command=open_question3)
Button3.pack(pady=20, padx=100, ipady=7, fill="x")

Button4 = ctk.CTkButton(master=frame, text="What are the highest-rated neighborhoods in New York?", command=open_question4)
Button4.pack(pady=20, padx=100, ipady=7, fill="x")

Button5 = ctk.CTkButton(master=frame, text="General statistics about data", command=open_stat)
Button5.pack(pady=20, padx=100, ipady=7, fill="x")

# Start the application's main loop
app2.mainloop()
