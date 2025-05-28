![Logo](ui/logo.png)

# 🕹️ Terminal FNaF

**Terminal FNaF** — is a terminal game inspired by the original *Five Nights at Freddy's* series. The player has to survive the night in the security room, watching the animatronics and controlling the doors and lights to prevent them from getting in.

---

## 📦 Installation

### 🔧 Requirements

- Python **3.8 or newer**
- Library `curses`  
  - **Linux/macOS**: set by default
  - **Windows**: install via pip:
    ```bash
    pip install windows-curses
    ```

### 📥 Cloning a repository

```bash
git clone https://github.com/Lonja971/Terminal-FNAF.git
cd P-FNAF
```

### ▶️ Launching the game

```bach
cd Terminal-FNAF
python main.py
```

## 🎮 Control

| Key     | Action                           |
| ------- | -------------------------------- |
| `A`     | Move the view to the left        |
| `D`     | Move the view to the right       |
| `K`     | Turn on/off the light            |
| `L`     | Open/close the door              |
| `SPACE` | Open/close cameras               |
| `1`–`9` | Switch to the appropriate camera |
| `Q`     | Exit the game                    |
| `P`     | Pause                            |

## 🧠 Gameplay

- Monitor your animatronics with cameras.
- Each action (doors, lights, cameras) consumes energy.
- If the animatronic reaches the room and the door is open, the game is over.
- Survive the night from 12:00 AM to 6:00 AM to win.

## ⚠️ Notes

- The terminal must support at least 130/40 characters for the correct display of the interface.
- It is recommended to run the game in full screen mode for the best experience.