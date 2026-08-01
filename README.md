# claude-experiments
Noob playing with Claude-Code

This repo contains two small games built while experimenting with Claude Code.

## Guessing Game (`guessing_game.py`)

A simple command-line game where the computer picks a random number between
1 and 100, and you try to guess it.

### Requirements

- Python 3

### How to run

```bash
python3 guessing_game.py
```

### Controls

- Type a whole number and press Enter to guess.

The game tells you if your guess is too high or too low, and reports how
many guesses it took once you find the correct number.

## Snake (`index.html`)

A classic Snake game that runs entirely in the browser, with retro
procedural sound effects and a persistent high score.

### Requirements

- Any modern web browser

### How to run

Open `index.html` directly in your browser (double-click it, or open it via
your editor/IDE). No server or build step needed.

### Controls

- **Arrow keys** or **WASD** — move the snake
- **Space** — restart after a game over
- Click **Restart** — also restarts after a game over

Eat the red food to grow and score points; the game speeds up every 5
points. Hitting a wall or yourself ends the game. Your best score is saved
in the browser's local storage, so it persists across page refreshes.
