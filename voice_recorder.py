import time
import wave
import pyaudio


class VoiceRecorder:
    recording = False
    recording_full_name = None
    paused = False
    _channels = 1
    _chunk = 1024
    _sample_rate = 44100
    _sample_format = pyaudio.paInt16
    _audio = None
    _stream = None
    _frames = []

    def record(self):
        self._frames = []
        self._prepare_audio()
        while self.recording:
            while self.paused:
                # it's very slow
                pass
            data = self._stream.read(self._chunk)
            self._frames.append(data)
        self._stop_recording()

    def _prepare_audio(self) -> None:
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(format=self._sample_format, channels=self._channels, rate=self._sample_rate,
                                        frames_per_buffer=self._chunk, input=True)

    def _stop_recording(self) -> None:
        time.sleep(0.1)
        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()
        self._save_recording()

    def _save_recording(self) -> None:
        file = wave.open(self.recording_full_name, 'wb')
        file.setnchannels(self._channels)
        file.setsampwidth(self._audio.get_sample_size(self._sample_format))
        file.setframerate(self._sample_rate)
        file.writeframes(b''.join(self._frames))
        file.close()
