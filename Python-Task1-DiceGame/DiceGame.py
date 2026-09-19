# Task 1
import math
import random
import sys
import time
import tkinter as tk
from tkinter import messagebox

# Windows audio support
try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False


# LOGIC 
class DiceGame:
    def __init__(self, num_dice=2):
        self.num_dice = num_dice
        self.history = []
        self.total_rolls = 0
        self.doubles_count = 0
        self.streak = 0
        self.prediction = None  # 'under', 'exact', 'over'

    def set_dice_count(self, count):
        self.num_dice = max(1, min(4, count))

    def roll(self):
        dice_values = [random.randint(1, 6) for _ in range(self.num_dice)]
        total_sum = sum(dice_values)
        is_double = (len(dice_values) == 2 and dice_values[0] == dice_values[1])

        self.total_rolls += 1
        if is_double:
            self.doubles_count += 1

        # Check Prediction Challenge
        won_prediction = False
        if self.prediction:
            if self.prediction == 'under' and total_sum < 7:
                won_prediction = True
            elif self.prediction == 'exact' and total_sum == 7:
                won_prediction = True
            elif self.prediction == 'over' and total_sum > 7:
                won_prediction = True

            if won_prediction:
                self.streak += 1
            else:
                self.streak = 0

        result = {
            "roll_number": self.total_rolls,
            "dice": dice_values,
            "sum": total_sum,
            "is_double": is_double,
            "prediction": self.prediction,
            "won_prediction": won_prediction,
            "streak": self.streak
        }
        self.history.insert(0, result)
        return result

    def get_average_sum(self):
        if not self.history:
            return 0.0
        return round(sum(item["sum"] for item in self.history) / len(self.history), 1)

    def get_highest_sum(self):
        if not self.history:
            return 0
        return max(item["sum"] for item in self.history)

    def reset(self):
        self.history.clear()
        self.total_rolls = 0
        self.doubles_count = 0
        self.streak = 0
        self.prediction = None


