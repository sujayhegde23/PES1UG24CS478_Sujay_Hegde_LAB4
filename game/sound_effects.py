import math
from array import array

import pygame


class SoundEffects:
    """Small generated tones used for gameplay feedback.

    Keeping the effects in code avoids requiring external audio assets. If an
    audio device is unavailable, the game continues silently.
    """

    def __init__(self):
        self.hit = None
        self.miss = None
        self.round_end = None

        mixer_settings = pygame.mixer.get_init()
        if not mixer_settings:
            return

        self.sample_rate, sample_size, self.channels = mixer_settings
        if sample_size != -16:
            return

        try:
            self.hit = self._make_tone(880, 0.12, 0.65)
            self.miss = self._make_tone(220, 0.18, 0.55)
            self.round_end = self._make_tone(440, 0.45, 0.65)
        except pygame.error:
            # Sound is optional feedback; do not prevent the game from running.
            self.hit = None
            self.miss = None
            self.round_end = None

    def _make_tone(self, frequency, duration, volume):
        sample_count = int(self.sample_rate * duration)
        samples = array("h")

        for index in range(sample_count):
            progress = index / sample_count
            fade = min(1.0, progress * 20, (1.0 - progress) * 20)
            wave = math.sin(2 * math.pi * frequency * index / self.sample_rate)
            sample = int(32767 * volume * fade * wave)
            for _ in range(self.channels):
                samples.append(sample)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play_hit(self):
        if self.hit:
            self.hit.play()

    def play_miss(self):
        if self.miss:
            self.miss.play()

    def play_round_end(self):
        if self.round_end:
            self.round_end.play()
