# Task 1: Dice Rolling Game 🎲

A desktop dice rolling game built with Python and Tkinter. It simulates rolling dice, displays the results, and lets you roll again, plus extras like animations, a prediction mini-game, statistics, and color themes.

## Task Requirements

| Requirement | How it's covered |
|---|---|
| Randomly generate two numbers between 1 and 6 | Two dice by default, using `random.randint(1, 6)` |
| Display the results | Dice faces are drawn on a canvas, with the sum shown below |
| Ask if the user wants to roll again | Click **ROLL DICE** or press **Spacebar** to roll again |

## Features

- **1 to 4 dice:** choose how many dice to roll
- **Animated roll:** dice shake and change faces before landing on the result
- **Doubles detection:** doubles are highlighted in gold with a celebration effect
- **Prediction challenge:** guess whether the sum will be under 7, exactly 7, or over 7 and build a winning streak
- **Live statistics:** total rolls, doubles count, average sum, and highest sum
- **Roll history:** a log of every roll in the session
- **4 color themes:** Obsidian Dark, Cyber Neon, Gold Casino, Emerald Luxury
- **Sound effects:** toggle on or off (Windows only)
- **Reset button:** clear all stats and start fresh

## Requirements

- Python 3.8 or higher
- Tkinter (included with the standard Python installer)

No external packages are needed.

## How to Run

```bash
python DiceGame.py
```

## How to Play

1. Choose how many dice you want (default is 2).
2. *(Optional)* Pick a prediction: **Under 7**, **Lucky 7**, or **Over 7**.
3. Click **ROLL DICE** or press **Spacebar**.
4. Check your result, streak, stats, and history.
5. Roll again as many times as you like, or press **Reset Stats** to start over.

## Project Structure

```
Python-Task1-DiceGame/
├── DiceGame.py        # Game logic and Tkinter UI
├── README.md
└── Screenshots/

```

## Code Overview

- **`DiceGame`** class: game logic only (rolling, doubles, streaks, statistics). It has no UI code, so it's easy to test on its own.
- **`PremiumDiceUI`** class: the Tkinter interface, dice drawing, animation, themes, and sound.

## Notes

- Sound effects use `winsound`, so they only work on Windows. On other systems the game runs normally without sound.
- The doubles counter applies when exactly 2 dice are selected.
- The prediction challenge compares the total against 7, which is the most balanced target for 2 dice.
