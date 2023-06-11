import time
import pydub
import pydub.exceptions
from generic_functions import GenericFunctions


class PianoRecorder(GenericFunctions):
    key = None
    key_time = None
    recording = False
    recording_full_name = None
    paused = False
    paused_time = 0
    current_time = None
    sound = None

    def record(self) -> None:
        self._create_base_sounds()
        while self.recording:
            self._handle_pause()
            self.key_time = 1000 * (time.time() - self.current_time - self.paused_time)
            time.sleep(0.001)
            try:
                self.sound = self.sound.overlay(getattr(self, f'{self.key}_wave', None), position=self.key_time)
                self.key = None
            except (AttributeError, pydub.exceptions.TooManyMissingFrames):
                pass
            self.sound += pydub.AudioSegment.silent(duration=self.key_time + 1000 * (1 - self.sound.duration_seconds))
        try:
            self._save_recording(self.sound)
        except FileNotFoundError:
            pass
        return

    def _create_base_sounds(self) -> None:
        self.sound = pydub.AudioSegment.silent(duration=1000)
        self._create_wave_for_each_key()

    def _create_wave_for_each_key(self) -> None:
        for key in self.key_map:
            setattr(self, f'{key}_wave', pydub.AudioSegment.from_wav(f'{self.keys_path}/{self.key_map[key]}.wav'))

    def _handle_pause(self) -> None:
        pause_loop_iteration = False
        start_time = time.time()
        while self.paused:
            # it's very slow during playing the piano
            # playing piano not allowed when stopped? then it works fine
            if self.key:
                self.key = None
            if not pause_loop_iteration:
                self.current_time += self.paused_time
                pause_loop_iteration = True
            self.paused_time = time.time() - start_time

    def _save_recording(self, sound) -> None:
        sound.export(self.recording_full_name, format='wav')
