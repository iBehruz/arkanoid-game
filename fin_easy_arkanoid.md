# FinEasy Arkanoid

This is my Arkanoid-style game built with Pygame for my internship’s Python homework, starting from the Phase 12 base (https://git.epam.com/Anton_Ilchenko/pygame-arkanoid). I added a title screen, mute button, extra levels, a game over screen, and power-ups, with a fintech twist to match my work on banking apps. The game runs locally (Python 3.13.4, Pygame 2.6.1) or in a browser via Pyodide.

## Features

- **Title Screen**: Shows “FinEasy Arkanoid - Press SPACE” to start the game.
- **Mute Button**: Top-right button to toggle sound effects for paddle and brick hits.
- **Three Levels**:
  - Level 1: Simple red brick grid.
  - Level 2: Blue bricks in alternating rows.
  - Level 3: Dense yellow brick grid.
- **Game Over Screen**: Displays “Game Over - Press R to Restart” when you lose all balls or clear all levels.
- **Power-Ups**:
  - *Coin Boost* (yellow): Makes the paddle bigger.
  - *Extra Ball* (blue): Adds another ball to the game.

## Setup

1. **Install Requirements**:
   - Install Python 3.13.4 or later.
   - Install Pygame: `pip install pygame`.
2. **Run the Game**:

   ```bash
   python arkanoid.py
   ```

   For browser use, deploy in a Pyodide environment (e.g., via JupyterLite).

## How to Play

- Press **SPACE** on the title screen to start.
- Use **LEFT** and **RIGHT** arrow keys to move the paddle.
- Click the **Mute/Unmute** button in the top-right to toggle sound.
- Break all bricks to advance levels. Collect power-ups (yellow or blue squares) for boosts.
- If you lose all balls or clear all levels, the game over screen appears. Press **R** to restart.

## Fintech Theme

I named the game “FinEasy Arkanoid” and themed the power-ups (“Coin Boost” and “Extra Ball”) to reflect my work on fintech projects like banking apps and payment systems. It’s a fun way to connect my coding skills to my career goals.

## Notes

- Built for my internship, extending the Phase 12 base with new features.