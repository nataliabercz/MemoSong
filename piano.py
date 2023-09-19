import time
import pygame
from recording_manager import RecordingManager
from generic_functions import GenericFunctions


class Piano(GenericFunctions):
    key = None
    recording_manager = RecordingManager()

    def play_key(self) -> None:
        key = self.key
        pygame.mixer.Sound.play(pygame.mixer.Sound(f'{self.keys_path}/{self.key_map[key]}.wav'))
        self.recording_manager.update_piano_recorder_key(key)
        time.sleep(0.1)
        self._remove_piano_key_highlight(key)
