import unittest
import tkinter
import customtkinter
import pygame
from PIL import Image
from mock import MagicMock, call, patch, mock_open
from memo_song import MemoSong
from file_manager import FileManager
from generic_functions import GenericFunctions
from piano import Piano


class TestMemoSong(unittest.TestCase):
    calls_each_key = [call('q'), call('2'), call('w'), call('3'), call('e'), call('r'), call('5'), call('t'),
                      call('6'), call('y'), call('7'), call('u'), call('i'), call('9'), call('o'), call('0'),
                      call('p'), call('['), call('='), call(']'), call('a'), call('z'), call('s'), call('x'),
                      call('c'), call('f'), call('v'), call('g'), call('b'), call('n'), call('j'), call('m'),
                      call('k'), call(','), call('l'), call('.'), call('/')]
    is_white_key = 3 * [True, False, True, False, True, True, False, True, False, True, False, True] + [True]

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

    @patch.object(MemoSong, '_set_image_name')
    def test_load_image_names(self, mock_set_image_name: MagicMock) -> None:
        self.memo_song._load_image_names()
        mock_set_image_name.assert_has_calls([
            call('idle'), call('keyboard'), call('logo'), call('mute'),
            call('pause_piano_recording'), call('pause_voice_recording'), call('playing'),
            call('start_piano_recording'), call('start_voice_recording'),
            call('stop_piano_recording'), call('stop_voice_recording')])

    def test_set_image_name(self) -> None:
        self.memo_song._set_image_name('keyboard')
        self.assertEqual(getattr(self.memo_song, f'keyboard_image'), f'{self.memo_song.images_path}/keyboard.png')

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

    def test_create_main_frame(self) -> None:
        mock_tkinter_frame = MagicMock()
        customtkinter.CTkFrame = MagicMock(return_value=mock_tkinter_frame)
        frame = self.memo_song._create_main_frame(0, 0, sticky='nw', frame_data={'width': 142, 'height': 133})
        mock_tkinter_frame.grid.assert_called_once_with(column=0, row=0, sticky='nw')
        self.assertEqual(frame, mock_tkinter_frame)

    def test_create_label(self) -> None:
        mock_tkinter_label = MagicMock()
        customtkinter.CTkLabel = MagicMock(return_value=mock_tkinter_label)
        self.memo_song._create_label(MagicMock(), text='text')
        mock_tkinter_label.pack.assert_called_once_with()

    def test_create_label_kwargs(self) -> None:
        mock_tkinter_label = MagicMock()
        customtkinter.CTkLabel = MagicMock(return_value=mock_tkinter_label)
        self.memo_song._create_label(MagicMock(), text='', pady=20, side=tkinter.TOP)
        mock_tkinter_label.pack.assert_called_once_with(pady=20, side='top')

    @patch.object(MemoSong, '_open_image', return_value='image')
    def test_create_label_image(self, mock_open_image: MagicMock) -> None:
        mock_tkinter_label = MagicMock()
        customtkinter.CTkLabel = MagicMock(return_value=mock_tkinter_label)
        self.memo_song._create_label(MagicMock(), text='', image=mock_open_image)
        mock_tkinter_label.pack.assert_called_once_with()

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
        mock_tkinter_frame = MagicMock()
        customtkinter.CTkFrame = MagicMock(return_value=mock_tkinter_frame)
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        self.memo_song.add_voice_recorder_title_frame(mock_tkinter_frame)
        mock_tkinter_frame.pack.assert_called_once_with(side='bottom')
        mock_tkinter_entry.pack.assert_called_once_with(side='bottom')
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'Title: ', side='bottom')

    @patch.object(MemoSong, '_open_image', return_value=mock_tkinter_image)
    def test_create_button_from_image(self, mock_open_image: MagicMock) -> None:
        self.memo_song._create_button_from_image(self.mock_tkinter_frame, 'keyboard', (45, 25),
                                                 self.memo_song._turn_keyboard_piano, tkinter.LEFT, self.memo_song)
        mock_open_image.assert_called_once_with('keyboard_image', (45, 25))
        self.mock_tkinter_button.pack.assert_called_once_with(side='left')
        self.assertEqual(getattr(self.memo_song, 'keyboard_button'), self.mock_tkinter_button)

    # def test_open_image(self):
    #     mock_image = MagicMock()
    #     self.memo_song.keyboard_image = MagicMock(return_value=mock_image)
    #     Image.open = MagicMock(return_value=mock_image)
    #     image = self.memo_song._open_image('keyboard_image')
    #     self.assertEqual(image, mock_image)

    @patch.object(MemoSong, '_create_button_from_image')
    @patch.object(MemoSong, 'add_update_file_frame')
    @patch.object(MemoSong, 'add_piano_recorder_title_frame')
    @patch.object(MemoSong, '_create_label')
    def test_configure_control_panel(self, mock_create_label: MagicMock,
                                     mock_add_piano_recorder_title_frame: MagicMock,
                                     mock_add_update_file_frame: MagicMock,
                                     mock_create_button_from_image: MagicMock) -> None:
        mock_tkinter_frame = MagicMock()
        customtkinter.CTkFrame = MagicMock(return_value=mock_tkinter_frame)
        self.memo_song._create_main_frame = MagicMock(return_value=mock_tkinter_frame)
        self.memo_song.configure_control_panel()
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'RECORD PIANO', anchor='w', padx=68)
        mock_add_piano_recorder_title_frame.assert_called_once_with(mock_tkinter_frame)
        mock_add_update_file_frame.assert_called_once_with(mock_tkinter_frame)
        mock_create_button_from_image.assert_has_calls([
            call(mock_tkinter_frame, 'start_piano_recording', (60, 60),
                 self.memo_song.recording_manager.start_piano_recording, 'left', self.memo_song.recording_manager),
            call(mock_tkinter_frame, 'pause_piano_recording', (60, 60),
                 self.memo_song.recording_manager.pause_piano_recording, 'left', self.memo_song.recording_manager),
            call(mock_tkinter_frame, 'stop_piano_recording', (60, 60),
                 self.memo_song.recording_manager.stop_piano_recording, 'left', self.memo_song.recording_manager)
        ])

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

    @patch.object(MemoSong, '_is_white_key', side_effect=is_white_key)
    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_add_keyboard_text(self, mock_get_button_from_key: MagicMock, mock_is_white_key: MagicMock) -> None:
        self.memo_song._add_keyboard_text()
        mock_is_white_key.assert_has_calls(self.calls_each_key)
        mock_get_button_from_key.assert_has_calls(self.calls_each_key)
        self.mock_tkinter_button.configure.assert_has_calls([
            call(text='q\nC', text_color='black', anchor='s'), call(text='2', text_color='white', anchor='s'),
            call(text='w\nD', text_color='black', anchor='s'), call(text='3', text_color='white', anchor='s'),
            call(text='e\nE', text_color='black', anchor='s'), call(text='r\nF', text_color='black', anchor='s'),
            call(text='5', text_color='white', anchor='s'), call(text='t\nG', text_color='black', anchor='s'),
            call(text='6', text_color='white', anchor='s'), call(text='y\nA', text_color='black', anchor='s'),
            call(text='7', text_color='white', anchor='s'), call(text='u\nB', text_color='black', anchor='s'),
            call(text='i\nC', text_color='black', anchor='s'), call(text='9', text_color='white', anchor='s'),
            call(text='o\nD', text_color='black', anchor='s'), call(text='0', text_color='white', anchor='s'),
            call(text='p\nE', text_color='black', anchor='s'), call(text='[\nF', text_color='black', anchor='s'),
            call(text='=', text_color='white', anchor='s'), call(text=']\nG', text_color='black', anchor='s'),
            call(text='a', text_color='white', anchor='s'), call(text='z\nA', text_color='black', anchor='s'),
            call(text='s', text_color='white', anchor='s'), call(text='x\nB', text_color='black', anchor='s'),
            call(text='c\nC', text_color='black', anchor='s'), call(text='f', text_color='white', anchor='s'),
            call(text='v\nD', text_color='black', anchor='s'), call(text='g', text_color='white', anchor='s'),
            call(text='b\nE', text_color='black', anchor='s'), call(text='n\nF', text_color='black', anchor='s'),
            call(text='j', text_color='white', anchor='s'), call(text='m\nG', text_color='black', anchor='s'),
            call(text='k', text_color='white', anchor='s'), call(text=',\nA', text_color='black', anchor='s'),
            call(text='l', text_color='white', anchor='s'), call(text='.\nB', text_color='black', anchor='s'),
            call(text='/\nC', text_color='black', anchor='s')
        ])

    @patch.object(MemoSong, '_is_white_key', side_effect=is_white_key)
    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_keyboard_text(self, mock_get_button_from_key: MagicMock, mock_is_white_key: MagicMock) -> None:
        self.memo_song._remove_keyboard_text()
        mock_is_white_key.assert_has_calls(self.calls_each_key)
        mock_get_button_from_key.assert_has_calls(self.calls_each_key)
        self.mock_tkinter_button.configure.assert_has_calls([
            call(text='C', anchor='s'), call(text=''), call(text='D', anchor='s'), call(text=''),
            call(text='E', anchor='s'), call(text='F', anchor='s'), call(text=''), call(text='G', anchor='s'),
            call(text=''), call(text='A', anchor='s'), call(text=''), call(text='B', anchor='s'),
            call(text='C', anchor='s'), call(text=''), call(text='D', anchor='s'), call(text=''),
            call(text='E', anchor='s'), call(text='F', anchor='s'), call(text=''), call(text='G', anchor='s'),
            call(text=''), call(text='A', anchor='s'), call(text=''), call(text='B', anchor='s'),
            call(text='C', anchor='s'), call(text=''), call(text='D', anchor='s'), call(text=''),
            call(text='E', anchor='s'), call(text='F', anchor='s'), call(text=''), call(text='G', anchor='s'),
            call(text=''), call(text='A', anchor='s'), call(text=''), call(text='B', anchor='s'),
            call(text='C', anchor='s')
        ])

    @patch.object(FileManager, 'edit_file')
    @patch.object(MemoSong, '_create_control_button')
    @patch.object(MemoSong, '_create_label', return_value=MagicMock())
    def test_add_update_file_frame(self, mock_create_label: MagicMock, mock_create_control_button: MagicMock,
                                   mock_file_manager_edit_file: MagicMock) -> None:
        mock_tkinter_frame = MagicMock()
        customtkinter.CTkFrame = MagicMock(return_value=mock_tkinter_frame)
        self.memo_song.add_update_file_frame(mock_tkinter_frame)
        mock_tkinter_frame.pack.assert_called_once_with(side='right')
        mock_create_label.assert_called_once_with(mock_tkinter_frame, 'EDIT FILE')
        # mock_create_control_button.assert_has_calls([
        #     call(mock_tkinter_frame, 'Rename', mock_lambda_function, width=70),
        #     call(mock_tkinter_frame, 'Delete', mock_lambda_function, width=70)
        # ])

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

    def test_setup_notepad(self) -> None:
        mock_tkinter_entry = MagicMock()
        customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
        mock_tkinter_textbox = MagicMock()
        customtkinter.CTkTextbox = MagicMock(return_value=mock_tkinter_textbox)
        self.memo_song._setup_notepad(MagicMock(), MagicMock())
        mock_tkinter_entry.pack.assert_called_once_with(side='left', fill='both', expand=1)
        mock_tkinter_textbox.pack.assert_called_once_with(side='bottom', fill='both', expand=1)
        self.assertEqual(FileManager.notepad_title_field, mock_tkinter_entry)
        self.assertEqual(FileManager.notepad_text_area, mock_tkinter_textbox)

    @patch.object(MemoSong, '_add_key_names')
    def test_create_piano_button(self, mock_add_key_names: MagicMock) -> None:
        self.memo_song._create_piano_button(MagicMock(), 'q', 0, 0, 0)
        mock_add_key_names.assert_called_once_with(self.mock_tkinter_button, 'q')
        self.assertEqual(getattr(GenericFunctions, 'q_key'), self.mock_tkinter_button)

    @patch.object(MemoSong, '_is_white_key', return_value=True)
    def test_add_key_names_white_key(self, mock_is_white_key: MagicMock) -> None:
        self.memo_song._add_key_names(self.mock_tkinter_button, 'q')
        mock_is_white_key.assert_called_once_with('q')
        self.mock_tkinter_button.configure.assert_called_once_with(text='C', text_color='black', anchor='s')

    @patch.object(MemoSong, '_is_white_key', return_value=False)
    def test_add_key_names_black_key(self, mock_is_white_key: MagicMock) -> None:
        self.memo_song._add_key_names(self.mock_tkinter_button, '2')
        mock_is_white_key.assert_called_once_with('2')
        self.mock_tkinter_button.configure.assert_not_called()

    @patch.object(pygame.mixer, 'init')
    def test_initialize_sound_mixer(self, mock_mixer_init: MagicMock) -> None:
        self.memo_song._initialize_sound_mixer()
        mock_mixer_init.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
