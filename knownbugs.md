# Known bugs

Issues recorded during review.

| Code | Meaning |
|  P1  | High Priority - Game-breaking |
|  P2  | Normal-priority bug |
|  P3  | Lower-priority issue |
|  IB  | Intended behavior |
|  IR  | Issue resolved |
|  RT  | Requires testing |

Five additional review passes covered input and movement; collision detection; spawning and upgrades; startup and game lifecycle; and settings, rendering, and logging. New findings below were checked with isolated runtime reproductions. No game source was changed. This review does not guarantee that every bug has been found.

Resolved issues are archived in [bughistory.md](bughistory.md). Original issue numbers are retained.

## 7. Fast objects can pass through collisions during slow frames (P2)

- Location: `game.py`, updates followed by collision checks; `shot.py`, `Shot.update()`; `asteroid.py`, `Asteroid.update()`.
- Collision checks use only the final positions after an entire frame's movement. An object can cross another object's collision area and finish beyond it without either sampled position overlapping.
- Reproduction: place a minimum-radius asteroid at (500, 500), and a shot at (420, 500) moving right at the current maximum shot speed of 1500. After a 0.1-second update, the shot is at (570, 500). Both endpoint collision checks return false even though the shot crossed the asteroid.
- Expected: hits along the movement path are detected, including during frame stalls.
- Suggested fix: use swept collision detection with previous and current positions, testing the relative movement segment against the sum of the collision radii. Alternatively, use a fixed simulation timestep with enough substeps to keep displacement small, checking collisions during each substep. Simply discarding excess elapsed time changes game timing and scoring.

## 9. HUD text is clipped at smaller configured resolutions (P2)

- Location: `game.py`, `Rendered_Stats` position; `rendered_text.py`, `Rendered_Stats.draw()` and the fixed-size general font.
- The HUD starts at `SCREEN_WIDTH - 800`, uses fixed offsets of 270 and 600 pixels, and keeps a 30-pixel font regardless of resolution. These values do not scale with the configurable window width.
- Reproduction: use a width of 640. The stats start at x=-160, placing almost all of the muzzle-velocity label outside the left edge. An isolated render with the current label measured its right edge at x=4.
- Expected: all HUD labels remain visible at supported window sizes.
- Suggested fix: calculate HUD placement from the actual window width and measured text widths, with consistent padding. Scale the font or wrap the stats onto additional rows when necessary; define and validate a minimum supported resolution if needed.

## 10. Player collision shape does not match the visible ship (P2)

- Location: `player.py`, `Player.triangle()`; `circleshape.py`, `CircleShape.collides_with()`.
- The player is drawn as a triangle, but collision detection uses a circle centered on the player with radius `PLAYER_RADIUS`. The circle includes empty space beside the ship, while the triangle's rear corners extend beyond it.
- Reproduction: approach an asteroid side-on or with a rear corner. Collisions can register before the visible ship touches the asteroid, or visible rear-corner contact can go undetected.
- Expected: collisions agree with the visible player shape at every rotation.
- Suggested fix: use triangle-versus-circle collision detection for player–asteroid collisions, using the vertices returned by `triangle()` and checking both edge distance and whether the asteroid's center lies inside the triangle.
