import unittest
import customtkinter
import time
import pygame
from mock import MagicMock, call, patch
from recording_manager import RecordingManager


class TestMemoSong(unittest.TestCase):
    mock_tkinter_radiobutton1 = MagicMock()
    mock_tkinter_radiobutton2 = MagicMock()
    customtkinter.CTkRadioButton = MagicMock(side_effect=[mock_tkinter_radiobutton1, mock_tkinter_radiobutton2])
    not_empty_radiobutton_list = [mock_tkinter_radiobutton1, mock_tkinter_radiobutton2]

    def setUp(self) -> None:
        self.recording_manager_cls = RecordingManager()

    @patch.object(RecordingManager, '_display_message_box')
    @patch('pygame.mixer.music')
    @patch.object(RecordingManager, '_remove_selection_from_radiobutton_list')
    @patch.object(RecordingManager, '_get_curselection_from_radiobutton_list', return_value=mock_tkinter_radiobutton1)
    def test_play_recording(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                            mock_remove_selection_from_radiobutton_list: MagicMock, mock_pygame_mixer: MagicMock,
                            mock_display_message_box: MagicMock) -> None:
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=self.not_empty_radiobutton_list)
        self.recording_manager_cls.notes_radiobutton_list = MagicMock()
        self.recording_manager_cls.play_recording()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.recordings_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.notes_radiobutton_list)
        mock_pygame_mixer.load.assert_called_once_with(
            f'{self.recording_manager_cls.app_path}/recordings/{self.mock_tkinter_radiobutton1}')
        mock_pygame_mixer.play.assert_called_once_with()
        mock_display_message_box.assert_not_called()

    @patch.object(RecordingManager, '_display_message_box')
    @patch('pygame.mixer.music')
    @patch.object(RecordingManager, '_remove_selection_from_radiobutton_list')
    @patch.object(RecordingManager, '_get_curselection_from_radiobutton_list', return_value=mock_tkinter_radiobutton1)
    def test_play_recording_error(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                                  mock_remove_selection_from_radiobutton_list: MagicMock, mock_pygame_mixer: MagicMock,
                                  mock_display_message_box: MagicMock) -> None:
        mock_pygame_mixer.load.side_effect = pygame.error
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=self.not_empty_radiobutton_list)
        self.recording_manager_cls.notes_radiobutton_list = MagicMock()
        self.recording_manager_cls.play_recording()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.recordings_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.notes_radiobutton_list)
        mock_pygame_mixer.load.assert_called_once_with(
            f'{self.recording_manager_cls.app_path}/recordings/{self.mock_tkinter_radiobutton1}')
        mock_pygame_mixer.play.assert_not_called()
        mock_display_message_box.assert_called_once_with('ERROR', 'Invalid file!', False, 300)

    @patch.object(RecordingManager, '_start_recording')
    def test_start_piano_recording(self, mock_start_recording: MagicMock) -> None:
        self.recording_manager_cls.start_piano_recording()
        mock_start_recording.assert_called_once_with('piano')

    @patch.object(RecordingManager, '_start_recording')
    def test_start_voice_recording(self, mock_start_recording: MagicMock) -> None:
        self.recording_manager_cls.start_voice_recording()
        mock_start_recording.assert_called_once_with('voice')

    @patch.object(RecordingManager, '_pause_recording')
    def test_pause_piano_recording(self, mock_pause_recording: MagicMock) -> None:
        self.recording_manager_cls.pause_piano_recording()
        mock_pause_recording.assert_called_once_with('piano')

    @patch.object(RecordingManager, '_pause_recording')
    def test_pause_voice_recording(self, mock_pause_recording: MagicMock) -> None:
        self.recording_manager_cls.pause_voice_recording()
        mock_pause_recording.assert_called_once_with('voice')

    @patch.object(RecordingManager, '_stop_recording')
    def test_stop_piano_recording(self, mock_stop_recording: MagicMock) -> None:
        self.recording_manager_cls.stop_piano_recording()
        mock_stop_recording.assert_called_once_with('piano')

    @patch.object(RecordingManager, '_stop_recording')
    def test_stop_voice_recording(self, mock_stop_recording: MagicMock) -> None:
        self.recording_manager_cls.stop_voice_recording()
        mock_stop_recording.assert_called_once_with('voice')

    @patch.object(RecordingManager, 'update_list')
    @patch('os.remove')
    @patch.object(RecordingManager, '_mute_playback')
    @patch.object(RecordingManager, '_setup_recorder')
    @patch.object(RecordingManager, '_display_message_box')
    @patch('os.listdir', return_value=['title'])
    @patch.object(RecordingManager, '_get_recording_title', return_value='title')
    @patch.object(RecordingManager, '_highlight_used_function')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_start_recording(self, mock_get_recorder: MagicMock, mock_highlight_used_function: MagicMock,
                             mock_get_recording_title: MagicMock, mock_os_listdir: MagicMock,
                             mock_display_message_box: MagicMock, mock_mute_playback: MagicMock,
                             mock_setup_recorder: MagicMock, mock_os_remove: MagicMock,
                             mock_update_list: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls.piano_recorder.paused = False
        mock_display_message_box.get.return_value = 'No'
        self.recording_manager_cls._start_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_highlight_used_function.assert_has_calls([call('pause_piano_recording', 'off'),
                                                       call('start_piano_recording', 'on')])
        mock_get_recording_title.assert_called_once_with('piano')
        mock_os_listdir.assert_called_once_with(f'{self.recording_manager_cls.app_path}/recordings')
        mock_display_message_box.assert_has_calls([call('OVERWRITE FILE', 'The file\ntitle already exists. Overwrite?',
                                                        True), call().get(), call().get().__eq__('Yes')])
        # mock_mute_playback.assert_called_once_with()
        # mock_setup_recorder.assert_called_once_with()
        # mock_os_remove.assert_called_once_with()
        # mock_update_list.assert_called_once_with()

    @patch.object(RecordingManager, '_setup_recorder')
    @patch.object(RecordingManager, 'update_list')
    @patch('os.remove')
    @patch.object(RecordingManager, '_mute_playback')
    @patch.object(RecordingManager, '_display_message_box')
    @patch('os.listdir')
    @patch.object(RecordingManager, '_get_recording_title', return_value='title')
    @patch.object(RecordingManager, '_highlight_used_function')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_start_recording_empty_dir(self, mock_get_recorder: MagicMock, mock_highlight_used_function: MagicMock,
                                       mock_get_recording_title: MagicMock, mock_os_listdir: MagicMock,
                                       mock_display_message_box: MagicMock, mock_mute_playback: MagicMock,
                                       mock_os_remove: MagicMock, mock_update_list: MagicMock,
                                       mock_setup_recorder: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls.piano_recorder.paused = False
        self.recording_manager_cls._start_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_highlight_used_function.assert_has_calls([call('pause_piano_recording', 'off'),
                                                       call('start_piano_recording', 'on')])
        mock_get_recording_title.assert_called_once_with('piano')
        mock_os_listdir.assert_called_once_with(f'{self.recording_manager_cls.app_path}/recordings')
        mock_display_message_box.assert_not_called()
        mock_display_message_box.get.assert_not_called()
        mock_mute_playback.assert_not_called()
        mock_os_remove.assert_not_called()
        mock_update_list.assert_not_called()
        mock_setup_recorder.assert_called_once_with(self.recording_manager_cls.piano_recorder, 'piano', 'title')

    @patch.object(RecordingManager, '_get_filename', return_value='title')
    def test_get_recording_title(self, mock_get_filename: MagicMock) -> None:
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        title = self.recording_manager_cls._get_recording_title('piano')
        mock_get_filename.assert_called_once_with(mock_tkinter_entry.get(), 'recordings', 'piano_')
        self.assertEqual(title, 'title')

    @patch('time.time', return_value=1694415648.8349693)
    @patch.object(RecordingManager, '_start_new_thread')
    def test_setup_recorder(self, mock_start_new_thread: MagicMock, mock_time: MagicMock) -> None:
        recorder = self.recording_manager_cls.piano_recorder
        self.recording_manager_cls._setup_recorder(recorder, 'piano', 'title')
        self.assertEqual(getattr(self.recording_manager_cls, 'piano_recording_title'), 'title')
        self.assertEqual(recorder.recording, True)
        self.assertEqual(recorder.recording_full_name, f'{self.recording_manager_cls.app_path}/recordings/title')
        self.assertEqual(recorder.current_time, mock_time())
        mock_start_new_thread.assert_called_once_with(recorder.record)

    def test_update_piano_recorder_key_recording(self) -> None:
        self.recording_manager_cls.piano_recorder.recording = True
        self.recording_manager_cls.update_piano_recorder_key('q')
        self.assertEqual(self.recording_manager_cls.piano_recorder.key, 'q')

    def test_update_piano_recorder_key_not_recording(self) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls.update_piano_recorder_key('q')
        self.assertEqual(self.recording_manager_cls.piano_recorder.key, None)

    @patch.object(RecordingManager, '_setup_pause')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_pause_recording_on(self, mock_get_recorder: MagicMock, mock_setup_pause: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.paused = False
        self.recording_manager_cls._pause_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_setup_pause.assert_called_once_with(self.recording_manager_cls.piano_recorder, 'piano', 'on')

    @patch.object(RecordingManager, '_setup_pause')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_pause_recording_off(self, mock_get_recorder: MagicMock, mock_setup_pause: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.paused = True
        self.recording_manager_cls._pause_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_setup_pause.assert_called_once_with(self.recording_manager_cls.piano_recorder, 'piano', 'off')

    @patch.object(RecordingManager, '_highlight_used_function')
    def test_setup_pause_on(self, mock_highlight_used_function: MagicMock) -> None:
        self.recording_manager_cls._setup_pause(self.recording_manager_cls.piano_recorder, 'piano', 'on')
        mock_highlight_used_function.assert_called_once_with('pause_piano_recording', 'on')
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, True)

    @patch.object(RecordingManager, '_highlight_used_function')
    def test_setup_pause_off(self, mock_highlight_used_function: MagicMock) -> None:
        self.recording_manager_cls._setup_pause(self.recording_manager_cls.piano_recorder, 'piano', 'off')
        mock_highlight_used_function.assert_called_once_with('pause_piano_recording', 'off')
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, False)

    @patch.object(RecordingManager, '_highlight_used_function')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_stop_recording(self, mock_get_recorder: MagicMock, mock_highlight_used_function: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = True
        self.recording_manager_cls.piano_recorder.paused = False
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=self.not_empty_radiobutton_list)
        self.recording_manager_cls.recordings_radiobutton_list.add_item = MagicMock()
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        self.recording_manager_cls.piano_recording_title = 'title'
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        self.recording_manager_cls._stop_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_highlight_used_function.assert_has_calls([call('pause_piano_recording', 'off'),
                                                       call('start_piano_recording', 'off')])
        self.recording_manager_cls.recordings_radiobutton_list.add_item.assert_called_once_with('title')
        mock_tkinter_entry.delete.assert_called_once_with(0, 'end')
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, False)

    @patch.object(RecordingManager, '_highlight_used_function')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_stop_recording_paused(self, mock_get_recorder: MagicMock,
                                   mock_highlight_used_function: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = True
        self.recording_manager_cls.piano_recorder.paused = False
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=self.not_empty_radiobutton_list)
        self.recording_manager_cls.recordings_radiobutton_list.add_item = MagicMock()
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        self.recording_manager_cls.piano_recording_title = 'title'
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        self.recording_manager_cls._stop_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_highlight_used_function.assert_has_calls([call('pause_piano_recording', 'off'),
                                                       call('start_piano_recording', 'off')])
        self.recording_manager_cls.recordings_radiobutton_list.add_item.assert_called_once_with('title')
        mock_tkinter_entry.delete.assert_called_once_with(0, 'end')
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, False)

    @patch.object(RecordingManager, '_highlight_used_function')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_stop_recording_stopped(self, mock_get_recorder: MagicMock,
                                    mock_highlight_used_function: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls.piano_recorder.paused = False
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=self.not_empty_radiobutton_list)
        self.recording_manager_cls.recordings_radiobutton_list.add_item = MagicMock()
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        self.recording_manager_cls.piano_recording_title = 'title'
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        self.recording_manager_cls._stop_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_highlight_used_function.assert_not_called()
        self.recording_manager_cls.recordings_radiobutton_list.add_item.assert_not_called()
        mock_tkinter_entry.delete.assert_not_called()
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, False)

    @patch.object(RecordingManager, '_highlight_used_function')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_stop_recording_stopped_paused(self, mock_get_recorder: MagicMock,
                                           mock_highlight_used_function: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls.piano_recorder.paused = True
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=self.not_empty_radiobutton_list)
        self.recording_manager_cls.recordings_radiobutton_list.add_item = MagicMock()
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        self.recording_manager_cls.piano_recording_title = 'title'
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        self.recording_manager_cls._stop_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_highlight_used_function.assert_not_called()
        self.recording_manager_cls.recordings_radiobutton_list.add_item.assert_not_called()
        mock_tkinter_entry.delete.assert_not_called()
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, True)

    def test_get_recorder_piano(self) -> None:
        recorder_name = self.recording_manager_cls._get_recorder('piano')
        self.assertEqual(recorder_name, self.recording_manager_cls.piano_recorder)

    def test_get_recorder_voice(self) -> None:
        recorder_name = self.recording_manager_cls._get_recorder('voice')
        self.assertEqual(recorder_name, self.recording_manager_cls.voice_recorder)
