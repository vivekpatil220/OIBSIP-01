import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate BMI and update GUI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # converting height from cm to meters
        bmi = weight / (height ** 2)
        bmi_result.set(f"Your BMI: {bmi:.1f}")

        # BMI Categories
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal Weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        bmi_category.set(f"Category: {category}")

        # Save BMI data to file
        save_bmi_data(weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")

# Function to save BMI data to JSON file
def save_bmi_data(weight, height, bmi, category):
    entry = {
        "Weight": weight,
        "Height": height,
        "BMI": bmi,
        "Category": category
    }

    filename = "bmi_data.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(entry)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to visualize historical BMI data
def visualize_data():
    try:
        filename = "bmi_data.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)

            weights = [entry["Weight"] for entry in data]
            bmis = [entry["BMI"] for entry in data]

            plt.figure(figsize=(8, 4))
            plt.scatter(weights, bmis, color='b', marker='o', edgecolors='k')
            plt.title('BMI Trend Over Time')
            plt.xlabel('Weight (kg)')
            plt.ylabel('BMI')
            plt.grid(True)

            # Embedding plot into Tkinter GUI
            canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=6, columnspan=2, pady=10)

        else:
            messagebox.showinfo("Info", "No BMI data found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("BMI Calculator")

# Styling
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12), padding=10)
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TEntry', font=('Helvetica', 12))

# Frame to hold the widgets
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# Weight input
weight_label = ttk.Label(frame, text="Weight (kg):")
weight_label.grid(row=0, column=0, sticky="w")

weight_entry = ttk.Entry(frame, width=20)
weight_entry.grid(row=0, column=1)

# Height input
height_label = ttk.Label(frame, text="Height (cm):")
height_label.grid(row=1, column=0, sticky="w")

height_entry = ttk.Entry(frame, width=20)
height_entry.grid(row=1, column=1)

# Calculate button
calculate_button = ttk.Button(frame, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, columnspan=2, pady=10)

# Visualize data button
visualize_button = ttk.Button(frame, text="Visualize Data", command=visualize_data)
visualize_button.grid(row=3, columnspan=2, pady=10)

# Result display
bmi_result = tk.StringVar()
result_label = ttk.Label(frame, textvariable=bmi_result)
result_label.grid(row=4, columnspan=2)

# Category display
bmi_category = tk.StringVar()
category_label = ttk.Label(frame, textvariable=bmi_category)
category_label.grid(row=5, columnspan=2)

# Start the main loop
root.mainloop()
