from key_player import KeyPlayer
from piano_recorder import PianoRecorder
from generic_functions import GenericFunctions


class Piano(GenericFunctions):
    key_player = KeyPlayer()
    piano_recorder = PianoRecorder()

    def play_key(self, key: str) -> None:
        self.key_player.key = key
        self.start_new_thread(self.key_player.play_key)
        self.update_piano_recorder_key(key)

    def update_piano_recorder_key(self, key: str) -> None:
        if self.piano_recorder.recording:
            self.piano_recorder.key = key
