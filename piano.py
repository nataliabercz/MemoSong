import time
import pygame
from piano_recorder import PianoRecorder
from recording_manager import RecordingManager
from generic_functions import GenericFunctions


class Piano(GenericFunctions):
    key = None
    piano_recorder = PianoRecorder()
    recording_manager = RecordingManager()

    def play_key(self) -> None:
        key = self.key
        pygame.mixer.Sound.play(pygame.mixer.Sound(f'{self.keys_path}/{self.key_map[key]}.wav'))
        self.recording_manager.update_piano_recorder_key(self.key)
        time.sleep(0.03)
        self.remove_button_highlight(key)
