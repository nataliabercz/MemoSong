import time
import pydub
from generic_functions import GenericFunctions


class PianoRecorder(GenericFunctions):
    key = None
    key_time = None
    recording = False
    recording_full_name = None
    current_time = None
    paused = False
    is_first_iteration = True
    _paused_time = 0
    _sound = None

    def record(self) -> None:
        self._create_base_sounds()
        self._loop_recording()
        try:
            self._save_recording(self._sound)
        except FileNotFoundError:
            pass
        return  # is it necessary ??

    def _create_base_sounds(self) -> None:
        self._sound = self._generate_silence(1000)
        self._create_wave_for_each_key()

    @staticmethod
    def _generate_silence(duration: int) -> pydub.AudioSegment:
        return pydub.AudioSegment.silent(duration=duration)

    def _create_wave_for_each_key(self) -> None:
        for key in self.key_map:
            setattr(self, f'{key}_wave', pydub.AudioSegment.from_wav(f'{self.keys_path}/{self.key_map[key]}.wav'))

    def _loop_recording(self) -> None:
        while self.recording:
            self._create_recording()

    def _create_recording(self) -> None:
        self._handle_pause()
        self.key_time = 1000 * (time.time() - self.current_time - self._paused_time)
        time.sleep(0.001)
        try:
            self._sound = self._sound.overlay(getattr(self, f'{self.key}_wave'), position=self.key_time)
            self.key = None
        except AttributeError:
            pass
        self._sound += self._generate_silence(self.key_time + 1000 * (1 - self._sound.duration_seconds))

    def _handle_pause(self) -> None:
        self.is_first_iteration = True
        start_time = time.time()
        self._loop_pause(start_time)

    def _loop_pause(self, start_time: float) -> None:
        while self.paused:
            self._set_paused_time(start_time)
            # it's very slow during playing the piano
            # playing piano not allowed when stopped? then it works fine

    def _set_paused_time(self, start_time: float) -> None:
        if self.key:
            self.key = None
        if self.is_first_iteration:
            self.current_time += self._paused_time
            self.is_first_iteration = False
        self._paused_time = time.time() - start_time

    def _save_recording(self, sound) -> None:
        sound.export(self.recording_full_name, format='wav')
