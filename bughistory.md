# Bug history

Resolved issues and intended behaviors moved from [knownbugs.md](knownbugs.md). Original issue numbers, descriptions, reproduction steps, and verification notes are preserved. Descriptions record the original behavior before the fixes.

| Code | Meaning |
|  P1  | High Priority - Game-breaking |
|  P2  | Normal-priority bug |
|  P3  | Lower-priority issue |
|  IB  | Intended behavior |
|  IR  | Issue resolved |
|  RT  | Requires testing |

## 1. Releasing fire bypasses the cooldown (IB)

- Location: `player.py`, `Player.update()`.
- Releasing Space resets `shot_cd_counter` to zero, so the next press fires immediately regardless of the remaining cooldown.
- Reproduction: press, release, and press Space on consecutive frames. Two shots fire within three frames despite the initial 0.6-second cooldown.
- Expected: the cooldown expires based on elapsed time, including time spent with Space released.
- Suggested fix: decrement the cooldown every update, clamping it to zero, regardless of whether Space is pressed. Fire only when Space is pressed and the cooldown has expired, then set the next cooldown to `60 / self.shot_rate`. Remove the release-time reset.

## 2. Diagonal movement exceeds the speed limit (IR)

- Location: `player.py`, `Player.move()`.
- Each velocity component is capped separately. At a 45-degree heading, the resulting speed can reach approximately 636 with the current configured limit of 450.
- Reproduction: accelerate at a 45-degree heading until both components reach their limits.
- Expected: total movement speed stays within `PLAYER_SPD_LIMIT` regardless of heading.
- Suggested fix: after acceleration, compare `self.velocity.length_squared()` with `PLAYER_SPD_LIMIT ** 2`; if it exceeds that value, call `self.velocity.scale_to_length(PLAYER_SPD_LIMIT)` instead of clamping each component.

- Resolution verification (2026-11-01): Verified total speed at 24 headings, forward and reverse thrust, and 30/60/120 FPS (144 cases). Speed stayed within the limit at every step and reached the configured maximum.

## 3. Position can cross the intended screen boundary after clamping (IR)

- Location: `player.py`, `Player.clamp_to_screen()` and `Player.update()`.
- Clamping happens before the position update, allowing movement to cross the boundary in the same frame. The half-radius margin also allows the drawn triangle to extend outside the screen at the clamped position.
- Reproduction: approach the right edge at maximum speed. With the current settings, a checked frame ended at x=1911.5 against a center-position limit of 1905, with a triangle vertex at x=1931.5 on a 1920-wide screen.
- Expected: the player center remains within the intended half-radius boundaries after movement. Partial overlap of the visible ship beyond the screen is intentional.
- Suggested fix: update position before clamping. Use the minimum and maximum x/y coordinates of `triangle()` to calculate the correction needed to keep every vertex inside the screen, including a margin for the outline. Apply that correction to the player position.

- Resolution verification (2026-11-01): Verified position after update against the intended half-radius boundaries at all four walls and a corner, using dt values of 1/120, 1/60, 1/30, and 0.1 seconds (20 cases). Clamping now follows movement. Partial ship overlap beyond the screen is intentional; keeping the entire triangle visible is not required.

## 4. Boundary clamping reverses velocity even when moving inward (IR)

- Location: `player.py`, `Player.clamp_to_screen()`.
- The inclusive boundary checks reverse velocity without checking its direction. A player exactly at an edge and already moving away from that edge is bounced back toward it.
- Reproduction: place the player at the left clamp boundary with x velocity +100 and call `clamp_to_screen()`. The velocity becomes -50 despite already pointing into the screen.
- Expected: reverse only the component directed out of the screen. This is separate from the position and margin issue above.
- Suggested fix: correct the position when it crosses a boundary, but reverse x velocity only when it points left at the left boundary or right at the right boundary. Apply the equivalent sign checks to y velocity at the top and bottom boundaries.

## 5. Main menu runs without a frame limit (IR)

- Location: `main.py`, `main()`.
- The menu repeatedly clears, draws, and flips the display without a clock tick or delay. On systems where display flipping does not block, this consumes CPU continuously while the menu is idle.
- Reproduction: leave the game at the main menu and observe CPU usage on a system without blocking display synchronization.
- Expected: limit menu frame rate, as the gameplay loop already does.
- Verification: confirmed by code inspection; CPU usage has not been measured in a graphical session.
- Suggested fix: create a menu `pygame.time.Clock()` and call `tick(60)` once per menu iteration. Keep this separate from the gameplay clock so time spent in a round does not become a menu simulation timestep.

