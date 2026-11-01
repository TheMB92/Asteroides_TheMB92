# Asteroids by TheMB92

My private Python learning project: an Asteroids-style game built with Pygame. I use it to practice game loops, object-oriented programming, vector movement, collision detection, sprite groups, and debugging through small, incremental changes.

The game is a work in progress. This repository also keeps my bug investigations, fixes, and future feature ideas.

## Setup and running

Requirements:

- Python 3.13 or newer (`.python-version` selects 3.13).
- Pygame 2.6.1, declared in `pyproject.toml`.
- A graphical desktop to play the game.

Run these commands from the repository directory. With `uv` installed:

```bash
uv sync
uv run main.py
```

Alternatively, use a virtual environment and pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pygame==2.6.1
python main.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

## Controls

| Key | Action |
| --- | --- |
| N | Start a new round from the menu |
| Q | Quit from the menu |
| W | Apply forward thrust |
| S | Apply reverse thrust |
| A / D | Rotate left / right |
| Space | Fire |
| Escape | End the current round and return to the menu |

Closing the window quits the game. Escape ends a round; it does not pause it.

## Gameplay

Survive incoming asteroids, shoot them to earn points, and collect upgrades. Larger asteroids split into two smaller, faster asteroids when hit. Touching a surviving asteroid ends the round. The menu then shows the last round's score and final weapon stats.

- **Scoring:** 10 points per second survived and 100 points per asteroid hit.
- **Movement:** thrust changes velocity, so the ship keeps drifting when thrust is released. Total speed is capped, and the screen edges bounce the ship inward with reduced velocity.
- **Difficulty:** collecting upgrades increases asteroid spawning frequency; every six collected upgrades also increases the available asteroid sizes and maximum spawn speed.
- **Intentional behavior:** releasing Space resets the firing cooldown, allowing a fresh press to fire immediately. The ship can also partially overlap the screen edges.

### Upgrades

| Pickup color | Upgrade | Effect | Maximum |
| --- | --- | --- | --- |
| Yellow | Fire rate | Adds 100 rounds per minute | 1,000 RPM |
| Magenta | Projectile speed | Adds 100 m/s to the displayed muzzle velocity | 1,000 m/s |
| Dark red | Penetration | Adds one asteroid hit per projectile | 3 hits |

Initial weapon stats are 100 RPM, 300 m/s displayed muzzle velocity, and one hit per projectile. Projectiles also inherit the ship's velocity. Upgrade types already at their maximum can result in skipped spawn attempts, and existing pickups of those types are removed.

## Configuration

Edit `settings.py` before launching:

```python
SCREEN_WIDTH_SETTING = 1920
SCREEN_RATIO = 16 / 9
```

The default window is 1920 × 1080. Height is calculated from the width and aspect ratio. Many sizes and movement values scale relative to a base width of 1280, but HUD layout does not yet adapt fully to smaller resolutions; see [knownbugs.md](knownbugs.md).

Gameplay values such as acceleration, speed limits, scoring, spawn intervals, and upgrade caps live in `constants.py`. Resolution currently requires editing the file; a settings menu and fullscreen support are planned.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Initializes Pygame, creates the shared display, and runs the menu |
| `game.py` | Runs rounds, manages sprite groups, handles collisions, and returns results |
| `player.py` | Ship movement, rotation, firing, and screen boundaries |
| `circleshape.py` | Shared circular-object position, velocity, collision, and bounds logic |
| `asteroid.py` | Asteroid movement, drawing, and splitting |
| `shot.py` | Projectile movement, drawing, and penetration state |
| `powerups.py` | Upgrade pickups and their effects |
| `spawnfield.py` | Asteroid and powerup spawning, plus difficulty increases |
| `rendered_text.py` | Score, weapon stats, menu, and round-results rendering |
| `constants.py` | Game balance values, colors, and scaled dimensions |
| `settings.py` | Window width and aspect ratio |
| `logger.py` | Development state snapshots and event logs |
| `pyproject.toml` / `uv.lock` | Python requirements, dependency declaration, and locked dependencies |

## Development notes

- [Known bugs](knownbugs.md): open findings, reproduction steps, and suggested fixes.
- [Bug history](bughistory.md): resolved issues and intentional behaviors, with verification notes where available. Issue numbers are retained across both files.
- [Future features](futurefeatures.md): planned work, including sprites, irregular asteroid shapes, backgrounds, propulsion effects, lives, a leaderboard, mouse menus, settings, sound, fullscreen, and weapon-changing upgrades.

Both menu and gameplay target 60 FPS. Development checks have included isolated runtime reproductions and rendering checks; there is currently no committed automated test suite. When changing gameplay, check movement, firing, all four screen edges, asteroid splitting, upgrade collection, and returning to the menu. See the bug files for specific regression cases and testing limits.

The logger writes `game_state.jsonl` and `game_events.jsonl` to the working directory. These are ignored by Git. State snapshots are limited to the initial logging window; event logs continue afterward. Each file is overwritten on its first write in a new process, then appended to. The known frame-counter limitation is recorded in `knownbugs.md`.

## License file

The repository includes the GNU GPL version 3 text in [LICENSE](LICENSE).
