import unittest
import wave
from mock import patch
from voice_recorder import VoiceRecorder
from test_memo_song_data import *


class TestVoiceRecorder(unittest.TestCase):
    def setUp(self) -> None:
        self.voice_recorder_cls = VoiceRecorder()

    @patch.object(VoiceRecorder, '_stop_recording')
    @patch.object(VoiceRecorder, '_loop_recording')
    @patch.object(VoiceRecorder, '_prepare_audio')
    def test_record(self, mock_prepare_audio: MagicMock, mock_loop_recording: MagicMock,
                    mock_stop_recording: MagicMock) -> None:
        self.voice_recorder_cls.recording = True
        self.voice_recorder_cls.record()
        mock_prepare_audio.assert_called_once_with()
        mock_loop_recording.assert_called_once_with()
        mock_stop_recording.assert_called_once_with()

    @patch.object(VoiceRecorder, '_stream', side_effect=mock_pyaudio_stream)
    def test_append_recorded_data(self, mock_stream: MagicMock) -> None:
        mock_stream.read.return_value = stream_read_data
        self.voice_recorder_cls._frames = []
        self.voice_recorder_cls._append_recorded_data()
        mock_stream.read.assert_called_once_with(1024)
        self.assertEqual(self.voice_recorder_cls._frames, [stream_read_data])

    @patch.object(VoiceRecorder, '_audio', side_effect=mock_pyaudio_audio)
    def test_prepare_audio(self, _: MagicMock) -> None:
        self.voice_recorder_cls._prepare_audio()
        mock_pyaudio_audio.open.assert_called_once_with(format=8, channels=1, rate=44100,
                                                        frames_per_buffer=1024, input=True)
        self.assertEqual(self.voice_recorder_cls._stream, mock_pyaudio_audio.open())

    @patch.object(VoiceRecorder, '_save_recording')
    @patch.object(VoiceRecorder, '_stream', side_effect=mock_pyaudio_stream)
    @patch.object(VoiceRecorder, '_audio', side_effect=mock_pyaudio_audio)
    @patch('time.sleep')
    def test_stop_recording(self, mock_time_sleep: MagicMock, mock_audio: MagicMock, mock_stream: MagicMock,
                            mock_save_recording: MagicMock) -> None:
        self.voice_recorder_cls._stop_recording()
        mock_time_sleep.assert_called_once_with(0.1)
        mock_stream.stop_stream.assert_called_once_with()
        mock_audio.terminate.assert_called_once_with()
        mock_save_recording.assert_called_once_with()

    @patch.object(VoiceRecorder, '_audio', side_effect=mock_pyaudio_audio)
    def test_save_recording(self, mock_audio: MagicMock) -> None:
        mock_audio.get_sample_size.return_value = 2
        file = wave.Wave_write(self.voice_recorder_cls.recording_full_name)
        file.setnchannels = MagicMock()
        file.setsampwidth = MagicMock()
        file.setframerate = MagicMock()
        file.writeframes = MagicMock()
        file.close = MagicMock()
        with patch('wave.open', return_value=file, create=True) as mock_wave_open:
            self.voice_recorder_cls._save_recording()
            mock_wave_open.assert_called_once_with(self.voice_recorder_cls.recording_full_name, 'wb')
            file.setnchannels.assert_called_once_with(1)
            file.setsampwidth.assert_called_once_with(2)
            mock_audio.get_sample_size.assert_called_once_with(8)
            file.setframerate.assert_called_once_with(44100)
            file.writeframes.assert_called_once_with(b'')
            file.close.assert_called_once_with()