- Resolution verification (2026-11-01): Ran 60 actual menu iterations with a real Pygame clock and SDL dummy display. Every iteration called tick(60); elapsed wall time was 0.970 seconds and CPU time was 0.162 seconds. Graphical window behavior was not tested.

## 6. Small asteroids are removed before entering the screen (IR)

- Location: `spawnfield.py`, `SpawnField.edges`; `circleshape.py`, `CircleShape.inbounds()`; `asteroid.py`, `Asteroid.update()`.
- Spawn positions use `ASTEROID_MAX_RADIUS`, but the cleanup margin uses each asteroid's own radius multiplied by seven. At the current scale, the spawn offset is 157 pixels while the smallest asteroid's cleanup margin is only 154 pixels.
- Reproduction: spawn a minimum-radius asteroid at the midpoint of any edge, moving straight inward at speed 40, and update it with `dt=1/60`. It is killed while still outside the screen. All four edges reproduced this. Faster small asteroids can also fail if they do not cover the gap in their first update.
- Expected: newly spawned asteroids survive their approach into the play area.
- Suggested fix: give asteroids a cleanup region that includes every legal spawn location, such as a shared margin of at least `ASTEROID_MAX_RADIUS`, or spawn each asteroid just beyond the edge using its own radius. Keep cleanup rules appropriate for shots as well; do not accidentally give all shots a large retention area.

- Resolution verification (2026-11-01): Verified minimum-radius asteroids at the start, midpoint, and end of all four spawn edges (12 paths). Each survived 300 updates at dt=1/60 and speed 40 and reached the screen. Cleanup now uses a shared margin of 1.1 times ASTEROID_MAX_RADIUS, including for shots.

## 8. Importing the entry module fails due to a circular import (IR)

- Location: `main.py`, `from game import *` and module-level display creation; `game.py`, `from main import screen`.
- Importing `main` loads `game`, which tries to import `screen` before `main` has created it. Running `main.py` as a script can take a different path because it initially loads as `__main__`, so this finding concerns module imports and reuse rather than a claim that normal script startup always fails.
- Reproduction: `.venv/bin/python -B -c 'import main'` raises `ImportError: cannot import name 'screen' from 'main'`. Confirmed with SDL's dummy video/audio drivers.
- Expected: importing the entry module succeeds without opening a window or starting the game.
- Suggested fix: initialize Pygame and create the display inside `main()`, import the game function explicitly, and pass the display to `game(screen)`. Remove the import of `main` from `game.py`.


- Resolution verification: Previously verified that importing main succeeds without creating a display, and that gameplay starts and exits using the shared display. Original priority: P3.

## 9. HUD text is clipped at smaller configured resolutions (IR)

- Location: `game.py`, `Rendered_Stats` position; `rendered_text.py`, `Rendered_Stats.draw()` and the fixed-size general font.
- The HUD starts at `SCREEN_WIDTH - 800`, uses fixed offsets of 270 and 600 pixels, and keeps a 30-pixel font regardless of resolution. These values do not scale with the configurable window width.
- Reproduction: use a width of 640. The stats start at x=-160, placing almost all of the muzzle-velocity label outside the left edge. An isolated render with the current label measured its right edge at x=4.
- Expected: all HUD labels remain visible at supported window sizes.
- Suggested fix: calculate HUD placement from the actual window width and measured text widths, with consistent padding. Scale the font or wrap the stats onto additional rows when necessary; define and validate a minimum supported resolution if needed.

- Resolution: HUD placement now uses `SCREEN_WIDTH - 500 * SCALE`, label offsets use `185 * SCALE` and `390 * SCALE`, and both score and stats render at font size `20 * SCALE`. These values scale with the configured screen height. Original priority: P2.
- Resolution verification (2026-11-04): Passed headless Pygame rendering checks at 640×360, 800×450, 1280×720, 1920×1080, 2560×1440, 640×480, 800×600, and 1280×1024. Ran one actual gameplay frame at each resolution and separately rendered stats with all upgrades at maximum. Compared each label against an unclipped reference render and checked screen containment and label overlap; all passed. At 640×360, the maximum-upgrade labels occupy x=390–639, fully inside the screen. Tested with SDL dummy video/audio drivers; a graphical desktop session and arbitrary aspect ratios were not tested.
