import unittest
import tkinter
import customtkinter
from mock import MagicMock, call, patch
from memo_song import MemoSong
from file_manager import FileManager
from generic_functions import GenericFunctions
from piano import Piano


class TestMemoSong(unittest.TestCase):
    mock_tkinter_frame = MagicMock()
    customtkinter.CTkFrame = MagicMock(return_value=mock_tkinter_frame)
    mock_tkinter_label = MagicMock()
    customtkinter.CTkLabel = MagicMock(return_value=mock_tkinter_label)
    mock_tkinter_button = MagicMock()
    customtkinter.CTkButton = MagicMock(return_value=mock_tkinter_button)
    mock_tkinter_entry = MagicMock()
    customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
    mock_tkinter_image = MagicMock()
    customtkinter.CTkImage = MagicMock(return_value=mock_tkinter_image)
    mock_tkinter_textbox = MagicMock()
    customtkinter.CTkTextbox = MagicMock(return_value=mock_tkinter_textbox)
    mock_event = MagicMock()
    tkinter.Event = MagicMock(return_value=mock_event)

    def setUp(self) -> None:
        self.root = customtkinter.CTk()
        self.memo_song = MemoSong(self.root)
        self.memo_song.root = MagicMock()

    def tearDown(self) -> None:
        if self.root:
            self.root.destroy()

    @patch.object(MemoSong, 'prepare_layout')
    @patch.object(MemoSong, '_set_theme')
    def test_run_application(self, mock_set_theme: MagicMock, mock_prepare_layout: MagicMock) -> None:
        self.memo_song.run_application()
        mock_set_theme.assert_called_once_with()
        mock_prepare_layout.assert_called_once_with()
        self.memo_song.root.mainloop.assert_called_once_with()

    def test_quit_application(self) -> None:
        self.memo_song.quit_application()
        self.memo_song.root.destroy.assert_called_once_with()

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
        self.memo_song.prepare_layout()
        mock_load_image_names.assert_called_once_with()
        mock_configure_logo.assert_called_once_with()
        mock_configure_voice_recorder.assert_called_once_with()
        mock_configure_control_panel.assert_called_once_with()
        mock_configure_file_browser.assert_has_calls([call('recordings', 2), call('notes', 4)])
        mock_configure_notepad.assert_called_once_with()
        mock_configure_piano.assert_called_once_with()
        mock_initialize_sound_mixer.assert_called_once_with()

    def test_configure_window(self) -> None:
        self.memo_song.configure_window()
        self.memo_song.root.title.assert_called_once_with('MemoSong')
        self.memo_song.root.iconbitmap.assert_called_once_with(f'{self.memo_song.images_path}/logo.ico')
        self.memo_song.root.configure.assert_called_once_with()
        self.memo_song.root.geometry.assert_called_once_with('1000x535+1+1')
        self.memo_song.root.resizable.assert_called_once_with(0, 0)
        self.memo_song.root.columnconfigure.assert_called_once_with(0, weight=1)

    @patch.object(MemoSong, '_open_image', return_value='image')
    @patch.object(MemoSong, '_create_label')
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_logo(self, mock_create_main_frame: MagicMock, mock_create_label: MagicMock,
                            mock_open_image: MagicMock) -> None:
        self.memo_song.configure_logo()
        mock_create_main_frame.assert_called_once_with(0, 0, sticky='nw', frame_data={'width': 142, 'height': 133})
        mock_create_label.assert_called_once_with(self.mock_tkinter_frame, '', image='image', padx=20, pady=20)
        mock_open_image.assert_called_once_with('logo_image', (110, 105))

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, 'add_voice_recorder_title_frame')
    @patch.object(MemoSong, '_create_label')
    @patch.object(MemoSong, '_create_main_frame', return_value=mock_tkinter_frame)
    def test_configure_voice_recorder(self, mock_create_main_frame: MagicMock, mock_create_label: MagicMock,
                                      mock_add_voice_recorder_title_frame: MagicMock,
                                      mock_create_button_from_image: MagicMock) -> None:
        self.memo_song.configure_voice_recorder()
        mock_create_main_frame.assert_called_once_with(1, 0, sticky='nw', frame_data={'width': 250, 'height': 133})
        mock_create_label.assert_called_once_with(self.mock_tkinter_frame, 'RECORD VOICE', side='top')
        mock_add_voice_recorder_title_frame.assert_called_once_with(self.mock_tkinter_frame)
        mock_create_button_from_image.assert_has_calls([
            call(self.mock_tkinter_frame, 'start_voice_recording', (40, 55),
                 self.memo_song.recording_manager.start_voice_recording, 'left',
                 self.memo_song.recording_manager, width=60),
            call(self.mock_tkinter_frame, 'pause_voice_recording', (40, 55),
                 self.memo_song.recording_manager.pause_voice_recording, 'left',
                 self.memo_song.recording_manager, width=60),
            call(self.mock_tkinter_frame, 'stop_voice_recording', (40, 55),
                 self.memo_song.recording_manager.stop_voice_recording, 'left',
                 self.memo_song.recording_manager, width=60)])

    @patch.object(MemoSong, '_create_label')
    def test_add_voice_recorder_title_frame(self, mock_create_label: MagicMock) -> None:
        self.mock_tkinter_frame.reset_mock()
        self.mock_tkinter_entry.reset_mock()
        self.memo_song.add_voice_recorder_title_frame(self.mock_tkinter_frame)
        self.mock_tkinter_frame.pack.assert_called_once_with(side='bottom')
        self.mock_tkinter_entry.pack.assert_called_once_with(side='bottom')
        mock_create_label.assert_called_once_with(self.mock_tkinter_frame, 'Title: ', side='bottom')

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, 'add_update_file_frame')
    @patch.object(MemoSong, 'add_piano_recorder_title_frame')
    @patch.object(MemoSong, '_create_label')
    def test_configure_control_panel(self, mock_create_label: MagicMock,
                                     mock_add_piano_recorder_title_frame: MagicMock,
                                     mock_add_update_file_frame: MagicMock,
                                     mock_create_button_from_image: MagicMock) -> None:
        self.mock_tkinter_frame.reset_mock()
        self.memo_song._create_main_frame = MagicMock(return_value=self.mock_tkinter_frame)
        self.memo_song.configure_control_panel()
        mock_create_label.assert_called_once_with(self.mock_tkinter_frame, 'RECORD PIANO', anchor='w', padx=68)
        mock_add_piano_recorder_title_frame.assert_called_once_with(self.mock_tkinter_frame)
        mock_add_update_file_frame.assert_called_once_with(self.mock_tkinter_frame)
        mock_create_button_from_image.assert_has_calls([
            call(self.mock_tkinter_frame, 'start_piano_recording', (60, 60),
                 self.memo_song.recording_manager.start_piano_recording, 'left', self.memo_song.recording_manager),
            call(self.mock_tkinter_frame, 'pause_piano_recording', (60, 60),
                 self.memo_song.recording_manager.pause_piano_recording, 'left', self.memo_song.recording_manager),
            call(self.mock_tkinter_frame, 'stop_piano_recording', (60, 60),
                 self.memo_song.recording_manager.stop_piano_recording, 'left', self.memo_song.recording_manager)
        ])

    @patch.object(FileManager, 'edit_file')
    @patch.object(MemoSong, '_create_control_button')
    @patch.object(MemoSong, '_create_label', return_value=MagicMock())
    def test_add_update_file_frame(self, mock_create_label: MagicMock, mock_create_control_button: MagicMock,
                                   mock_file_manager_edit_file: MagicMock) -> None:
        self.mock_tkinter_frame.reset_mock()
        self.memo_song.add_update_file_frame(self.mock_tkinter_frame)
        self.mock_tkinter_frame.pack.assert_called_once_with(side='right')
        mock_create_label.assert_called_once_with(self.mock_tkinter_frame, 'EDIT FILE')
        # mock_create_control_button.assert_has_calls([
        #     call(mock_tkinter_frame, 'Rename', mock_lambda_function, width=70),
        #     call(mock_tkinter_frame, 'Delete', mock_lambda_function, width=70)
        # ])

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, '_create_label')
    def test_add_piano_recorder_title_frame(self, mock_create_label: MagicMock,
                                            mock_create_button_from_image: MagicMock) -> None:
        self.memo_song.add_piano_recorder_title_frame(self.mock_tkinter_frame)
        self.mock_tkinter_frame.pack.assert_called_once_with(side='bottom', fill='both')
        mock_create_label.assert_called_once_with(self.mock_tkinter_frame, '  Title: ', side='left')
        self.mock_tkinter_entry.pack.assert_called_once_with(side='left')
        mock_create_button_from_image.assert_has_calls([
            call(self.mock_tkinter_frame, 'keyboard', (45, 25),
                 self.memo_song._turn_keyboard_piano, 'left', self.memo_song),
            call(self.mock_tkinter_frame, 'mute', (25, 25),
                 self.memo_song._mute_playback, 'right', self.memo_song)])
        self.memo_song.root.bind.assert_called_once_with('`', self.memo_song._turn_keyboard_piano)

    @patch.object(MemoSong, '_add_keyboard_text')
    @patch.object(MemoSong, '_highlight_used_function')
    def test_turn_keyboard_piano_on(self, mock_highlight_used_function: MagicMock,
                                    mock_add_keyboard_text: MagicMock) -> None:
        self.memo_song.keyboard_on = False
        self.memo_song._turn_keyboard_piano()
        self.memo_song.root.focus.assert_called_once_with()
        mock_highlight_used_function.assert_called_once_with('keyboard', 'on')
        self.memo_song.root.bind.assert_called_once_with('<Key>', self.memo_song._play_pressed_key)
        mock_add_keyboard_text.assert_called_once_with()
        self.assertEqual(self.memo_song.keyboard_on, True)

    @patch.object(MemoSong, '_remove_keyboard_text')
    @patch.object(MemoSong, '_highlight_used_function')
    def test_turn_keyboard_piano_off(self, mock_highlight_used_function: MagicMock,
                                     mock_remove_keyboard_text: MagicMock) -> None:
        self.memo_song.keyboard_on = True
        self.memo_song._turn_keyboard_piano()
        mock_highlight_used_function.assert_called_once_with('keyboard', 'off')
        self.memo_song.root.unbind.assert_called_once_with('<Key>')
        mock_remove_keyboard_text.assert_called_once_with()
        self.assertEqual(self.memo_song.keyboard_on, False)

    @patch.object(MemoSong, '_play_key')
    @patch.object(MemoSong, '_highlight_button')
    def test_play_pressed_key(self, mock_highlight_button: MagicMock, mock_play_key: MagicMock) -> None:
        self.mock_event.char.lower = MagicMock(return_value='q')
        self.memo_song.root.update_idletasks = MagicMock()
        self.memo_song._play_pressed_key(self.mock_event)
        self.mock_event.char.lower.assert_called_once_with()
        mock_highlight_button.assert_called_once_with('q')
        self.memo_song.root.update_idletasks.assert_called_once_with()
        mock_play_key.assert_called_once_with('q')

    @patch.object(MemoSong, '_play_key')
    @patch.object(MemoSong, '_highlight_button')
    def test_play_pressed_key_wrong_key(self, mock_highlight_button: MagicMock, mock_play_key: MagicMock) -> None:
        self.mock_event.char.lower = MagicMock(return_value='1')
        self.memo_song.root.update_idletasks = MagicMock()
        self.memo_song._play_pressed_key(self.mock_event)
        self.mock_event.char.lower.assert_called_once_with()
        mock_highlight_button.assert_not_called()
        self.memo_song.root.update_idletasks.assert_not_called()
        mock_play_key.assert_not_called()

    @patch.object(Piano, 'key', return_value='q')
    @patch.object(MemoSong, '_start_new_thread')
    @patch.object(MemoSong.piano, 'play_key')
    def test_play_key_repeated_key(self, mock_piano_play_key: MagicMock, mock_start_new_thread: MagicMock,
                                   _: MagicMock) -> None:
        self.memo_song._play_key('q')
        self.assertEqual(Piano.key, 'q')
        mock_start_new_thread.assert_called_once_with(mock_piano_play_key)

    @patch.object(Piano, 'key', return_value='q')
    @patch.object(MemoSong, '_start_new_thread')
    @patch.object(MemoSong.piano, 'play_key')
    def test_play_key_changed_key(self, mock_piano_play_key: MagicMock, mock_start_new_thread: MagicMock,
                                  _: MagicMock) -> None:
        self.memo_song._play_key('2')
        self.assertEqual(Piano.key, '2')
        mock_start_new_thread.assert_called_once_with(mock_piano_play_key)

    def test_configure_file_browser(self):
        # browser_frame = self._create_main_frame(column_number, 0, grid_data={'rowspan': 2})
        # self._create_label(browser_frame, browser_type.upper(), side=tkinter.TOP)
        # header_frame = customtkinter.CTkFrame(browser_frame)
        # header_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        # self._create_label(header_frame, 'Find: ', side=tkinter.LEFT)
        # browser_search_field = customtkinter.CTkEntry(header_frame, width=120)
        # browser_search_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        # setattr(self.file_manager, f'{browser_type}_search_field', browser_search_field)
        # self._create_control_button(header_frame, 'Search', getattr(self.file_manager, f'search_{browser_type}'),
        #                             tkinter.LEFT, width=1)
        # self._create_control_button(browser_frame, 'Update List', lambda: self.file_manager.update_list(browser_type),
        #                             tkinter.BOTTOM)
        # if browser_type == 'notes':
        #     command = self.note_manager.open_note
        # else:
        #     command = self.recording_manager.play_recording
        # self._create_radiobutton_list(browser_frame, browser_type, command)
        pass

    @patch.object(FileManager, 'create_radiobutton_list', return_value='radiobutton_list')
    def test_create_radiobutton_list_recordings(self, mock_create_radiobutton_list: MagicMock) -> None:
        self.memo_song._create_radiobutton_list(self.mock_tkinter_frame, 'recordings', 'command')
        mock_create_radiobutton_list.assert_called_once_with(self.mock_tkinter_frame, 'recordings', 'command')
        self.assertEqual(FileManager.recordings_radiobutton_list, 'radiobutton_list')

    @patch.object(FileManager, 'create_radiobutton_list', return_value='notes_list')
    def test_create_radiobutton_list_notes(self, mock_create_radiobutton_list: MagicMock) -> None:
        self.memo_song._create_radiobutton_list(self.mock_tkinter_frame, 'notes', 'command')
        mock_create_radiobutton_list.assert_called_once_with(self.mock_tkinter_frame, 'notes', 'command')
        self.assertEqual(FileManager.notes_radiobutton_list, 'notes_list')

    def test_configure_notepad(self):
        # notepad_frame = self._create_main_frame(3, 0, frame_data={'height': self._height-200}, grid_data={'rowspan': 2})
        # self._create_label(notepad_frame, 'NOTEPAD', side=tkinter.TOP)
        # header_frame = customtkinter.CTkFrame(notepad_frame)
        # header_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        # self._create_control_button(header_frame, 'Save', self.note_manager.save_note, tkinter.LEFT, width=1)
        # self._create_label(header_frame, 'Title: ', side=tkinter.LEFT)
        # self._create_control_button(notepad_frame, 'Clear Notepad', self.note_manager.clear_notepad, tkinter.BOTTOM)
        # self._setup_notepad(header_frame, notepad_frame)
        pass

    def test_setup_notepad(self) -> None:
        self.mock_tkinter_entry.reset_mock()
        self.mock_tkinter_textbox.reset_mock()
        self.memo_song._setup_notepad(MagicMock(), MagicMock())
        self.mock_tkinter_entry.pack.assert_called_once_with(side='left', fill='both', expand=1)
        self.mock_tkinter_textbox.pack.assert_called_once_with(side='bottom', fill='both', expand=1)
        self.assertEqual(FileManager.notepad_title_field, self.mock_tkinter_entry)
        self.assertEqual(FileManager.notepad_text_area, self.mock_tkinter_textbox)

    def test_configure_piano(self):
        # piano_frame = self._create_main_frame(0, 2, grid_data={'columnspan': 5})
        # key_swift = 45
        # pad_x_white = 5
        # pad_x_black = 40
        # for key in self.key_map:
        #     if self._is_white_key(key):
        #         self._create_piano_button(piano_frame, key, pad_x_white, 3, 5, fg_color='white', width=47, height=225,
        #                                   border_width=1, border_color='black')
        #         pad_x_white += key_swift
        # for key in self.key_map:
        #     if key in ['e', 'u', 'p', 'x', 'b']:
        #         pad_x_black += key_swift
        #     if not self._is_white_key(key):
        #         self._create_piano_button(piano_frame, key, pad_x_black, 4, 26, fg_color='black', width=22, height=140)
        #         pad_x_black += key_swift
        pass

    def test_create_main_frame(self) -> None:
        self.mock_tkinter_frame.reset_mock()
        frame = self.memo_song._create_main_frame(0, 0, sticky='nw', frame_data={'width': 142, 'height': 133})
        self.mock_tkinter_frame.grid.assert_called_once_with(column=0, row=0, sticky='nw')
        self.assertEqual(frame, self.mock_tkinter_frame)

    @patch.object(MemoSong, '_add_key_names')
    def test_create_piano_button(self, mock_add_key_names: MagicMock) -> None:
        self.memo_song._create_piano_button(MagicMock(), 'q', 0, 0, 0)
        mock_add_key_names.assert_called_once_with(self.mock_tkinter_button, 'q')
        self.assertEqual(getattr(GenericFunctions, 'q_key'), self.mock_tkinter_button)


if __name__ == '__main__':
    unittest.main()
