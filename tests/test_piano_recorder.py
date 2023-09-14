import unittest
from mock import patch
from piano_recorder import PianoRecorder
from test_memo_song_data import *


class TestMemoSong(unittest.TestCase):
    def setUp(self) -> None:
        self.piano_recorder_cls = PianoRecorder()
        self.piano_recorder_cls._sound = mock_sound

    @patch.object(PianoRecorder, '_save_recording')
    @patch.object(PianoRecorder, '_loop_recording')
    @patch.object(PianoRecorder, '_create_base_sounds')
    def test_record(self, mock_create_base_sounds: MagicMock, mock_loop_recording: MagicMock,
                    mock_save_recording: MagicMock) -> None:
        self.piano_recorder_cls.record()
        mock_create_base_sounds.assert_called_once_with()
        mock_loop_recording.assert_called_once_with()
        mock_save_recording.assert_called_once_with(self.piano_recorder_cls._sound)

    @patch.object(PianoRecorder, '_save_recording', side_effect=FileNotFoundError)
    @patch.object(PianoRecorder, '_loop_recording')
    @patch.object(PianoRecorder, '_create_base_sounds')
    def test_record_error(self, mock_create_base_sounds: MagicMock, mock_loop_recording: MagicMock,
                          mock_save_recording: MagicMock) -> None:
        self.piano_recorder_cls.record()
        mock_create_base_sounds.assert_called_once_with()
        mock_loop_recording.assert_called_once_with()
        mock_save_recording.assert_called_once_with(self.piano_recorder_cls._sound)

    @patch.object(PianoRecorder, '_generate_silence')
    @patch.object(PianoRecorder, '_create_wave_for_each_key')
    def test_create_base_sounds(self, mock_create_wave_for_each_key: MagicMock,
                                mock_generate_silence: MagicMock) -> None:
        self.piano_recorder_cls._create_base_sounds()
        mock_create_wave_for_each_key.assert_called_once_with()
        mock_generate_silence.assert_called_once_with(1000)
        self.assertEqual(self.piano_recorder_cls._sound, mock_generate_silence(1000))

    @patch('pydub.AudioSegment.silent')
    def test_generate_silence(self, mock_pydub: MagicMock) -> None:
        silence = self.piano_recorder_cls._generate_silence(1000)
        mock_pydub.assert_called_once_with(duration=1000)
        self.assertEqual(silence, mock_pydub(duration=1000))

    @patch('pydub.AudioSegment')
    def test_create_wave_for_each_key(self, mock_pydub: MagicMock) -> None:
        self.piano_recorder_cls._create_wave_for_each_key()
        mock_pydub.from_wav.assert_has_calls(calls_pydub_from_wav)
        self.assertEqual(getattr(self.piano_recorder_cls, 'q_wave'), mock_pydub.from_wav())

    # @patch.object(PianoRecorder, '_generate_silence')
    # @patch('time.sleep')
    # @patch('time.time', return_value=1694415648.8349693)
    # @patch.object(PianoRecorder, '_handle_pause')
    # def test_create_recording(self, mock_handle_pause: MagicMock, mock_time: MagicMock,
    #                           mock_time_sleep: MagicMock, mock_generate_silence: MagicMock) -> None:
    #     self.piano_recorder_cls.key = 'q'
    #     self.piano_recorder_cls.q_key = MagicMock()
    #     self.piano_recorder_cls.current_time = 1694415638.8349693
    #     self.piano_recorder_cls._paused_time = 0
    #     self.piano_recorder_cls._create_recording()
    #     mock_handle_pause.assert_called_once_with()
    #     mock_time.assert_called_once_with()
    #     mock_time_sleep.assert_called_once_with(0.001)
    #     mock_sound.overlay.assert_called_once_with(self.piano_recorder_cls.q_key, position=10000.0)
    #     mock_generate_silence.assert_called_once_with(10000.0 + 1000 * (1 - mock_sound.overlay().duration_seconds))
    #     self.assertEqual(self.piano_recorder_cls.key_time, 10000.0)
    #     self.assertAlmostEquals(self.piano_recorder_cls.key, None)
    #
    # @patch.object(PianoRecorder, '_generate_silence')
    # @patch('time.sleep')
    # @patch('time.time', return_value=1694415648.8349693)
    # @patch.object(PianoRecorder, '_handle_pause')
    # def test_create_recording_error(self, mock_handle_pause: MagicMock, mock_time: MagicMock,
    #                                 mock_time_sleep: MagicMock, mock_generate_silence: MagicMock) -> None:
    #     self.piano_recorder_cls.current_time = 1694415638.8349693
    #     self.piano_recorder_cls._paused_time = 0
    #     mock_sound.overlay = MagicMock(side_effect=AttributeError)
    #     self.piano_recorder_cls._create_recording()
    #     mock_handle_pause.assert_called_once_with()
    #     mock_time.assert_called_once_with()
    #     mock_time_sleep.assert_called_once_with(0.001)
    #     mock_sound.overlay.assert_called_once_with(getattr(self, f'{self.piano_recorder_cls.key}_wave', None),
    #                                                position=10000.0)
    #     mock_generate_silence.assert_called_once_with(10000.0 + 1000 * (1 - mock_sound.overlay().duration_seconds))
    #     self.assertEqual(self.piano_recorder_cls.key_time, 10000.0)
    #     self.assertAlmostEquals(self.piano_recorder_cls.key, None)

    @patch.object(PianoRecorder, '_loop_pause')
    @patch('time.time', return_value=1694415648.8349693)
    def test_handle_pause(self, mock_time: MagicMock, mock_loop_pause: MagicMock) -> None:
        self.piano_recorder_cls._handle_pause()
        mock_time.assert_called_once_with()
        mock_loop_pause.assert_called_once_with(1694415648.8349693)

    @patch('time.time', return_value=1694415658.8349693)
    def test_set_paused_time(self, mock_time: MagicMock) -> None:
        self.piano_recorder_cls.current_time = 1694415628.8349693
        self.piano_recorder_cls._set_paused_time(1694415648.8349693)
        mock_time.assert_called_once_with()
        self.assertEqual(self.piano_recorder_cls.key, None)
        self.assertEqual(self.piano_recorder_cls.is_first_iteration, False)
        self.assertEqual(self.piano_recorder_cls._paused_time, 10.0)

    def test_save_recording(self) -> None:
        self.piano_recorder_cls._save_recording(mock_sound)
        mock_sound.export.assert_called_once_with(self.piano_recorder_cls.recording_full_name, format='wav')
