# Target Aim Trainer

A Pygame aim trainer that uses shrinking targets, score tracking, timed rounds, difficulty selection, and sound feedback.

## Features

- A target spawns at a random position and shrinks while it remains on screen.
- Circular hit detection always uses the same current radius as the visible target.
- Clicking the target scores a hit and spawns a new target immediately.
- Clicking outside the target, or allowing it to expire, records a miss.
- Score, remaining time, and live accuracy are displayed during each round.
- Each round lasts 30 seconds.
- A Game Over screen displays the final score and accuracy.
- Players can start a new round at a selected difficulty or exit the game.
- Generated sound effects play for hits, misses, timeouts, and the end of a round.

The sound effects are generated at runtime, so no audio files need to be downloaded. If an audio device is unavailable, the game continues silently.

## Getting Started

1. Install Python 3.10 or later.
2. Install the dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:

   ```bash
   python main.py
   ```

## Controls

- **Left-click:** Hit the visible target. Clicking anywhere else counts as a miss.
- **Game Over screen:** Press `1` for Easy, `2` for Medium, or `3` for Hard to play again.
- **Exit:** Press `Esc` on the Game Over screen or close the window.

## Difficulty Settings

| Difficulty | Starting radius | Minimum radius | Target lifespan |
| --- | ---: | ---: | ---: |
| Easy | 48 px | 18 px | 150 frames |
| Medium | 40 px | 12 px | 90 frames |
| Hard | 32 px | 9 px | 60 frames |

## Completed Tasks

### Task 1: Refine Collision Detection

`Target.contains_point()` uses the target's current `visual_radius()`. The clickable area therefore shrinks exactly with the circle drawn on screen; late clicks outside the visible circle are misses.

### Task 2: Implement Game Over Condition

When the timer reaches zero, the round stops and displays a Game Over screen with the final score and accuracy. The game waits on this screen for player input instead of printing results to the console.

### Task 3: Add Replay Option

The Game Over screen offers Easy, Medium, and Hard replay choices. Selecting one starts a fresh 30-second round and resets the timer, score, hit count, miss count, and target.

### Task 4: Add Sound Feedback

The game plays a high tone for successful hits, a low tone for missed clicks and expired targets, and a longer tone when the round ends.

## Folder Structure

```text
target-aim-trainer/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── sound_effects.py
│   └── target.py
└── README.md
```

## Video Demo

- [Before changes — raw video](https://github.com/SETAPESU26/47_target-aim-trainer/raw/refs/heads/main/videos/before.mp4)
- [After changes — raw video](https://github.com/SETAPESU26/47_target-aim-trainer/raw/refs/heads/main/videos/after.mp4)
