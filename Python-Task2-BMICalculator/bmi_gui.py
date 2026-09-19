# Task 2: BMI Calculator
import tkinter as tk
from bmi_logic import calculate_bmi, classify_bmi
from bmi_database import init_db, save_record, get_user_history
import matplotlib.pyplot as plt

# Set up the database table (only creates it if it doesn't exist)
init_db()

# Create main window
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x500")

# Dark theme colors
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ENTRY_BG = "#2d2d2d"
BTN_BG = "#3a3a3a"

window.configure(bg=BG_COLOR)

# Name label + input box
name_label = tk.Label(window, text="Name:", bg=BG_COLOR, fg=FG_COLOR)
name_label.pack()
name_entry = tk.Entry(window, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
name_entry.pack()

# Weight label + input box
weight_label = tk.Label(window, text="Weight (kg):", bg=BG_COLOR, fg=FG_COLOR)
weight_label.pack()
weight_entry = tk.Entry(window, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
weight_entry.pack()

# Height label + input box
height_label = tk.Label(window, text="Height (m):", bg=BG_COLOR, fg=FG_COLOR)
height_label.pack()
height_entry = tk.Entry(window, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
height_entry.pack()

# Label to show the result
result_label = tk.Label(window, text="", font=("Arial", 14), bg=BG_COLOR)
result_label.pack(pady=20)

def on_calculate_click():
    name = name_entry.get().strip().lower()
    weight_text = weight_entry.get()
    height_text = height_entry.get()

    if name == "":
        result_label.config(text="Error: Please enter a name.", fg="red")
        return

    try:
        weight = float(weight_text)
        height = float(height_text)
        if weight <= 0 or height <= 0:
            result_label.config(text="Error: Values must be positive.", fg="red")
            return
    except ValueError:
        result_label.config(text="Error: Enter valid numbers.", fg="red")
        return

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    if category == "Underweight":
        color = "#3399ff"
    elif category == "Normal":
        color = "#33cc33"
    elif category == "Overweight":
        color = "orange"
    else:
        color = "#ff4d4d"

    result_label.config(text=f"{name}, your BMI is {bmi} ({category})", fg=color)

    try:
        save_record(name, weight, height, bmi, category)
    except Exception as e:
        result_label.config(text=f"Saved calc, but DB error: {e}", fg="red")

def on_view_trend_click():
    name = name_entry.get().strip().lower()
    if name == "":
        result_label.config(text="Error: Enter a name to view trend.", fg="red")
        return

    try:
        history = get_user_history(name)
    except Exception as e:
        result_label.config(text=f"DB error: {e}", fg="red")
        return

    if len(history) == 0:
        result_label.config(text=f"No history found for {name}.", fg="red")
        return

    bmis = [row[0] for row in history]
    dates = [row[1][5:16] for row in history]  # trims to "MM-DD HH:MM"

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Background zones for BMI categories
    ax.axhspan(0, 18.5, color="#3399ff", alpha=0.15)
    ax.axhspan(18.5, 25, color="#33cc33", alpha=0.15)
    ax.axhspan(25, 30, color="orange", alpha=0.15)
    ax.axhspan(30, max(bmis) + 5, color="#ff4d4d", alpha=0.15)

    ax.plot(dates, bmis, marker='o', color='cyan', linewidth=2, markersize=8, zorder=3)

    # Label each point with its exact BMI value
    for x, y in zip(dates, bmis):
        ax.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=9, color='white')

    ax.set_title(f"BMI Trend for {name}", fontsize=14, color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("BMI", color='white')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

calculate_button = tk.Button(window, text="Calculate", command=on_calculate_click, bg=BTN_BG, fg=FG_COLOR)
calculate_button.pack(pady=10)

trend_button = tk.Button(window, text="View Trend", command=on_view_trend_click, bg=BTN_BG, fg=FG_COLOR)
trend_button.pack(pady=10)

window.mainloop()