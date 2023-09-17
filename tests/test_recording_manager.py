import unittest
import pygame
from mock import patch
from recording_manager import RecordingManager
from test_memo_song_data import *


class TestRecordingManager(unittest.TestCase):
    def setUp(self) -> None:
        self.recording_manager_cls = RecordingManager()
        self.recorder = self.recording_manager_cls.piano_recorder

    @patch.object(RecordingManager, '_display_message_box')
    @patch('pygame.mixer.music')
    @patch.object(RecordingManager, '_remove_selection_from_radiobutton_list')
    @patch.object(RecordingManager, '_get_curselection_from_radiobutton_list', return_value=mock_tkinter_radiobutton_1)
    def test_play_recording(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                            mock_remove_selection_from_radiobutton_list: MagicMock, mock_pygame_mixer: MagicMock,
                            mock_display_message_box: MagicMock) -> None:
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=not_empty_radiobutton_list)
        self.recording_manager_cls.notes_radiobutton_list = MagicMock()
        self.recording_manager_cls.play_recording()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.recordings_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.notes_radiobutton_list)
        mock_pygame_mixer.load.assert_called_once_with(
            f'{self.recording_manager_cls.app_path}/recordings/{mock_tkinter_radiobutton_1}')
        mock_pygame_mixer.play.assert_called_once_with()
        mock_display_message_box.assert_not_called()

    @patch.object(RecordingManager, '_display_message_box')
    @patch('pygame.mixer.music')
    @patch.object(RecordingManager, '_remove_selection_from_radiobutton_list')
    @patch.object(RecordingManager, '_get_curselection_from_radiobutton_list', return_value=mock_tkinter_radiobutton_1)
    def test_play_recording_error(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                                  mock_remove_selection_from_radiobutton_list: MagicMock, mock_pygame_mixer: MagicMock,
                                  mock_display_message_box: MagicMock) -> None:
        mock_pygame_mixer.load.side_effect = pygame.error
        self.recording_manager_cls.recordings_radiobutton_list = MagicMock(return_value=not_empty_radiobutton_list)
        self.recording_manager_cls.notes_radiobutton_list = MagicMock()
        self.recording_manager_cls.play_recording()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.recordings_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.recording_manager_cls.notes_radiobutton_list)
        mock_pygame_mixer.load.assert_called_once_with(
            f'{self.recording_manager_cls.app_path}/recordings/{mock_tkinter_radiobutton_1}')
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

    @patch.object(RecordingManager, '_start_recorder')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_start_recording(self, mock_get_recorder: MagicMock, mock_start_recorder: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls._start_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_start_recorder.assert_called_once_with(self.recording_manager_cls.piano_recorder, 'piano')

    @patch.object(RecordingManager, '_start_recorder')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_start_recording_started(self, mock_get_recorder: MagicMock, mock_start_recorder: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = True
        self.recording_manager_cls._start_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_start_recorder.assert_not_called()

    @patch.object(RecordingManager, '_setup_recorder')
    @patch.object(RecordingManager, '_check_whether_to_overwrite')
    @patch.object(RecordingManager, '_list_files', return_value=[])
    @patch.object(RecordingManager, '_get_recording_title', return_value='title')
    @patch.object(RecordingManager, '_modify_buttons_highlight')
    def test_start_recorder(self, mock_modify_buttons_highlight: MagicMock, mock_get_recording_title: MagicMock,
                            mock_list_files: MagicMock, mock_check_whether_to_overwrite: MagicMock,
                            mock_setup_recorder: MagicMock) -> None:
        self.recording_manager_cls._start_recorder(self.recorder, 'piano')
        mock_modify_buttons_highlight.assert_called_once_with('piano', 'on')
        mock_get_recording_title.assert_called_once_with('piano')
        mock_list_files.assert_called_once_with(f'{self.recording_manager_cls.app_path}/recordings')
        mock_check_whether_to_overwrite.assert_not_called()
        mock_setup_recorder.assert_called_once_with(self.recorder, 'piano', 'title')
        self.assertEqual(self.recorder.paused, False)

    @patch.object(RecordingManager, '_setup_recorder')
    @patch.object(RecordingManager, '_check_whether_to_overwrite')
    @patch.object(RecordingManager, '_list_files', return_value=['title'])
    @patch.object(RecordingManager, '_get_recording_title', return_value='title')
    @patch.object(RecordingManager, '_modify_buttons_highlight')
    def test_start_recorder_overwrite(self, mock_modify_buttons_highlight: MagicMock,
                                      mock_get_recording_title: MagicMock, mock_list_files: MagicMock,
                                      mock_check_whether_to_overwrite: MagicMock,
                                      mock_setup_recorder: MagicMock) -> None:
        self.recording_manager_cls._start_recorder(self.recorder, 'piano')
        mock_modify_buttons_highlight.assert_called_once_with('piano', 'on')
        mock_get_recording_title.assert_called_once_with('piano')
        mock_list_files.assert_called_once_with(f'{self.recording_manager_cls.app_path}/recordings')
        mock_check_whether_to_overwrite.assert_called_once_with(self.recorder, 'piano', 'title')
        mock_setup_recorder.assert_not_called()
        self.assertEqual(self.recorder.paused, False)

    @patch.object(RecordingManager, '_highlight_button')
    @patch.object(RecordingManager, '_setup_recorder_and_overwrite')
    @patch.object(RecordingManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    def test_check_whether_to_overwrite_yes(self, mock_display_message_box: MagicMock,
                                            mock_setup_recorder_and_overwrite: MagicMock,
                                            mock_highlight_button: MagicMock) -> None:
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.recording_manager_cls._check_whether_to_overwrite(self.recorder, 'piano', 'title')
        mock_display_message_box.assert_called_once_with('OVERWRITE FILE', 'The file\ntitle already exists. Overwrite?',
                                                         True)
        mock_setup_recorder_and_overwrite.assert_called_once_with(self.recorder, 'piano', 'title')
        mock_highlight_button.assert_not_called()

    @patch.object(RecordingManager, '_highlight_button')
    @patch.object(RecordingManager, '_setup_recorder_and_overwrite')
    @patch.object(RecordingManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    def test_check_whether_to_overwrite_no(self, mock_display_message_box: MagicMock,
                                           mock_setup_recorder_and_overwrite: MagicMock,
                                           mock_highlight_button: MagicMock) -> None:
        mock_tkinter_messagebox.get.return_value = 'No'
        self.recording_manager_cls._check_whether_to_overwrite(self.recorder, 'piano', 'title')
        mock_display_message_box.assert_called_once_with('OVERWRITE FILE', 'The file\ntitle already exists. Overwrite?',
                                                         True)
        mock_setup_recorder_and_overwrite.assert_not_called()
        mock_highlight_button.assert_called_once_with('start_piano_recording', 'off')

    @patch.object(RecordingManager, 'update_list')
    @patch.object(RecordingManager, '_remove_file')
    @patch.object(RecordingManager, '_setup_recorder')
    @patch.object(RecordingManager, '_mute_playback')
    def test_setup_recorder_and_overwrite(self, mock_mute_playback: MagicMock, mock_setup_recorder: MagicMock,
                                          mock_remove_file: MagicMock, mock_update_list: MagicMock) -> None:
        self.recording_manager_cls._setup_recorder_and_overwrite(self.recorder, 'piano', 'title')
        mock_mute_playback.assert_called_once_with()
        mock_setup_recorder.assert_called_once_with(self.recorder, 'piano', 'title')
        mock_remove_file.assert_called_once_with('title')
        mock_update_list.assert_called_once_with('recordings')

    @patch.object(RecordingManager, '_start_new_thread')
    @patch('time.time', return_value=1694415648.8349693)
    @patch.object(RecordingManager, '_get_title_field', return_value=mock_tkinter_entry)
    def test_setup_recorder(self, mock_get_title_field: MagicMock, mock_time: MagicMock,
                            mock_start_new_thread: MagicMock) -> None:
        mock_tkinter_entry.reset_mock()
        self.recording_manager_cls._setup_recorder(self.recorder, 'piano', 'title')
        mock_get_title_field.assert_called_once_with('piano')
        mock_tkinter_entry.configure.assert_called_once_with(state='disabled')
        mock_time.assert_called_once_with()
        mock_start_new_thread.assert_called_once_with(self.recorder.record)
        self.assertEqual(getattr(self.recording_manager_cls, 'piano_recording_title'), 'title')
        self.assertEqual(self.recorder.recording, True)
        self.assertEqual(self.recorder.recording_full_name, f'{self.recording_manager_cls.app_path}/recordings/title')
        self.assertEqual(self.recorder.current_time, mock_time())

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

    @patch.object(RecordingManager, '_highlight_button')
    def test_setup_pause_on(self, mock_highlight_button: MagicMock) -> None:
        self.recording_manager_cls._setup_pause(self.recording_manager_cls.piano_recorder, 'piano', 'on')
        mock_highlight_button.assert_called_once_with('pause_piano_recording', 'on')
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, True)

    @patch.object(RecordingManager, '_highlight_button')
    def test_setup_pause_off(self, mock_highlight_button: MagicMock) -> None:
        self.recording_manager_cls._setup_pause(self.recording_manager_cls.piano_recorder, 'piano', 'off')
        mock_highlight_button.assert_called_once_with('pause_piano_recording', 'off')
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, False)

    @patch.object(RecordingManager, '_stop_recorder')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_stop_recording(self, mock_get_recorder: MagicMock, mock_stop_recorder: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = True
        self.recording_manager_cls._stop_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_stop_recorder.assert_called_once_with(self.recording_manager_cls.piano_recorder, 'piano')

    @patch.object(RecordingManager, '_stop_recorder')
    @patch.object(RecordingManager, '_get_recorder', return_value=RecordingManager.piano_recorder)
    def test_stop_recording_stopped(self, mock_get_recorder: MagicMock, mock_stop_recorder: MagicMock) -> None:
        self.recording_manager_cls.piano_recorder.recording = False
        self.recording_manager_cls._stop_recording('piano')
        mock_get_recorder.assert_called_once_with('piano')
        mock_stop_recorder.assert_not_called()

    @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.recordings_radiobutton_list')
    @patch.object(RecordingManager, '_get_recording_title')
    @patch.object(RecordingManager, '_modify_title_field')
    @patch.object(RecordingManager, '_modify_buttons_highlight')
    def test_stop_recorder(self, mock_modify_buttons_highlight: MagicMock, mock_modify_title_field: MagicMock,
                           mock_get_recording_title: MagicMock, mock_recordings_radiobutton_list: MagicMock) -> None:
        mock_recordings_radiobutton_list.add_item = MagicMock()
        self.recording_manager_cls.recordings_radiobutton_list = mock_recordings_radiobutton_list
        self.recording_manager_cls._stop_recorder(self.recording_manager_cls.piano_recorder, 'piano')
        mock_modify_buttons_highlight.assert_called_once_with('piano', 'off')
        mock_modify_title_field.assert_called_once_with('piano')
        mock_recordings_radiobutton_list.add_item.assert_called_once_with(mock_get_recording_title('piano'))
        self.assertEqual(self.recording_manager_cls.piano_recorder.paused, False)
        self.assertEqual(self.recording_manager_cls.piano_recorder.recording, False)

    @patch.object(RecordingManager, '_get_title_field', return_value=mock_tkinter_entry)
    def test_modify_title_field(self, mock_get_title_field: MagicMock) -> None:
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        self.recording_manager_cls._modify_title_field('piano')
        mock_get_title_field.assert_called_once_with('piano')
        mock_tkinter_entry.configure.assert_called_once_with(state='normal')
        mock_tkinter_entry.delete.assert_called_once_with(0, tkinter.END)

    @patch.object(RecordingManager, '_get_full_filename', return_value='title')
    def test_get_recording_title(self, mock_get_filename: MagicMock) -> None:
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        title = self.recording_manager_cls._get_recording_title('piano')
        mock_get_filename.assert_called_once_with(mock_tkinter_entry.get(), 'recordings', 'piano_')
        self.assertEqual(title, 'title')

    def test_get_title_field(self) -> None:
        self.recording_manager_cls.piano_recording_title_field = mock_tkinter_entry
        title_field = self.recording_manager_cls._get_title_field('piano')
        self.assertEqual(title_field, self.recording_manager_cls.piano_recording_title_field)

    def test_get_recorder_piano(self) -> None:
        recorder_name = self.recording_manager_cls._get_recorder('piano')
        self.assertEqual(recorder_name, self.recording_manager_cls.piano_recorder)

    def test_get_recorder_voice(self) -> None:
        recorder_name = self.recording_manager_cls._get_recorder('voice')
        self.assertEqual(recorder_name, self.recording_manager_cls.voice_recorder)

    @patch.object(RecordingManager, '_highlight_button')
    def test_modify_buttons_highlight_start_on(self, mock_highlight_button: MagicMock) -> None:
        self.recording_manager_cls._modify_buttons_highlight('piano', 'on')
        mock_highlight_button.assert_has_calls([call('pause_piano_recording', 'off'),
                                                call('start_piano_recording', 'on')
                                                ])

    @patch.object(RecordingManager, '_highlight_button')
    def test_modify_buttons_highlight_start_off(self, mock_highlight_button: MagicMock) -> None:
        self.recording_manager_cls._modify_buttons_highlight('piano', 'off')
        mock_highlight_button.assert_has_calls([call('pause_piano_recording', 'off'),
                                                call('start_piano_recording', 'off')
                                                ])
