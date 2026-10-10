import pygame
import random
from .sound_effects import SoundEffects
from .target import Target

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)
DARK_GRAY = (35, 35, 40)

class GameEngine:
    DIFFICULTIES = {
        "Easy": {"base_radius": 48, "min_radius": 18, "lifespan_frames": 150},
        "Medium": {"base_radius": 40, "min_radius": 12, "lifespan_frames": 90},
        "Hard": {"base_radius": 32, "min_radius": 9, "lifespan_frames": 60},
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.round_seconds = 30
        self.difficulty = "Medium"
        self.font = pygame.font.SysFont("Arial", 26)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.message_font = pygame.font.SysFont("Arial", 22)
        self.sounds = SoundEffects()
        self.exit_requested = False
        self._start_new_round(self.difficulty)

    def _spawn_target(self):
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height, self.height - self.margin)
        return Target(x, y, **self.DIFFICULTIES[self.difficulty])

    def _start_new_round(self, difficulty):
        self.difficulty = difficulty
        self.time_left_frames = self.round_seconds * 60
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.game_over = False
        self.target = self._spawn_target()

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit_requested = True
            elif event.type == pygame.KEYDOWN:
                difficulty_keys = {
                    pygame.K_1: "Easy",
                    pygame.K_2: "Medium",
                    pygame.K_3: "Hard",
                }
                difficulty = difficulty_keys.get(event.key)
                if difficulty:
                    self._start_new_round(difficulty)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.sounds.play_hit()
            self.target = self._spawn_target()
        else:
            self.misses += 1
            self.sounds.play_miss()

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            self.sounds.play_round_end()
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            self.sounds.play_miss()
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        if self.game_over:
            self._render_game_over(screen)
            return

        r = int(self.target.visual_radius())
        pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
        pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))

    def _render_game_over(self, screen):
        screen.fill(DARK_GRAY)

        title = self.title_font.render("Game Over", True, RED)
        score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        accuracy = self.font.render(
            f"Final Accuracy: {self.accuracy()}%", True, WHITE
        )
        instruction = self.message_font.render(
            "Play again: 1 Easy    2 Medium    3 Hard", True, WHITE
        )
        exit_instruction = self.message_font.render(
            "Press Esc or close the window to exit", True, WHITE
        )

        center_x = self.width // 2
        screen.blit(title, title.get_rect(center=(center_x, self.height // 2 - 75)))
        screen.blit(score, score.get_rect(center=(center_x, self.height // 2 - 10)))
        screen.blit(accuracy, accuracy.get_rect(center=(center_x, self.height // 2 + 30)))
        screen.blit(
            instruction,
            instruction.get_rect(center=(center_x, self.height // 2 + 85)),
        )
        screen.blit(
            exit_instruction,
            exit_instruction.get_rect(center=(center_x, self.height // 2 + 120)),
        )
