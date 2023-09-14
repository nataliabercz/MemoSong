import unittest
import pygame
from mock import MagicMock, patch
from piano import Piano


class TestMemoSong(unittest.TestCase):
    def setUp(self) -> None:
        self.piano_cls = Piano()

    @patch.object(Piano, '_remove_button_highlight')
    @patch('time.sleep')
    @patch('piano.Piano.recording_manager.update_piano_recorder_key')
    @patch('pygame.mixer.Sound')
    def test_play_key(self, mock_pygame_mixer: MagicMock, mock_update_piano_recorder_key: MagicMock,
                      mock_time_sleep: MagicMock, mock_remove_button_highlight: MagicMock) -> None:
        self.piano_cls.key = 'q'
        self.piano_cls.play_key()
        mock_pygame_mixer.assert_called_once_with(f'{self.piano_cls.keys_path}/c3.wav')
        mock_pygame_mixer.play.assert_called_once_with(pygame.mixer.Sound(f'{self.piano_cls.keys_path}/c3.wav'))
        mock_update_piano_recorder_key.assert_called_once_with('q')
        mock_time_sleep.assert_called_once_with(0.1)
        mock_remove_button_highlight.assert_called_once_with('q')
