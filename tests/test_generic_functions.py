import unittest
import pygame
from mock import patch
from memo_song import MemoSong
from test_memo_song_data import *


class TestMemoSong(unittest.TestCase):
    def setUp(self) -> None:
        self.root = customtkinter.CTk()
        self.memo_song = MemoSong(self.root)

    def tearDown(self) -> None:
        if self.root:
            self.root.destroy()

    @patch.object(customtkinter, 'set_default_color_theme')
    @patch.object(customtkinter, 'set_appearance_mode')
    def test_set_theme(self, mock_set_appearance_mode: MagicMock, mock_set_default_color_theme: MagicMock) -> None:
        self.memo_song._set_theme()
        mock_set_appearance_mode.assert_called_once_with('dark')
        mock_set_default_color_theme.assert_called_once_with(f'{self.memo_song.app_path}/data/theme.json')
        self.assertEqual(customtkinter.get_appearance_mode(), 'Dark')

    @patch.object(MemoSong, '_is_white_key', return_value=True)
    def test_add_key_names_white_key(self, mock_is_white_key: MagicMock) -> None:
        self.memo_song._add_key_names(mock_tkinter_button, 'q')
        mock_is_white_key.assert_called_once_with('q')
        mock_tkinter_button.configure.assert_called_once_with(text='C', text_color='black', anchor='s')

    @patch.object(MemoSong, '_is_white_key', return_value=False)
    def test_add_key_names_black_key(self, mock_is_white_key: MagicMock) -> None:
        self.memo_song._add_key_names(mock_tkinter_button, '2')
        mock_is_white_key.assert_called_once_with('2')
        mock_tkinter_button.configure.assert_not_called()

    def test_is_white_key_true(self) -> None:
        key = self.memo_song._is_white_key('q')
        self.assertEqual(key, True)

    def test_is_white_key_false(self) -> None:
        key = self.memo_song._is_white_key('2')
        self.assertEqual(key, False)

    @patch.object(MemoSong, '_is_white_key', side_effect=is_white_key)
    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_add_keyboard_text(self, mock_get_button_from_key: MagicMock, mock_is_white_key: MagicMock) -> None:
        self.memo_song._add_keyboard_text()
        mock_is_white_key.assert_has_calls(calls_each_key)
        mock_get_button_from_key.assert_has_calls(calls_each_key)
        mock_tkinter_button.configure.assert_has_calls(calls_add_keyboard_text)

    @patch.object(MemoSong, '_is_white_key', side_effect=is_white_key)
    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_keyboard_text(self, mock_get_button_from_key: MagicMock, mock_is_white_key: MagicMock) -> None:
        self.memo_song._remove_keyboard_text()
        mock_is_white_key.assert_has_calls(calls_each_key)
        mock_get_button_from_key.assert_has_calls(calls_each_key)
        mock_tkinter_button.configure.assert_has_calls(calls_remove_keyboard_text)

    def test_get_button_from_key(self) -> None:
        self.memo_song.q_key = mock_tkinter_button
        button = self.memo_song._get_button_from_key('q')
        self.assertEqual(button, getattr(self.memo_song, 'q_key'))

    def test_open_image(self) -> None:
        # mock_image = MagicMock()
        # self.memo_song.keyboard_image = MagicMock(return_value=mock_image)
        # Image.open = MagicMock(return_value=mock_image)
        # image = self.memo_song._open_image('keyboard_image')
        # self.assertEqual(image, mock_image)
        pass

    @patch.object(MemoSong, '_set_image_name')
    def test_load_image_names(self, mock_set_image_name: MagicMock) -> None:
        self.memo_song._load_image_names()
        mock_set_image_name.assert_has_calls(calls_load_image_names)

    def test_set_image_name(self) -> None:
        self.memo_song._set_image_name('keyboard')
        self.assertEqual(getattr(self.memo_song, f'keyboard_image'), f'{self.memo_song.images_path}/keyboard.png')

    @patch.object(pygame.mixer, 'init')
    def test_initialize_sound_mixer(self, mock_mixer_init: MagicMock) -> None:
        self.memo_song._initialize_sound_mixer()
        mock_mixer_init.assert_called_once_with()

    @patch.object(MemoSong, '_initialize_sound_mixer')
    @patch.object(pygame.mixer, 'quit')
    def test_mute_playback(self, mock_mixer_quit: MagicMock, mock_initialize_sound_mixer: MagicMock) -> None:
        self.memo_song._mute_playback()
        mock_mixer_quit.assert_called_once_with()
        mock_initialize_sound_mixer.assert_called_once_with()

    @patch('threading.Thread')
    def test_start_new_thread(self, mock_threading: MagicMock) -> None:
        mock_target = MagicMock()
        self.memo_song._start_new_thread(mock_target)
        mock_threading.assert_called_once_with(target=mock_target)

    def test_highlight_used_function_on(self) -> None:
        mock_tkinter_button.reset_mock()
        self.memo_song.keyboard_button = mock_tkinter_button
        self.memo_song._highlight_used_function('keyboard', 'on')
        mock_tkinter_button.configure.assert_called_once_with(border_width=1)

    def test_highlight_used_function_off(self) -> None:
        mock_tkinter_button.reset_mock()
        self.memo_song.keyboard_button = mock_tkinter_button
        self.memo_song._highlight_used_function('keyboard', 'off')
        mock_tkinter_button.configure.assert_called_once_with(border_width=0)

    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_highlight_button(self, mock_get_button_from_key: MagicMock) -> None:
        mock_tkinter_button.reset_mock()
        self.memo_song._highlight_button('q')
        mock_get_button_from_key.assert_called_once_with('q')
        mock_tkinter_button.configure.assert_called_once_with(fg_color=['#325882', '#14375e'])

    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_button_highlight_white_key(self, mock_get_button_from_key: MagicMock) -> None:
        mock_tkinter_button.reset_mock()
        self.memo_song._remove_button_highlight('q')
        mock_get_button_from_key.assert_called_once_with('q')
        mock_tkinter_button.configure.assert_called_once_with(fg_color='white')

    @patch.object(MemoSong, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_button_highlight_black_key(self, mock_get_button_from_key: MagicMock) -> None:
        mock_tkinter_button.reset_mock()
        self.memo_song._remove_button_highlight('2')
        mock_get_button_from_key.assert_called_once_with('2')
        mock_tkinter_button.configure.assert_called_once_with(fg_color='black')

    @patch('os.listdir', return_value=['piano_recording', 'my_note'])
    def test_filename_exists_true(self, mock_list_dir: MagicMock) -> None:
        filename_exists = self.memo_song._filename_exists('recordings', 'piano_recording')
        mock_list_dir.assert_called_once_with(f'{self.memo_song.app_path}/recordings')
        self.assertEqual(filename_exists, True)

    @patch('os.listdir', return_value=['piano_recording'])
    def test_filename_exists_true(self, mock_list_dir: MagicMock) -> None:
        filename_exists = self.memo_song._filename_exists('notes', 'my_note')
        mock_list_dir.assert_called_once_with(f'{self.memo_song.app_path}/notes')
        self.assertEqual(filename_exists, False)

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir', return_value=['recordings', 'notes'])
    def test_directory_exists_true(self, mock_list_dir: MagicMock, mock_path_is_dir: MagicMock) -> None:
        directory_exists = self.memo_song._directory_exists('recordings')
        mock_list_dir.assert_called_once_with(f'{self.memo_song.app_path}')
        mock_path_is_dir.assert_called_once_with(f'{self.memo_song.app_path}/recordings')
        self.assertEqual(directory_exists, True)

    @patch('os.path.isdir', return_value=True)
    @patch('os.listdir', return_value=['recordings'])
    def test_directory_exists_false(self, mock_list_dir: MagicMock, mock_path_is_dir: MagicMock) -> None:
        directory_exists = self.memo_song._directory_exists('notes')
        mock_list_dir.assert_called_once_with(f'{self.memo_song.app_path}')
        mock_path_is_dir.assert_not_called()
        self.assertEqual(directory_exists, False)

    @patch('os.path.isdir', return_value=False)
    @patch('os.listdir', return_value=['recordings', 'notes'])
    def test_directory_exists_not_directory(self, mock_list_dir: MagicMock, mock_path_is_dir: MagicMock) -> None:
        directory_exists = self.memo_song._directory_exists('recordings')
        mock_list_dir.assert_called_once_with(f'{self.memo_song.app_path}')
        mock_path_is_dir.assert_called_once_with(f'{self.memo_song.app_path}/recordings')
        self.assertEqual(directory_exists, False)

    @patch('os.mkdir')
    def test_create_directory(self, mock_mkdir: MagicMock()) -> None:
        self.memo_song._create_directory('recordings')
        mock_mkdir.assert_called_once_with(f'{self.memo_song.app_path}/recordings')

    def test_get_curselection_from_radiobutton_list(self) -> None:
        # radiobutton_list = []
        # curselection = self.memo_song._get_curselection_from_radiobutton_list(radiobutton_list)
        # self.memo_song.file_manager.
        # # return radiobutton_list.get_selected_item()
        pass

    def _remove_selection_from_radiobutton_list(self) -> None:
        # radiobutton_list.remove_item_selection()
        pass

    @patch.object(MemoSong, '_open_image', return_value=mock_tkinter_image)
    def test_create_button_from_image(self, mock_open_image: MagicMock) -> None:
        self.memo_song._create_button_from_image(MagicMock(), 'keyboard', (45, 25),
                                                 self.memo_song._turn_keyboard_piano, tkinter.LEFT, self.memo_song)
        mock_open_image.assert_called_once_with('keyboard_image', (45, 25))
        mock_tkinter_button.pack.assert_called_once_with(side='left')
        self.assertEqual(getattr(self.memo_song, 'keyboard_button'), mock_tkinter_button)

    def test_create_control_button(self) -> None:
        self.memo_song._create_control_button(MagicMock(), 'Search', self.memo_song.file_manager._search, tkinter.LEFT)
        # mock_tkinter_button.reset_mock()
        # mock_tkinter_button.configure.assert_called_once_with(side='left', fill='both')

    def test_create_label(self) -> None:
        mock_tkinter_label.reset_mock()
        self.memo_song._create_label(MagicMock(), text='text')
        mock_tkinter_label.pack.assert_called_once_with()

    def test_create_label_kwargs(self) -> None:
        mock_tkinter_label.reset_mock()
        self.memo_song._create_label(MagicMock(), text='', pady=20, side=tkinter.TOP)
        mock_tkinter_label.pack.assert_called_once_with(pady=20, side='top')

    @patch.object(MemoSong, '_open_image', return_value='image')
    def test_create_label_image(self, mock_open_image: MagicMock) -> None:
        mock_tkinter_label.reset_mock()
        self.memo_song._create_label(MagicMock(), text='', image=mock_open_image)
        mock_tkinter_label.pack.assert_called_once_with()

    def test_display_message_box(self) -> None:
        message_box = self.memo_song._display_message_box('ERROR', f'Invalid file!', False, 300)
        self.assertEqual(message_box, mock_tkinter_messagebox)


if __name__ == '__main__':
    unittest.main()
