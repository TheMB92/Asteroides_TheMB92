# Known bugs

Issues recorded during review. P2 indicates a normal-priority bug; P3 indicates a lower-priority issue.

Five additional review passes covered input and movement; collision detection; spawning and upgrades; startup and game lifecycle; and settings, rendering, and logging. New findings below were checked with isolated runtime reproductions. No game source was changed. This review does not guarantee that every bug has been found.

## 1. Releasing fire bypasses the cooldown (P2)

- Location: `player.py`, `Player.update()`.
- Releasing Space resets `shot_cd_counter` to zero, so the next press fires immediately regardless of the remaining cooldown.
- Reproduction: press, release, and press Space on consecutive frames. Two shots fire within three frames despite the initial 0.6-second cooldown.
- Expected: the cooldown expires based on elapsed time, including time spent with Space released.
- Suggested fix: decrement the cooldown every update, clamping it to zero, regardless of whether Space is pressed. Fire only when Space is pressed and the cooldown has expired, then set the next cooldown to `60 / self.shot_rate`. Remove the release-time reset.

## 2. Diagonal movement exceeds the speed limit (P2)

- Location: `player.py`, `Player.move()`.
- Each velocity component is capped separately. At a 45-degree heading, the resulting speed can reach approximately 636 with the current configured limit of 450.
- Reproduction: accelerate at a 45-degree heading until both components reach their limits.
- Expected: total movement speed stays within `PLAYER_SPD_LIMIT` regardless of heading.
- Suggested fix: after acceleration, compare `self.velocity.length_squared()` with `PLAYER_SPD_LIMIT ** 2`; if it exceeds that value, call `self.velocity.scale_to_length(PLAYER_SPD_LIMIT)` instead of clamping each component.

## 3. The player can extend beyond the screen (P2)

- Location: `player.py`, `Player.clamp_to_screen()` and `Player.update()`.
- Clamping happens before the position update, allowing movement to cross the boundary in the same frame. The half-radius margin also allows the drawn triangle to extend outside the screen at the clamped position.
- Reproduction: approach the right edge at maximum speed. With the current settings, a checked frame ended at x=1911.5 against a center-position limit of 1905, with a triangle vertex at x=1931.5 on a 1920-wide screen.
- Expected: the player remains within the screen after movement, accounting for the ship's visible shape.
- Suggested fix: update position before clamping. Use the minimum and maximum x/y coordinates of `triangle()` to calculate the correction needed to keep every vertex inside the screen, including a margin for the outline. Apply that correction to the player position.

## 4. Boundary clamping reverses velocity even when moving inward (P2)

- Location: `player.py`, `Player.clamp_to_screen()`.
- The inclusive boundary checks reverse velocity without checking its direction. A player exactly at an edge and already moving away from that edge is bounced back toward it.
- Reproduction: place the player at the left clamp boundary with x velocity +100 and call `clamp_to_screen()`. The velocity becomes -50 despite already pointing into the screen.
- Expected: reverse only the component directed out of the screen. This is separate from the position and margin issue above.
- Suggested fix: correct the position when it crosses a boundary, but reverse x velocity only when it points left at the left boundary or right at the right boundary. Apply the equivalent sign checks to y velocity at the top and bottom boundaries.

## 5. Main menu runs without a frame limit (P2)

- Location: `main.py`, `main()`.
- The menu repeatedly clears, draws, and flips the display without a clock tick or delay. On systems where display flipping does not block, this consumes CPU continuously while the menu is idle.
- Reproduction: leave the game at the main menu and observe CPU usage on a system without blocking display synchronization.
- Expected: limit menu frame rate, as the gameplay loop already does.
- Verification: confirmed by code inspection; CPU usage has not been measured in a graphical session.
- Suggested fix: create a menu `pygame.time.Clock()` and call `tick(60)` once per menu iteration. Keep this separate from the gameplay clock so time spent in a round does not become a menu simulation timestep.

## 6. Small asteroids are removed before entering the screen (P2)

- Location: `spawnfield.py`, `SpawnField.edges`; `circleshape.py`, `CircleShape.inbounds()`; `asteroid.py`, `Asteroid.update()`.
- Spawn positions use `ASTEROID_MAX_RADIUS`, but the cleanup margin uses each asteroid's own radius multiplied by seven. At the current scale, the spawn offset is 157 pixels while the smallest asteroid's cleanup margin is only 154 pixels.
- Reproduction: spawn a minimum-radius asteroid at the midpoint of any edge, moving straight inward at speed 40, and update it with `dt=1/60`. It is killed while still outside the screen. All four edges reproduced this. Faster small asteroids can also fail if they do not cover the gap in their first update.
- Expected: newly spawned asteroids survive their approach into the play area.
- Suggested fix: give asteroids a cleanup region that includes every legal spawn location, such as a shared margin of at least `ASTEROID_MAX_RADIUS`, or spawn each asteroid just beyond the edge using its own radius. Keep cleanup rules appropriate for shots as well; do not accidentally give all shots a large retention area.

## 7. Fast objects can pass through collisions during slow frames (P2)

- Location: `game.py`, updates followed by collision checks; `shot.py`, `Shot.update()`; `asteroid.py`, `Asteroid.update()`.
- Collision checks use only the final positions after an entire frame's movement. An object can cross another object's collision area and finish beyond it without either sampled position overlapping.
- Reproduction: place a minimum-radius asteroid at (500, 500), and a shot at (420, 500) moving right at the current maximum shot speed of 1500. After a 0.1-second update, the shot is at (570, 500). Both endpoint collision checks return false even though the shot crossed the asteroid.
- Expected: hits along the movement path are detected, including during frame stalls.
- Suggested fix: use swept collision detection with previous and current positions, testing the relative movement segment against the sum of the collision radii. Alternatively, use a fixed simulation timestep with enough substeps to keep displacement small, checking collisions during each substep. Simply discarding excess elapsed time changes game timing and scoring.

## 8. Importing the entry module fails due to a circular import (P3)

- Location: `main.py`, `from game import *` and module-level display creation; `game.py`, `from main import screen`.
- Importing `main` loads `game`, which tries to import `screen` before `main` has created it. Running `main.py` as a script can take a different path because it initially loads as `__main__`, so this finding concerns module imports and reuse rather than a claim that normal script startup always fails.
- Reproduction: `.venv/bin/python -B -c 'import main'` raises `ImportError: cannot import name 'screen' from 'main'`. Confirmed with SDL's dummy video/audio drivers.
- Expected: importing the entry module succeeds without opening a window or starting the game.
- Suggested fix: initialize Pygame and create the display inside `main()`, import the game function explicitly, and pass the display to `game(screen)`. Remove the import of `main` from `game.py`.

## 9. HUD text is clipped at smaller configured resolutions (P2)

- Location: `game.py`, `Rendered_Stats` position; `rendered_text.py`, `Rendered_Stats.draw()` and the fixed-size general font.
- The HUD starts at `SCREEN_WIDTH - 800`, uses fixed offsets of 270 and 600 pixels, and keeps a 30-pixel font regardless of resolution. These values do not scale with the configurable window width.
- Reproduction: use a width of 640. The stats start at x=-160, placing almost all of the muzzle-velocity label outside the left edge. An isolated render with the current label measured its right edge at x=4.
- Expected: all HUD labels remain visible at supported window sizes.
- Suggested fix: calculate HUD placement from the actual window width and measured text widths, with consistent padding. Scale the font or wrap the stats onto additional rows when necessary; define and validate a minimum supported resolution if needed.
