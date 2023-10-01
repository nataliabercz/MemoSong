import unittest
import pygame
from mock import patch
from generic_functions import GenericFunctions
from test_memo_song_data import *


class TestGenericFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.generic_functions_cls = GenericFunctions()

    @patch.object(customtkinter, 'set_default_color_theme')
    @patch.object(customtkinter, 'set_appearance_mode')
    def test_set_theme(self, mock_set_appearance_mode: MagicMock, mock_set_default_color_theme: MagicMock) -> None:
        self.generic_functions_cls._set_theme()
        mock_set_appearance_mode.assert_called_once_with('dark')
        mock_set_default_color_theme.assert_called_once_with(f'{self.generic_functions_cls.app_path}/data/theme.json')
        self.assertEqual(customtkinter.get_appearance_mode(), 'Dark')

    @patch.object(GenericFunctions, '_is_white_key', return_value=True)
    def test_add_key_names_white_key(self, mock_is_white_key: MagicMock) -> None:
        self.generic_functions_cls._add_key_names(mock_tkinter_button, 'q')
        mock_is_white_key.assert_called_once_with('q')
        mock_tkinter_button.configure.assert_called_once_with(text='C', text_color='black', anchor='s')

    @patch.object(GenericFunctions, '_is_white_key', return_value=False)
    def test_add_key_names_black_key(self, mock_is_white_key: MagicMock) -> None:
        self.generic_functions_cls._add_key_names(mock_tkinter_button, '2')
        mock_is_white_key.assert_called_once_with('2')
        mock_tkinter_button.configure.assert_not_called()

    def test_is_white_key_true(self) -> None:
        key = self.generic_functions_cls._is_white_key('q')
        self.assertEqual(key, True)

    def test_is_white_key_false(self) -> None:
        key = self.generic_functions_cls._is_white_key('2')
        self.assertEqual(key, False)

    @patch.object(GenericFunctions, '_is_white_key', side_effect=is_white_key)
    @patch.object(GenericFunctions, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_add_keyboard_text(self, mock_get_button_from_key: MagicMock, mock_is_white_key: MagicMock) -> None:
        self.generic_functions_cls._add_keyboard_text()
        mock_is_white_key.assert_has_calls(calls_each_key)
        mock_get_button_from_key.assert_has_calls(calls_each_key)
        mock_tkinter_button.configure.assert_has_calls(calls_add_keyboard_text)

    @patch.object(GenericFunctions, '_is_white_key', side_effect=is_white_key)
    @patch.object(GenericFunctions, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_keyboard_text(self, mock_get_button_from_key: MagicMock, mock_is_white_key: MagicMock) -> None:
        self.generic_functions_cls._remove_keyboard_text()
        mock_is_white_key.assert_has_calls(calls_each_key)
        mock_get_button_from_key.assert_has_calls(calls_each_key)
        mock_tkinter_button.configure.assert_has_calls(calls_remove_keyboard_text)

    def test_get_button_from_key(self) -> None:
        self.generic_functions_cls.q_key = mock_tkinter_button
        button = self.generic_functions_cls._get_button_from_key('q')
        self.assertEqual(button, getattr(self.generic_functions_cls, 'q_key'))

    @patch('PIL.Image.open')
    def test_open_image(self, mock_pil_image_open: MagicMock) -> None:
        self.generic_functions_cls.keyboard_image = MagicMock()
        image = self.generic_functions_cls._open_image('keyboard_image', (45, 25))
        mock_pil_image_open.assert_called_once_with(self.generic_functions_cls.keyboard_image)
        self.assertEqual(image, mock_tkinter_image)

    @patch.object(GenericFunctions, '_set_image_name')
    def test_load_image_names(self, mock_set_image_name: MagicMock) -> None:
        self.generic_functions_cls._load_image_names()
        mock_set_image_name.assert_has_calls(calls_load_image_names)

    def test_set_image_name(self) -> None:
        self.generic_functions_cls._set_image_name('keyboard')
        self.assertEqual(getattr(self.generic_functions_cls, f'keyboard_image'),
                         f'{self.generic_functions_cls.images_path}/keyboard.png')

    @patch.object(pygame.mixer, 'init')
    def test_initialize_sound_mixer(self, mock_mixer_init: MagicMock) -> None:
        self.generic_functions_cls._initialize_sound_mixer()
        mock_mixer_init.assert_called_once_with()

    @patch.object(GenericFunctions, '_initialize_sound_mixer')
    @patch.object(pygame.mixer, 'quit')
    def test_mute_playback(self, mock_mixer_quit: MagicMock, mock_initialize_sound_mixer: MagicMock) -> None:
        self.generic_functions_cls._mute_playback()
        mock_mixer_quit.assert_called_once_with()
        mock_initialize_sound_mixer.assert_called_once_with()

    @patch('threading.Thread')
    def test_start_new_thread(self, mock_threading: MagicMock) -> None:
        mock_target = MagicMock()
        self.generic_functions_cls._start_new_thread(mock_target)
        mock_threading.assert_called_once_with(target=mock_target)

    def test_highlight_button_on(self) -> None:
        mock_tkinter_button.reset_mock()
        self.generic_functions_cls.keyboard_button = mock_tkinter_button
        self.generic_functions_cls._highlight_button('keyboard', 'on')
        mock_tkinter_button.configure.assert_called_once_with(border_width=1)

    def test_highlight_button_off(self) -> None:
        mock_tkinter_button.reset_mock()
        self.generic_functions_cls.keyboard_button = mock_tkinter_button
        self.generic_functions_cls._highlight_button('keyboard', 'off')
        mock_tkinter_button.configure.assert_called_once_with(border_width=0)

    @patch.object(GenericFunctions, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_highlight_piano_key(self, mock_get_button_from_key: MagicMock) -> None:
        mock_tkinter_button.reset_mock()
        self.generic_functions_cls._highlight_piano_key('q')
        mock_get_button_from_key.assert_called_once_with('q')
        mock_tkinter_button.configure.assert_called_once_with(fg_color=['#325882', '#14375e'])

    @patch.object(GenericFunctions, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_piano_key_highlight_white_key(self, mock_get_button_from_key: MagicMock) -> None:
        mock_tkinter_button.reset_mock()
        self.generic_functions_cls._remove_piano_key_highlight('q')
        mock_get_button_from_key.assert_called_once_with('q')
        mock_tkinter_button.configure.assert_called_once_with(fg_color='white')

    @patch.object(GenericFunctions, '_get_button_from_key', return_value=mock_tkinter_button)
    def test_remove_piano_key_highlight_black_key(self, mock_get_button_from_key: MagicMock) -> None:
        mock_tkinter_button.reset_mock()
        self.generic_functions_cls._remove_piano_key_highlight('2')
        mock_get_button_from_key.assert_called_once_with('2')
        mock_tkinter_button.configure.assert_called_once_with(fg_color='black')

    @patch.object(GenericFunctions, '_list_files', return_value=['file1', 'file2'])
    def test_filename_exists_true(self, mock_list_files: MagicMock) -> None:
        filename_exists = self.generic_functions_cls._filename_exists('recordings', 'file1')
        mock_list_files.assert_called_once_with(f'{self.generic_functions_cls.app_path}/recordings')
        self.assertEqual(filename_exists, True)

    @patch.object(GenericFunctions, '_list_files', return_value=['file1'])
    def test_filename_exists_true(self, mock_list_files: MagicMock) -> None:
        filename_exists = self.generic_functions_cls._filename_exists('notes', 'file2')
        mock_list_files.assert_called_once_with(f'{self.generic_functions_cls.app_path}/notes')
        self.assertEqual(filename_exists, False)

    @patch('os.path.isdir', return_value=True)
    @patch.object(GenericFunctions, '_list_files', return_value=['recordings', 'notes'])
    def test_directory_exists_true(self, mock_list_files: MagicMock, mock_path_is_dir: MagicMock) -> None:
        directory_exists = self.generic_functions_cls._directory_exists('recordings')
        mock_list_files.assert_called_once_with(f'{self.generic_functions_cls.app_path}')
        mock_path_is_dir.assert_called_once_with(f'{self.generic_functions_cls.app_path}/recordings')
        self.assertEqual(directory_exists, True)

    @patch('os.path.isdir', return_value=True)
    @patch.object(GenericFunctions, '_list_files', return_value=['recordings'])
    def test_directory_exists_false(self, mock_list_files: MagicMock, mock_path_is_dir: MagicMock) -> None:
        directory_exists = self.generic_functions_cls._directory_exists('notes')
        mock_list_files.assert_called_once_with(f'{self.generic_functions_cls.app_path}')
        mock_path_is_dir.assert_not_called()
        self.assertEqual(directory_exists, False)

    @patch('os.path.isdir', return_value=False)
    @patch.object(GenericFunctions, '_list_files', return_value=['recordings', 'notes'])
    def test_directory_exists_not_directory(self, mock_list_files: MagicMock, mock_path_is_dir: MagicMock) -> None:
        directory_exists = self.generic_functions_cls._directory_exists('recordings')
        mock_list_files.assert_called_once_with(f'{self.generic_functions_cls.app_path}')
        mock_path_is_dir.assert_called_once_with(f'{self.generic_functions_cls.app_path}/recordings')
        self.assertEqual(directory_exists, False)

    @patch.object(GenericFunctions, '_display_message_box')
    @patch.object(GenericFunctions, '_list_files', return_value=['file1', 'file2'])
    def test_list_files(self, mock_list_files: MagicMock, mock_display_message_box: MagicMock) -> None:
        files = self.generic_functions_cls._list_files('recordings')
        mock_list_files.assert_called_once_with('recordings')
        mock_display_message_box.assert_not_called()
        self.assertEqual(files, ['file1', 'file2'])

    @patch.object(GenericFunctions, '_display_message_box')
    @patch.object(GenericFunctions, '_list_files', return_value=[])
    def test_list_files_empty(self, mock_list_files: MagicMock, mock_display_message_box: MagicMock) -> None:
        files = self.generic_functions_cls._list_files('recordings')
        mock_list_files.assert_called_once_with('recordings')
        mock_display_message_box.assert_not_called()
        self.assertEqual(files, [])

    @patch.object(GenericFunctions, '_display_message_box')
    @patch('os.listdir', side_effect=OSError(os_error_list.format('???')))
    def test_list_files_os_error(self, mock_list_files: MagicMock, mock_display_message_box: MagicMock) -> None:
        self.generic_functions_cls._list_files('???')
        mock_list_files.assert_called_once_with('???')
        mock_display_message_box.assert_called_once_with('ERROR', os_error_msg, False, 300)

    @patch.object(GenericFunctions, '_display_message_box')
    @patch('os.listdir', side_effect=FileNotFoundError(
        file_not_found_error_list.format(f'{GenericFunctions.app_path}/recordings/not_existent')))
    def test_list_files_error_2(self, mock_list_files: MagicMock, mock_display_message_box: MagicMock) -> None:
        self.generic_functions_cls._list_files('not_existent')
        mock_list_files.assert_called_once_with('not_existent')
        mock_display_message_box.assert_called_once_with('ERROR', file_not_found_error_msg, False, 300)

    @patch('os.mkdir')
    def test_create_directory(self, mock_mkdir: MagicMock()) -> None:
        self.generic_functions_cls._create_directory('recordings')
        mock_mkdir.assert_called_once_with(f'{self.generic_functions_cls.app_path}/recordings')

    @patch('file_manager.FileManager.recordings_radiobutton_list')
    def test_get_curselection_from_radiobutton_list(self, mock_recordings_radiobutton_list: MagicMock) -> None:
        mock_recordings_radiobutton_list.get_selected_item = MagicMock()
        selected_item = self.generic_functions_cls._get_curselection_from_radiobutton_list(
            mock_recordings_radiobutton_list)
        mock_recordings_radiobutton_list.get_selected_item.assert_called_once_with()
        self.assertEqual(selected_item, mock_recordings_radiobutton_list.get_selected_item())

    @patch('file_manager.FileManager.recordings_radiobutton_list')
    def test_remove_selection_from_radiobutton_list(self, mock_recordings_radiobutton_list: MagicMock) -> None:
        mock_recordings_radiobutton_list.remove_item_selection = MagicMock()
        self.generic_functions_cls._remove_selection_from_radiobutton_list(mock_recordings_radiobutton_list)
        mock_recordings_radiobutton_list.remove_item_selection.assert_called_once_with()

    @patch.object(GenericFunctions, '_open_image', return_value=mock_tkinter_image)
    def test_create_button_from_image(self, mock_open_image: MagicMock) -> None:
        self.generic_functions_cls._create_button_from_image(MagicMock(), 'keyboard', (45, 25), 'command', tkinter.LEFT,
                                                             self.generic_functions_cls)
        mock_open_image.assert_called_once_with('keyboard_image', (45, 25))
        mock_tkinter_button.pack.assert_called_once_with(side='left')
        self.assertEqual(getattr(self.generic_functions_cls, 'keyboard_button'), mock_tkinter_button)

    def test_create_control_button(self) -> None:
        mock_tkinter_button.reset_mock()
        self.generic_functions_cls._create_control_button(MagicMock(), 'Search', 'command', tkinter.LEFT)
        mock_tkinter_button.pack.assert_called_once_with(side='left', fill='both')

    def test_create_label(self) -> None:
        mock_tkinter_label.reset_mock()
        self.generic_functions_cls._create_label(MagicMock(), text='text')
        mock_tkinter_label.pack.assert_called_once_with()

    def test_create_label_kwargs(self) -> None:
        mock_tkinter_label.reset_mock()
        self.generic_functions_cls._create_label(MagicMock(), text='', pady=20, side=tkinter.TOP)
        mock_tkinter_label.pack.assert_called_once_with(pady=20, side='top')

    @patch.object(GenericFunctions, '_open_image', return_value='image')
    def test_create_label_image(self, mock_open_image: MagicMock) -> None:
        mock_tkinter_label.reset_mock()
        self.generic_functions_cls._create_label(MagicMock(), text='', image=mock_open_image)
        mock_tkinter_label.pack.assert_called_once_with()

    def test_display_message_box(self) -> None:
        message_box = self.generic_functions_cls._display_message_box('ERROR', f'Invalid file!', False, 300)
        self.assertEqual(message_box, mock_tkinter_messagebox)