#UI
class PremiumDiceUI:
    # Color Themes Definition
    THEMES = {
        "Obsidian Dark": {
            "bg": "#0F172A",
            "card_bg": "#1E293B",
            "border": "#334155",
            "accent": "#6366F1",
            "accent_hover": "#4F46E5",
            "gold": "#F59E0B",
            "text": "#F8FAFC",
            "subtext": "#94A3B8",
            "die_bg": "#FFFFFF",
            "die_pip": "#0F172A",
            "die_border": "#CBD5E1"
        },
        "Cyber Neon": {
            "bg": "#090D16",
            "card_bg": "#111827",
            "border": "#1E293B",
            "accent": "#06B6D4",
            "accent_hover": "#0891B2",
            "gold": "#EC4899",
            "text": "#F3F4F6",
            "subtext": "#6B7280",
            "die_bg": "#1F2937",
            "die_pip": "#22D3EE",
            "die_border": "#06B6D4"
        },
        "Gold Casino": {
            "bg": "#1C1917",
            "card_bg": "#292524",
            "border": "#44403C",
            "accent": "#F59E0B",
            "accent_hover": "#D97706",
            "gold": "#FBBF24",
            "text": "#FAFAF9",
            "subtext": "#A8A29E",
            "die_bg": "#FEF3C7",
            "die_pip": "#78350F",
            "die_border": "#F59E0B"
        },
        "Emerald Luxury": {
            "bg": "#064E3B",
            "card_bg": "#065F46",
            "border": "#047857",
            "accent": "#10B981",
            "accent_hover": "#059669",
            "gold": "#F59E0B",
            "text": "#ECFDF5",
            "subtext": "#A7F3D0",
            "die_bg": "#FFFFFF",
            "die_pip": "#064E3B",
            "die_border": "#34D399"
        }
    }

    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Dice Roller Studio Pro")
        self.root.geometry("620x760")
        self.root.resizable(False, False)

        self.current_theme_name = "Obsidian Dark"
        self.theme = self.THEMES[self.current_theme_name]
        self.sound_enabled = True

        self.game = DiceGame(num_dice=2)
        self.is_rolling = False
        self.particles = []

        self.root.configure(bg=self.theme["bg"])
        self.setup_ui()
        self.draw_dice([1, 1])

    def setup_ui(self):
        # Header 
        header = tk.Frame(self.root, bg=self.theme["bg"], padx=25, pady=15)
        header.pack(fill=tk.X)

        title_label = tk.Label(
            header,
            text="🎲 DICE ROLLER STUDIO",
            font=("Segoe UI", 18, "bold"),
            fg=self.theme["text"],
            bg=self.theme["bg"]
        )
        title_label.pack(side=tk.LEFT)

        controls_top = tk.Frame(header, bg=self.theme["bg"])
        controls_top.pack(side=tk.RIGHT)

        self.sound_btn = tk.Button(
            controls_top,
            text="🔊 Sound: ON",
            font=("Segoe UI", 9, "bold"),
            fg=self.theme["text"],
            bg=self.theme["card_bg"],
            activebackground=self.theme["border"],
            activeforeground=self.theme["text"],
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.toggle_sound
        )
        self.sound_btn.pack(side=tk.LEFT, padx=5)

        self.theme_var = tk.StringVar(value=self.current_theme_name)
        theme_menu = tk.OptionMenu(
            controls_top,
            self.theme_var,
            *list(self.THEMES.keys()),
            command=self.change_theme
        )
        theme_menu.config(
            font=("Segoe UI", 9, "bold"),
            fg=self.theme["text"],
            bg=self.theme["card_bg"],
            activebackground=self.theme["border"],
            activeforeground=self.theme["text"],
            bd=0,
            highlightthickness=0
        )
        theme_menu.pack(side=tk.LEFT, padx=5)

        # Stage Frame
        self.stage_frame = tk.Frame(
            self.root,
            bg=self.theme["card_bg"],
            padx=20,
            pady=15,
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        self.stage_frame.pack(fill=tk.X, padx=25, pady=5)

        selector_frame = tk.Frame(self.stage_frame, bg=self.theme["card_bg"])
        selector_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            selector_frame,
            text="Dice Count:",
            font=("Segoe UI", 10, "bold"),
            fg=self.theme["subtext"],
            bg=self.theme["card_bg"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.dice_count_var = tk.IntVar(value=2)
        for n in [1, 2, 3, 4]:
            rb = tk.Radiobutton(
                selector_frame,
                text=f"{n} Die" if n == 1 else f"{n} Dice",
                value=n,
                variable=self.dice_count_var,
                command=self.on_dice_count_change,
                font=("Segoe UI", 9, "bold"),
                fg=self.theme["text"],
                bg=self.theme["card_bg"],
                selectcolor=self.theme["border"],
                activebackground=self.theme["card_bg"],
                activeforeground=self.theme["text"]
            )
            rb.pack(side=tk.LEFT, padx=4)

        # Animated Canvas
        self.canvas = tk.Canvas(
            self.stage_frame,
            width=530,
            height=170,
            bg=self.theme["bg"],
            highlightthickness=1,
            highlightbackground=self.theme["border"]
        )
        self.canvas.pack(pady=5)

        self.result_lbl = tk.Label(
            self.stage_frame,
            text="READY TO ROLL!",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme["gold"],
            bg=self.theme["card_bg"]
        )
        self.result_lbl.pack(pady=(10, 2))

        self.sub_result_lbl = tk.Label(
            self.stage_frame,
            text="Click 'ROLL DICE' or press Spacebar",
            font=("Segoe UI", 9),
            fg=self.theme["subtext"],
            bg=self.theme["card_bg"]
        )
        self.sub_result_lbl.pack(pady=(0, 10))

        # Prediction Mini-Game Box
        game_box = tk.Frame(self.stage_frame, bg=self.theme["bg"], padx=12, pady=8, highlightthickness=1, highlightbackground=self.theme["border"])
        game_box.pack(fill=tk.X, pady=5)

        g_head = tk.Frame(game_box, bg=self.theme["bg"])
        g_head.pack(fill=tk.X, pady=(0, 5))

        tk.Label(g_head, text="🎯 PREDICTION CHALLENGE", font=("Segoe UI", 9, "bold"), fg=self.theme["gold"], bg=self.theme["bg"]).pack(side=tk.LEFT)
        self.streak_lbl = tk.Label(g_head, text="Streak: 0 🔥", font=("Segoe UI", 9, "bold"), fg=self.theme["subtext"], bg=self.theme["bg"])
        self.streak_lbl.pack(side=tk.RIGHT)

        predict_btn_frame = tk.Frame(game_box, bg=self.theme["bg"])
        predict_btn_frame.pack(fill=tk.X)

        self.pred_btns = {}
        for mode, label in [("under", "Under 7 (<7)"), ("exact", "Lucky 7 (=7)"), ("over", "Over 7 (>7)")]:
            btn = tk.Button(
                predict_btn_frame,
                text=label,
                font=("Segoe UI", 9, "bold"),
                fg=self.theme["text"],
                bg=self.theme["card_bg"],
                activebackground=self.theme["accent"],
                activeforeground="#FFFFFF",
                bd=0,
                pady=5,
                cursor="hand2",
                command=lambda m=mode: self.select_prediction(m)
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
            self.pred_btns[mode] = btn

        # Roll Action Button
        self.roll_btn = tk.Button(
            self.root,
            text="🎲 ROLL DICE",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg=self.theme["accent"],
            activebackground=self.theme["accent_hover"],
            activeforeground="#FFFFFF",
            bd=0,
            pady=12,
            cursor="hand2",
            command=self.roll_dice_animated
        )
        self.roll_btn.pack(fill=tk.X, padx=25, pady=12)

        # Statistics Cards Container
        stats_container = tk.Frame(self.root, bg=self.theme["bg"])
        stats_container.pack(fill=tk.X, padx=25, pady=0)

        self.stat_cards = {}
        metrics = [
            ("rolls", "Total Rolls", "0"),
            ("doubles", "Doubles", "0"),
            ("avg", "Avg Sum", "0.0"),
            ("highest", "Highest Sum", "0")
        ]

        for key, label_text, default_val in metrics:
            card = tk.Frame(
                stats_container,
                bg=self.theme["card_bg"],
                padx=10,
                pady=8,
                highlightthickness=1,
                highlightbackground=self.theme["border"]
            )
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

            val_lbl = tk.Label(card, text=default_val, font=("Segoe UI", 14, "bold"), fg=self.theme["text"], bg=self.theme["card_bg"])
            val_lbl.pack()

            txt_lbl = tk.Label(card, text=label_text, font=("Segoe UI", 7, "bold"), fg=self.theme["subtext"], bg=self.theme["card_bg"])
            txt_lbl.pack()

            self.stat_cards[key] = val_lbl

        # History Header & Box
        hist_head = tk.Frame(self.root, bg=self.theme["bg"])
        hist_head.pack(fill=tk.X, padx=25, pady=(12, 4))

        tk.Label(hist_head, text="📜 ROLL HISTORY", font=("Segoe UI", 10, "bold"), fg=self.theme["subtext"], bg=self.theme["bg"]).pack(side=tk.LEFT)
        reset_btn = tk.Button(
            hist_head,
            text="Reset Stats",
            font=("Segoe UI", 8, "bold"),
            fg=self.theme["subtext"],
            bg=self.theme["card_bg"],
            activebackground=self.theme["border"],
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.reset_stats
        )
        reset_btn.pack(side=tk.RIGHT)

        self.history_box = tk.Text(
            self.root,
            height=5,
            bg=self.theme["card_bg"],
            fg=self.theme["text"],
            font=("Consolas", 9),
            bd=0,
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            padx=12,
            pady=8
        )
        self.history_box.pack(fill=tk.X, padx=25, pady=(0, 15))
        self.history_box.insert(tk.END, "No rolls recorded yet.\n")
        self.history_box.config(state=tk.DISABLED)

        # Spacebar shortcut
        self.root.bind("<space>", lambda e: self.roll_dice_animated())

    def play_sound(self, sound_type="roll"):
        if self.sound_enabled and HAS_SOUND and sys.platform.startswith("win"):
            try:
                if sound_type == "roll":
                    winsound.Beep(480, 30)
                elif sound_type == "land":
                    winsound.Beep(220, 70)
                elif sound_type == "win":
                    winsound.Beep(659, 90)
                    winsound.Beep(880, 140)
            except Exception:
                pass

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.config(text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF")

    def change_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.theme = self.THEMES[theme_name]

        self.root.configure(bg=self.theme["bg"])
        self.stage_frame.configure(bg=self.theme["card_bg"], highlightbackground=self.theme["border"])
        self.canvas.configure(bg=self.theme["bg"], highlightbackground=self.theme["border"])
        self.roll_btn.configure(bg=self.theme["accent"], activebackground=self.theme["accent_hover"])
        self.result_lbl.configure(fg=self.theme["gold"], bg=self.theme["card_bg"])
        self.sub_result_lbl.configure(fg=self.theme["subtext"], bg=self.theme["card_bg"])
        self.history_box.configure(bg=self.theme["card_bg"], fg=self.theme["text"], highlightbackground=self.theme["border"])

        for card in self.stat_cards.values():
            card.master.configure(bg=self.theme["card_bg"], highlightbackground=self.theme["border"])
            card.configure(fg=self.theme["text"], bg=self.theme["card_bg"])

        self.draw_dice(self.game.history[0]["dice"] if self.game.history else [1] * self.game.num_dice)

    def select_prediction(self, mode):
        if self.game.prediction == mode:
            self.game.prediction = None
        else:
            self.game.prediction = mode

        for m, btn in self.pred_btns.items():
            if m == self.game.prediction:
                btn.configure(bg=self.theme["gold"], fg="#000000")
            else:
                btn.configure(bg=self.theme["card_bg"], fg=self.theme["text"])

    def on_dice_count_change(self):
        count = self.dice_count_var.get()
        self.game.set_dice_count(count)
        self.draw_dice([1] * count)

    def draw_dice(self, values, offsets=None, rotation_angle=0):
        self.canvas.delete("all")
        count = len(values)
        size = 84
        gap = 22

        total_width = count * size + (count - 1) * gap
        start_x = (530 - total_width) / 2
        start_y = (170 - size) / 2

        for i, val in enumerate(values):
            ox, oy = offsets[i] if offsets and i < len(offsets) else (0, 0)
            x = start_x + i * (size + gap) + ox
            y = start_y + oy

            # Drop Shadow
            self.canvas.create_rectangle(x + 5, y + 5, x + size + 5, y + size + 5, fill="#05070B", outline="", tags="shadow")

            is_double = (count == 2 and values[0] == values[1] and offsets is None)
            die_bg = self.theme["gold"] if is_double else self.theme["die_bg"]
            die_border = self.theme["gold"] if is_double else self.theme["die_border"]

            self.draw_rounded_rectangle(x, y, x + size, y + size, radius=16, fill=die_bg, outline=die_border, width=2)
            self.draw_pips(x, y, size, val)

            if is_double:
                self.canvas.create_rectangle(x - 2, y - 2, x + size + 2, y + size + 2, outline=self.theme["gold"], width=2)

        self.update_particles()

    def draw_rounded_rectangle(self, x1, y1, x2, y2, radius=15, **kwargs):
        points = [
            x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius,
            x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_pips(self, x, y, size, value):
        r = size * 0.088
        dot_color = self.theme["die_pip"]

        cx, cy = x + size / 2, y + size / 2
        l, r_pos = x + size * 0.27, x + size * 0.73
        t, b = y + size * 0.27, y + size * 0.73

        pips_map = {
            1: [(cx, cy)],
            2: [(l, t), (r_pos, b)],
            3: [(l, t), (cx, cy), (r_pos, b)],
            4: [(l, t), (r_pos, t), (l, b), (r_pos, b)],
            5: [(l, t), (r_pos, t), (cx, cy), (l, b), (r_pos, b)],
            6: [(l, t), (r_pos, t), (l, cy), (r_pos, cy), (l, b), (r_pos, b)]
        }

        for px, py in pips_map.get(value, []):
            self.canvas.create_oval(px - r, py - r, px + r, py + r, fill=dot_color, outline="")

    def roll_dice_animated(self):
        if self.is_rolling:
            return

        self.is_rolling = True
        self.roll_btn.config(state=tk.DISABLED, text="🎲 ROLLING...")
        count = self.game.num_dice

        steps = 14
        interval = 35  # ms

        def animate(step):
            if step < steps:
                temp_vals = [random.randint(1, 6) for _ in range(count)]
                offsets = [(random.randint(-6, 6), random.randint(-6, 6)) for _ in range(count)]
                self.draw_dice(temp_vals, offsets, rotation_angle=step * 25)
                self.play_sound("roll")
                self.root.after(interval + step * 2, animate, step + 1)
            else:
                self.finish_roll()

        animate(0)

    def finish_roll(self):
        result = self.game.roll()
        self.play_sound("land")

        if result["is_double"] or result["won_prediction"]:
            self.play_sound("win")
            self.spawn_particles()

        self.draw_dice(result["dice"])

        dice_str = " + ".join(str(d) for d in result["dice"])
        if result["is_double"]:
            self.result_lbl.config(text=f"🎉 DOUBLE {result['dice'][0]}s! (Sum: {result['sum']})", fg=self.theme["gold"])
        else:
            self.result_lbl.config(text=f"ROLLED: [{dice_str}] → SUM: {result['sum']}", fg=self.theme["text"])

        subtext = f"Dice breakdown: {dice_str}"
        if result["prediction"]:
            if result["won_prediction"]:
                subtext += f" | 🎯 Prediction Correct! (+1 Streak)"
            else:
                subtext += f" | ❌ Prediction Missed"
        self.sub_result_lbl.config(text=subtext)
        self.streak_lbl.config(text=f"Streak: {result['streak']} 🔥")

        self.stat_cards["rolls"].config(text=str(self.game.total_rolls))
        self.stat_cards["doubles"].config(text=str(self.game.doubles_count))
        self.stat_cards["avg"].config(text=str(self.game.get_average_sum()))
        self.stat_cards["highest"].config(text=str(self.game.get_highest_sum()))

        self.history_box.config(state=tk.NORMAL)
        if self.game.total_rolls == 1:
            self.history_box.delete("1.0", tk.END)

        log_str = f"Roll #{result['roll_number']:02d}: [{dice_str}] -> Sum: {result['sum']}"
        if result["is_double"]:
            log_str += " ⭐ DOUBLE!"
        if result["won_prediction"]:
            log_str += " 🎯 WIN!"

        self.history_box.insert("1.0", log_str + "\n")
        self.history_box.config(state=tk.DISABLED)

        self.is_rolling = False
        self.roll_btn.config(state=tk.NORMAL, text="🎲 ROLL DICE")

    def spawn_particles(self):
        colors = ["#F59E0B", "#6366F1", "#10B981", "#EC4899", "#3B82F6"]
        self.particles = []
        for _ in range(35):
            self.particles.append({
                "x": random.randint(100, 430),
                "y": random.randint(30, 140),
                "vx": random.uniform(-4, 4),
                "vy": random.uniform(-5, -1),
                "color": random.choice(colors),
                "size": random.randint(4, 8),
                "life": 1.0
            })

    def update_particles(self):
        if not self.particles:
            return

        alive = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.35
            p["life"] -= 0.04

            if p["life"] > 0:
                alive.append(p)
                self.canvas.create_oval(
                    p["x"] - p["size"], p["y"] - p["size"],
                    p["x"] + p["size"], p["y"] + p["size"],
                    fill=p["color"], outline=""
                )
        self.particles = alive
        if alive:
            self.root.after(30, self.draw_dice, self.game.history[0]["dice"] if self.game.history else [1] * self.game.num_dice)

    def reset_stats(self):
        self.game.reset()
        self.draw_dice([1] * self.game.num_dice)
        self.result_lbl.config(text="READY TO ROLL!", fg=self.theme["gold"])
        self.sub_result_lbl.config(text="Click 'ROLL DICE' or press Spacebar")
        self.streak_lbl.config(text="Streak: 0 🔥")

        for key, default in [("rolls", "0"), ("doubles", "0"), ("avg", "0.0"), ("highest", "0")]:
            self.stat_cards[key].config(text=default)

        self.history_box.config(state=tk.NORMAL)
        self.history_box.delete("1.0", tk.END)
        self.history_box.insert(tk.END, "Stats reset.\n")
        self.history_box.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumDiceUI(root)
    root.mainloop()