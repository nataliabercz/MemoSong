import unittest
from mock import patch
from memo_song import MemoSong
from test_memo_song_data import *


class TestMemoSong(unittest.TestCase):
    def setUp(self) -> None:
        self.root = customtkinter.CTk()
        self.memo_song_cls = MemoSong(self.root)
        self.memo_song_cls.root = MagicMock()

    def tearDown(self) -> None:
        if self.root:
            self.root.destroy()

    @patch.object(MemoSong, 'prepare_layout')
    @patch.object(MemoSong, '_set_theme')
    def test_run_application(self, mock_set_theme: MagicMock, mock_prepare_layout: MagicMock) -> None:
        self.memo_song_cls.run_application()
        mock_set_theme.assert_called_once_with()
        mock_prepare_layout.assert_called_once_with()
        self.memo_song_cls.root.mainloop.assert_called_once_with()

    def test_quit_application(self) -> None:
        self.memo_song_cls.quit_application()
        self.memo_song_cls.root.destroy.assert_called_once_with()

    @patch.object(MemoSong, '_initialize_sound_mixer')
    @patch.object(MemoSong, 'configure_piano')
    @patch.object(MemoSong, 'configure_notepad')
    @patch.object(MemoSong, 'configure_file_browser')
    @patch.object(MemoSong, 'configure_control_panel')
    @patch.object(MemoSong, 'configure_voice_recorder')
    @patch.object(MemoSong, 'configure_logo')
    @patch.object(MemoSong, '_load_image_names')
    def test_prepare_layout(self, mock_load_image_names: MagicMock, mock_configure_logo: MagicMock,
                            mock_configure_voice_recorder: MagicMock, mock_configure_control_panel: MagicMock,
                            mock_configure_file_browser: MagicMock, mock_configure_notepad: MagicMock,
                            mock_configure_piano: MagicMock, mock_initialize_sound_mixer: MagicMock) -> None:
        self.memo_song_cls.prepare_layout()
        mock_load_image_names.assert_called_once_with()
        mock_configure_logo.assert_called_once_with()
        mock_configure_voice_recorder.assert_called_once_with()
        mock_configure_control_panel.assert_called_once_with()
        mock_configure_file_browser.assert_has_calls([call('recordings', 2), call('notes', 4)])
        mock_configure_notepad.assert_called_once_with()
        mock_configure_piano.assert_called_once_with()
        mock_initialize_sound_mixer.assert_called_once_with()

    def test_configure_window(self) -> None:
        self.memo_song_cls.configure_window()
        self.memo_song_cls.root.title.assert_called_once_with('MemoSong')
        self.memo_song_cls.root.iconbitmap.assert_called_once_with(f'{self.memo_song_cls.images_path}/logo.ico')
        self.memo_song_cls.root.configure.assert_called_once_with()
        self.memo_song_cls.root.geometry.assert_called_once_with('1000x535+1+1')
        self.memo_song_cls.root.resizable.assert_called_once_with(0, 0)
        self.memo_song_cls.root.columnconfigure.assert_called_once_with(0, weight=1)

    @patch.object(MemoSong, '_open_image', return_value='image')
    @patch.object(MemoSong, '_create_label')
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_logo(self, mock_create_main_frame: MagicMock, mock_create_label: MagicMock,
                            mock_open_image: MagicMock) -> None:
        self.memo_song_cls.configure_logo()
        mock_create_main_frame.assert_called_once_with(0, 0, sticky='nw', frame_data={'width': 142, 'height': 133})
        mock_create_label.assert_called_once_with(mock_tkinter_frame, '', image='image', padx=20, pady=20)
        mock_open_image.assert_called_once_with('logo_image', (110, 105))

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, 'add_voice_recorder_title_frame')
    @patch.object(MemoSong, '_create_label')
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_voice_recorder(self, mock_create_main_frame: MagicMock, mock_create_label: MagicMock,
                                      mock_add_voice_recorder_title_frame: MagicMock,
                                      mock_create_button_from_image: MagicMock) -> None:
        self.memo_song_cls.configure_voice_recorder()
        mock_create_main_frame.assert_called_once_with(1, 0, sticky='nw', frame_data={'width': 250, 'height': 133})
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'RECORD VOICE', side='top')
        mock_add_voice_recorder_title_frame.assert_called_once_with(mock_tkinter_frame)
        mock_create_button_from_image.assert_has_calls([
            call(mock_tkinter_frame, 'start_voice_recording', (40, 55),
                 self.memo_song_cls.recording_manager.start_voice_recording, 'left',
                 self.memo_song_cls.recording_manager, width=60),
            call(mock_tkinter_frame, 'pause_voice_recording', (40, 55),
                 self.memo_song_cls.recording_manager.pause_voice_recording, 'left',
                 self.memo_song_cls.recording_manager, width=60),
            call(mock_tkinter_frame, 'stop_voice_recording', (40, 55),
                 self.memo_song_cls.recording_manager.stop_voice_recording, 'left',
                 self.memo_song_cls.recording_manager, width=60)
        ])

    @patch.object(MemoSong, '_create_label')
    def test_add_voice_recorder_title_frame(self, mock_create_label: MagicMock) -> None:
        mock_tkinter_frame.reset_mock()
        mock_tkinter_entry.reset_mock()
        self.memo_song_cls.add_voice_recorder_title_frame(mock_tkinter_frame)
        mock_tkinter_frame.pack.assert_called_once_with(side='bottom')
        mock_tkinter_entry.pack.assert_called_once_with(side='bottom')
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'Title: ', side='bottom')

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, 'add_update_file_frame')
    @patch.object(MemoSong, 'add_piano_recorder_title_frame')
    @patch.object(MemoSong, '_create_label')
    def test_configure_control_panel(self, mock_create_label: MagicMock,
                                     mock_add_piano_recorder_title_frame: MagicMock,
                                     mock_add_update_file_frame: MagicMock,
                                     mock_create_button_from_image: MagicMock) -> None:
        mock_tkinter_frame.reset_mock()
        self.memo_song_cls._create_main_frame = MagicMock(return_value=mock_tkinter_frame)
        self.memo_song_cls.configure_control_panel()
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'RECORD PIANO', anchor='w', padx=68)
        mock_add_piano_recorder_title_frame.assert_called_once_with(mock_tkinter_frame)
        mock_add_update_file_frame.assert_called_once_with(mock_tkinter_frame)
        mock_create_button_from_image.assert_has_calls([
            call(mock_tkinter_frame, 'start_piano_recording', (60, 60),
                 self.memo_song_cls.recording_manager.start_piano_recording, 'left',
                 self.memo_song_cls.recording_manager),
            call(mock_tkinter_frame, 'pause_piano_recording', (60, 60),
                 self.memo_song_cls.recording_manager.pause_piano_recording, 'left',
                 self.memo_song_cls.recording_manager),
            call(mock_tkinter_frame, 'stop_piano_recording', (60, 60),
                 self.memo_song_cls.recording_manager.stop_piano_recording, 'left',
                 self.memo_song_cls.recording_manager)
        ])

    @patch.object(MemoSong, '_create_control_button')
    @patch.object(MemoSong, '_create_label', return_value=MagicMock())
    def test_add_update_file_frame(self, mock_create_label: MagicMock, mock_create_control_button: MagicMock) -> None:
        mock_tkinter_frame.reset_mock()
        self.memo_song_cls.add_update_file_frame(mock_tkinter_frame)
        mock_tkinter_frame.pack.assert_called_once_with(side='right')
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'EDIT FILE')
        # mock_create_control_button.assert_has_calls([
        #     call(mock_tkinter_frame, 'Rename', self.memo_song_cls.file_manager.edit_file(), width=70),
        #     call(mock_tkinter_frame, 'Delete', self.memo_song_cls.file_manager.edit_file(), width=70)
        #     ])

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, '_create_label')
    def test_add_piano_recorder_title_frame(self, mock_create_label: MagicMock,
                                            mock_create_button_from_image: MagicMock) -> None:
        self.memo_song_cls.add_piano_recorder_title_frame(mock_tkinter_frame)
        mock_tkinter_frame.pack.assert_called_once_with(side='bottom', fill='both')
        mock_create_label.assert_called_once_with(mock_tkinter_frame, '  Title: ', side='left')
        mock_tkinter_entry.pack.assert_called_once_with(side='left')
        mock_create_button_from_image.assert_has_calls([
            call(mock_tkinter_frame, 'keyboard', (45, 25), self.memo_song_cls._turn_keyboard_piano, 'left',
                 self.memo_song_cls),
            call(mock_tkinter_frame, 'mute', (25, 25), self.memo_song_cls._mute_playback, 'right', self.memo_song_cls)
        ])
        self.memo_song_cls.root.bind.assert_called_once_with('`', self.memo_song_cls._turn_keyboard_piano)

    @patch.object(MemoSong, '_add_keyboard_text')
    @patch.object(MemoSong, '_highlight_used_function')
    def test_turn_keyboard_piano_on(self, mock_highlight_used_function: MagicMock,
                                    mock_add_keyboard_text: MagicMock) -> None:
        self.memo_song_cls.keyboard_on = False
        self.memo_song_cls._turn_keyboard_piano()
        self.memo_song_cls.root.focus.assert_called_once_with()
        mock_highlight_used_function.assert_called_once_with('keyboard', 'on')
        self.memo_song_cls.root.bind.assert_called_once_with('<Key>', self.memo_song_cls._play_pressed_key)
        mock_add_keyboard_text.assert_called_once_with()
        self.assertEqual(self.memo_song_cls.keyboard_on, True)

    @patch.object(MemoSong, '_remove_keyboard_text')
    @patch.object(MemoSong, '_highlight_used_function')
    def test_turn_keyboard_piano_off(self, mock_highlight_used_function: MagicMock,
                                     mock_remove_keyboard_text: MagicMock) -> None:
        self.memo_song_cls.keyboard_on = True
        self.memo_song_cls._turn_keyboard_piano()
        mock_highlight_used_function.assert_called_once_with('keyboard', 'off')
        self.memo_song_cls.root.unbind.assert_called_once_with('<Key>')
        mock_remove_keyboard_text.assert_called_once_with()
        self.assertEqual(self.memo_song_cls.keyboard_on, False)

    @patch.object(MemoSong, '_play_key')
    @patch.object(MemoSong, '_highlight_button')
    def test_play_pressed_key(self, mock_highlight_button: MagicMock, mock_play_key: MagicMock) -> None:
        mock_event.char.lower = MagicMock(return_value='q')
        self.memo_song_cls.root.update_idletasks = MagicMock()
        self.memo_song_cls._play_pressed_key(mock_event)
        mock_event.char.lower.assert_called_once_with()
        mock_highlight_button.assert_called_once_with('q')
        self.memo_song_cls.root.update_idletasks.assert_called_once_with()
        mock_play_key.assert_called_once_with('q')

    @patch.object(MemoSong, '_play_key')
    @patch.object(MemoSong, '_highlight_button')
    def test_play_pressed_key_wrong_key(self, mock_highlight_button: MagicMock, mock_play_key: MagicMock) -> None:
        mock_event.char.lower = MagicMock(return_value='1')
        self.memo_song_cls.root.update_idletasks = MagicMock()
        self.memo_song_cls._play_pressed_key(mock_event)
        mock_event.char.lower.assert_called_once_with()
        mock_highlight_button.assert_not_called()
        self.memo_song_cls.root.update_idletasks.assert_not_called()
        mock_play_key.assert_not_called()

    @patch('piano.Piano.key', return_value='q')
    @patch.object(MemoSong, '_start_new_thread')
    @patch.object(MemoSong.piano, 'play_key')
    def test_play_key_repeated_key(self, mock_piano_play_key: MagicMock, mock_start_new_thread: MagicMock,
                                   _: MagicMock) -> None:
        self.memo_song_cls._play_key('q')
        self.assertEqual(self.memo_song_cls.piano.key, 'q')
        mock_start_new_thread.assert_called_once_with(mock_piano_play_key)

    @patch('piano.Piano.key', return_value='q')
    @patch.object(MemoSong, '_start_new_thread')
    @patch.object(MemoSong.piano, 'play_key')
    def test_play_key_changed_key(self, mock_piano_play_key: MagicMock, mock_start_new_thread: MagicMock,
                                  _: MagicMock) -> None:
        self.memo_song_cls._play_key('2')
        self.assertEqual(self.memo_song_cls.piano.key, '2')
        mock_start_new_thread.assert_called_once_with(mock_piano_play_key)

    @patch.object(MemoSong, '_create_radiobutton_list')
    @patch.object(MemoSong, '_create_control_button')
    @patch.object(MemoSong, '_create_label', return_value=mock_tkinter_label)
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_file_browser(self, mock_create_main_frame: MagicMock, mock_create_label: MagicMock,
                                    mock_create_control_button: MagicMock,
                                    mock_create_radiobutton_list: MagicMock) -> None:
        mock_tkinter_frame.reset_mock()
        mock_tkinter_entry.reset_mock()
        self.memo_song_cls.configure_file_browser('recordings', 2)
        mock_create_main_frame.assert_called_once_with(2, 0, grid_data={'rowspan': 2})
        mock_create_label.assert_has_calls([
            call(mock_tkinter_frame, 'RECORDINGS', side='top'), call(mock_tkinter_frame, 'Find: ', side='left')
        ])
        # mock_tkinter_frame.pack.assert_called_once_with(side='top', fill='both')
        # mock_tkinter_entry.pack.assert_called_once_with(side='left', fill='both', expand=1)
        # mock_create_control_button.assert_has_calls([
        #     call(mock_tkinter_frame, 'Search', self.memo_song_cls.file_manager.search_recordings, 'left', width=1),
        #     call(mock_tkinter_frame, 'Update List', self.memo_song_cls.file_manager.update_list, 'bottom')])
        mock_create_radiobutton_list.assert_called_once_with(mock_tkinter_frame, 'recordings',
                                                             self.memo_song_cls.recording_manager.play_recording)
        self.assertEqual(getattr(self.memo_song_cls.file_manager, 'recordings_search_field'), mock_tkinter_entry)

    @patch('file_manager.FileManager.create_radiobutton_list', return_value='radiobutton_list')
    def test_create_radiobutton_list_recordings(self, mock_create_radiobutton_list: MagicMock) -> None:
        self.memo_song_cls._create_radiobutton_list(mock_tkinter_frame, 'recordings', 'command')
        mock_create_radiobutton_list.assert_called_once_with(mock_tkinter_frame, 'recordings', 'command')
        self.assertEqual(self.memo_song_cls.file_manager.recordings_radiobutton_list, 'radiobutton_list')

    @patch('file_manager.FileManager.create_radiobutton_list', return_value='notes_list')
    def test_create_radiobutton_list_notes(self, mock_create_radiobutton_list: MagicMock) -> None:
        self.memo_song_cls._create_radiobutton_list(mock_tkinter_frame, 'notes', 'command')
        mock_create_radiobutton_list.assert_called_once_with(mock_tkinter_frame, 'notes', 'command')
        self.assertEqual(self.memo_song_cls.file_manager.notes_radiobutton_list, 'notes_list')

    @patch.object(MemoSong, '_setup_notepad', return_value=mock_tkinter_textbox)
    @patch.object(MemoSong, '_create_control_button', return_value=mock_tkinter_button)
    @patch.object(MemoSong, '_create_label', return_value=mock_tkinter_label)
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_notepad(self, mock_create_main_frame: MagicMock, mock_create_label: MagicMock,
                               mock_create_control_button: MagicMock, mock_setup_notepad: MagicMock) -> None:
        mock_tkinter_frame.reset_mock()
        self.memo_song_cls.configure_notepad()
        mock_create_main_frame.assert_called_once_with(3, 0, frame_data={'height': 335}, grid_data={'rowspan': 2})
        mock_create_label.assert_has_calls([
            call(mock_tkinter_frame, 'NOTEPAD', side='top'), call(mock_tkinter_frame, 'Title: ', side='left')
        ])
        mock_tkinter_frame.pack.assert_called_once_with(side='top', fill='both')
        mock_create_control_button.assert_has_calls([
            call(mock_tkinter_frame, 'Save', self.memo_song_cls.note_manager.save_note, 'left', width=1),
            call(mock_tkinter_frame, 'Clear Notepad', self.memo_song_cls.note_manager.clear_notepad, 'bottom')
        ])
        mock_setup_notepad.assert_called_once_with(mock_tkinter_frame, mock_tkinter_frame)

    def test_setup_notepad(self) -> None:
        mock_tkinter_entry.reset_mock()
        mock_tkinter_textbox.reset_mock()
        self.memo_song_cls._setup_notepad(MagicMock(), MagicMock())
        mock_tkinter_entry.pack.assert_called_once_with(side='left', fill='both', expand=1)
        mock_tkinter_textbox.pack.assert_called_once_with(side='bottom', fill='both', expand=1)
        self.assertEqual(self.memo_song_cls.file_manager.notepad_title_field, mock_tkinter_entry)
        self.assertEqual(self.memo_song_cls.file_manager.notepad_text_area, mock_tkinter_textbox)

    @patch.object(MemoSong, '_create_piano_button')
    @patch.object(MemoSong, '_is_white_key', side_effect=2*is_white_key)
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_piano(self, mock_create_main_frame: MagicMock, mock_is_white_key: MagicMock,
                             mock_create_piano_button: MagicMock) -> None:
        self.memo_song_cls.configure_piano()
        mock_create_main_frame.assert_called_once_with(0, 2, grid_data={'columnspan': 5})
        mock_is_white_key.assert_has_calls(calls_each_key)
        mock_create_piano_button.assert_has_calls(calls_configure_piano)

    def test_create_main_frame(self) -> None:
        mock_tkinter_frame.reset_mock()
        frame = self.memo_song_cls._create_main_frame(0, 0, sticky='nw', frame_data={'width': 142, 'height': 133})
        mock_tkinter_frame.grid.assert_called_once_with(column=0, row=0, sticky='nw')
        self.assertEqual(frame, mock_tkinter_frame)

    @patch.object(MemoSong, '_add_key_names')
    def test_create_piano_button(self, mock_add_key_names: MagicMock) -> None:
        self.memo_song_cls._create_piano_button(MagicMock(), 'q', 0, 0, 0)
        mock_add_key_names.assert_called_once_with(mock_tkinter_button, 'q')
        self.assertEqual(getattr(self.memo_song_cls, 'q_key'), mock_tkinter_button)


if __name__ == '__main__':
    unittest.main()
