# Task 3: Password Generator
import tkinter as tk
from password_logic import generate_password, check_strength
import pyperclip

# --- Theme ---
BG_COLOR = "#12121c"
CARD_COLOR = "#1c1c2b"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#9370ff"
FG_COLOR = "#f0f0f5"
MUTED = "#9a9aae"
ENTRY_BG = "#25253a"

window = tk.Tk()
window.title("Password Generator")
window.geometry("450x650")
window.configure(bg=BG_COLOR)

def card(parent, **kwargs):
    return tk.Frame(parent, bg=CARD_COLOR, highlightbackground="#33334d",
                     highlightthickness=1, **kwargs)

# --- Header ---
header = tk.Frame(window, bg=BG_COLOR)
header.pack(fill="x", pady=(10, 4))
tk.Label(header, text="🔐 Password Generator", font=("Segoe UI", 15, "bold"),
         bg=BG_COLOR, fg=FG_COLOR).pack()
tk.Label(header, text="Secure, customizable passwords in one click",
         font=("Segoe UI", 8), bg=BG_COLOR, fg=MUTED).pack(pady=(1, 0))

# --- Result card ---
result_card = card(window)
result_card.pack(fill="x", padx=20, pady=5, ipady=5)

result_label = tk.Label(result_card, text="Click Generate to begin",
                         font=("Consolas", 14, "bold"), bg=CARD_COLOR, fg=MUTED, wraplength=370)
result_label.pack(pady=(5, 3))

strength_label = tk.Label(result_card, text="", font=("Segoe UI", 9, "bold"), bg=CARD_COLOR)
strength_label.pack()

# --- Settings card ---
settings_card = card(window)
settings_card.pack(fill="x", padx=20, pady=5, ipady=3)

tk.Label(settings_card, text="LENGTH", font=("Segoe UI", 8, "bold"),
         bg=CARD_COLOR, fg=ACCENT).pack(anchor="w", padx=16, pady=(5, 0))

length_value_label = tk.Label(settings_card, text="12", font=("Segoe UI", 15, "bold"),
                               bg=CARD_COLOR, fg=FG_COLOR)
length_value_label.pack(anchor="w", padx=16)

def on_length_change(value):
    length_value_label.config(text=value)

length_slider = tk.Scale(settings_card, from_=8, to=32, orient="horizontal",
                          bg=CARD_COLOR, fg=FG_COLOR, troughcolor=ENTRY_BG,
                          activebackground=ACCENT, highlightthickness=0,
                          bd=0, showvalue=False, sliderrelief="flat",
                          command=on_length_change)
length_slider.set(12)
length_slider.pack(fill="x", padx=16, pady=(0, 3))

tk.Frame(settings_card, bg="#33334d", height=1).pack(fill="x", padx=16, pady=2)

tk.Label(settings_card, text="CHARACTER TYPES", font=("Segoe UI", 8, "bold"),
         bg=CARD_COLOR, fg=ACCENT).pack(anchor="w", padx=16, pady=(0, 1))

use_upper = tk.BooleanVar(value=True)
use_lower = tk.BooleanVar(value=True)
use_digits = tk.BooleanVar(value=True)
use_symbols = tk.BooleanVar(value=False)
exclude_ambiguous = tk.BooleanVar(value=False)

def make_checkbox(parent, text, variable):
    cb = tk.Checkbutton(parent, text=text, variable=variable,
                         bg=CARD_COLOR, fg=FG_COLOR, selectcolor=ENTRY_BG,
                         activebackground=CARD_COLOR, activeforeground=FG_COLOR,
                         font=("Segoe UI", 9), anchor="w")
    cb.pack(anchor="w", padx=16, fill="x", pady=0)
    return cb

make_checkbox(settings_card, "Uppercase (A-Z)", use_upper)
make_checkbox(settings_card, "Lowercase (a-z)", use_lower)
make_checkbox(settings_card, "Numbers (0-9)", use_digits)
make_checkbox(settings_card, "Symbols (!@#$...)", use_symbols)
make_checkbox(settings_card, "Exclude ambiguous (0,O,1,l,I)", exclude_ambiguous)

# --- Buttons ---
button_frame = tk.Frame(window, bg=BG_COLOR)
button_frame.pack(fill="x", padx=20, pady=5)

def on_enter(e): e.widget.config(bg=ACCENT_HOVER)
def on_leave(e): e.widget.config(bg=ACCENT)

generate_button = tk.Button(button_frame, text="Generate Password", bg=ACCENT, fg="white",
                             font=("Segoe UI", 10, "bold"), bd=0, activebackground=ACCENT_HOVER,
                             activeforeground="white", cursor="hand2", pady=6)
generate_button.pack(fill="x")
generate_button.bind("<Enter>", on_enter)
generate_button.bind("<Leave>", on_leave)

copy_button = tk.Button(button_frame, text="Copy to Clipboard", bg=ENTRY_BG, fg=FG_COLOR,
                         font=("Segoe UI", 9), bd=0, activebackground="#33334d",
                         activeforeground=FG_COLOR, cursor="hand2", pady=4)
copy_button.pack(fill="x", pady=(4, 0))

# --- History card ---
history_card = card(window)
history_card.pack(fill="both", expand=True, padx=20, pady=(0, 8), ipady=3)

tk.Label(history_card, text="SESSION HISTORY", font=("Segoe UI", 8, "bold"),
         bg=CARD_COLOR, fg=ACCENT).pack(anchor="w", padx=16, pady=(5, 2))

history_box = tk.Listbox(history_card, height=5, bg=ENTRY_BG, fg=FG_COLOR,
                          font=("Consolas", 11), highlightthickness=0, borderwidth=0,
                          selectbackground=ACCENT)
history_box.pack(fill="x", padx=16, pady=(0, 4))

password_history = []
current_password = ""

def update_history_display():
    history_box.delete(0, tk.END)
    for pw in reversed(password_history):
        history_box.insert(tk.END, pw)

def on_generate_click():
    global current_password
    try:
        pw = generate_password(
            length=length_slider.get(),
            use_upper=use_upper.get(),
            use_lower=use_lower.get(),
            use_digits=use_digits.get(),
            use_symbols=use_symbols.get(),
            exclude_ambiguous=exclude_ambiguous.get()
        )
    except ValueError as e:
        result_label.config(text=str(e), fg="#ff6b6b")
        strength_label.config(text="")
        return

    current_password = pw
    result_label.config(text=pw, fg=FG_COLOR)

    strength = check_strength(pw)
    strength_colors = {"Weak": "#ff6b6b", "Medium": "#ffb84d", "Strong": "#4dd88a"}
    strength_label.config(text=f"● {strength}", fg=strength_colors[strength])

    pyperclip.copy(pw)

    password_history.append(pw)
    if len(password_history) > 5:
        password_history.pop(0)
    update_history_display()

def on_copy_click():
    if current_password:
        pyperclip.copy(current_password)
        strength_label.config(text=strength_label.cget("text") + "   (copied ✓)")

generate_button.config(command=on_generate_click)
copy_button.config(command=on_copy_click)

window.mainloop()