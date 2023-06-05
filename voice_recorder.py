import time
import wave
import pyaudio


class VoiceRecorder:
    frames = []
    channels = 1
    chunk = 1024
    sample_rate = 44100
    sample_format = pyaudio.paInt16
    audio = None
    stream = None
    recording_full_name = None
    recording = False
    paused = False

    def record(self):
        self.frames = []
        self._prepare_audio()
        while self.recording:
            while self.paused:
                # it's very slow
                pass
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        self._stop_recording()

    def _prepare_audio(self) -> None:
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.sample_format, channels=self.channels, rate=self.sample_rate,
                                      frames_per_buffer=self.chunk, input=True)

    def _stop_recording(self) -> None:
        time.sleep(0.1)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self._save_recording()

    def _save_recording(self) -> None:
        file = wave.open(self.recording_full_name, 'wb')
        file.setnchannels(self.channels)
        file.setsampwidth(self.audio.get_sample_size(self.sample_format))
        file.setframerate(self.sample_rate)
        file.writeframes(b''.join(self.frames))
        file.close()
