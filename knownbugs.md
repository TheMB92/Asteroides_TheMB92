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

## 10. Player collision shape does not match the visible ship (P2)

- Location: `player.py`, `Player.triangle()`; `circleshape.py`, `CircleShape.collides_with()`.
- The player is drawn as a triangle, but collision detection uses a circle centered on the player with radius `PLAYER_RADIUS`. The circle includes empty space beside the ship, while the triangle's rear corners extend beyond it.
- Reproduction: approach an asteroid side-on or with a rear corner. Collisions can register before the visible ship touches the asteroid, or visible rear-corner contact can go undetected.
- Expected: collisions agree with the visible player shape at every rotation.
- Suggested fix: use triangle-versus-circle collision detection for player–asteroid collisions, using the vertices returned by `triangle()` and checking both edge distance and whether the asteroid's center lies inside the triangle.

## 11. Holding N can immediately restart after a round ends (P2)

- Location: `main.py`, `main()`, the `keys[pygame.K_n]` check.
- Starting a round checks whether N is held, rather than whether a new press occurred. If N is still held when gameplay returns, the next menu iteration immediately starts another round, replacing the results screen without a fresh request.
- Reproduction: hold N while ending a round with Escape. The menu starts another round while the same N press remains held.
- Verification (2026-11-01): ran the actual menu loop with N continuously pressed and a stub game that returned immediately. The game was called twice without any release or new press. This confirms the menu trigger; the round duration was shortened for an isolated test.
- Expected: starting another round requires a fresh N press in the menu.
- Suggested fix: start rounds from `pygame.KEYDOWN` events for N, or require a release before accepting another press. Avoid processing stale start events after returning from gameplay.

## 12. Event log frame numbers freeze after the snapshot limit (P3)

- Location: `logger.py`, `log_state()` and `log_event()`.
- `log_state()` returns before incrementing `_frame_count` once it exceeds `_FPS * _MAX_SECONDS`. Event logging continues, but every subsequent event reports frame 961, including events in later rounds. This prevents identifying the actual simulation frame of a hit, split, or upgrade.
- Reproduction: set `_frame_count` to 960, call `log_state()` 20 times and log an event; call it another 100 times and log another event. Both events report frame 961.
- Verification (2026-11-01): reproduced with the real logging functions and mocked file writes, preserving existing log files. Both captured event records contained `"frame": 961`.
- Expected: the snapshot limit stops state snapshots while event frame numbers continue to advance.
- Suggested fix: increment the frame counter on every gameplay iteration before applying the state-snapshot limit. Keep the limit on snapshot writing only.

## 13. Spawn timers discard elapsed intervals during long frames (P2)

- Location: `spawnfield.py`, `AsteroidField.update()` and `PowerUpField.update()`.
- Each update handles at most one spawn interval and resets `spawn_timer` to zero. Any remaining elapsed time is discarded. Frame stalls therefore reduce asteroid and powerup spawn frequency relative to survival scoring, which uses the full elapsed time.
- Reproduction: update an asteroid field twice with `dt=1.8`. Only two asteroids spawn over 3.6 seconds, despite the 0.8-second interval. Updating the same total time in 0.1-second steps produces four. For a powerup field, two updates with `dt=6` produce two selection attempts over 12 seconds, versus four attempts with 0.1-second steps at the 3-second interval.
- Verification (2026-11-01): reproduced both comparisons with real field updates and mocked `spawn()` calls. Powerup counts measure selection attempts, since maxed upgrade types can intentionally produce no pickup.
- Expected: spawn scheduling accounts for elapsed intervals and retains the unused remainder, independently of frame rate.
- Suggested fix: subtract the interval instead of resetting to zero, and process each elapsed interval with a loop. If limiting catch-up spawns to avoid bursts, define that policy explicitly and retain the remaining time.
