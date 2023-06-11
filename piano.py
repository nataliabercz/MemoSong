import pygame
from piano_recorder import PianoRecorder
from recording_manager import RecordingManager
from generic_functions import GenericFunctions


class Piano(GenericFunctions):
    piano_recorder = PianoRecorder()
    recording_manager = RecordingManager()

    def play_key(self, key: str) -> None:
        pygame.mixer.Sound.play(pygame.mixer.Sound(f'{self.keys_path}/{self.key_map[key]}.wav'))
        self.recording_manager.update_piano_recorder_key(key)
