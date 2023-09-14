import unittest
import datetime
from mock import patch
from file_manager import FileManager
from test_memo_song_data import *


class TestFileManager(unittest.TestCase):
    def setUp(self) -> None:
        self.file_manager_cls = FileManager()

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, '_delete_file')
    @patch.object(FileManager, '_rename_file')
    @patch.object(FileManager, '_get_curselection_from_radiobutton_list', return_value='file')
    def test_edit_file_rename(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                              mock_rename_file: MagicMock, mock_delete_file: MagicMock,
                              mock_display_message_box: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls.edit_file('rename')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.file_manager_cls.recordings_radiobutton_list)
        mock_rename_file.assert_called_once_with('file')
        mock_delete_file.assert_not_called()
        mock_display_message_box.assert_not_called()

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, '_delete_file')
    @patch.object(FileManager, '_rename_file')
    @patch.object(FileManager, '_get_curselection_from_radiobutton_list', return_value='file')
    def test_edit_file_rename(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                              mock_rename_file: MagicMock, mock_delete_file: MagicMock,
                              mock_display_message_box: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls.edit_file('delete')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.file_manager_cls.recordings_radiobutton_list)
        mock_rename_file.assert_not_called()
        mock_delete_file.assert_called_once_with('file')
        mock_display_message_box.assert_not_called()

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, '_rename_file')
    @patch.object(FileManager, '_delete_file')
    @patch.object(FileManager, '_get_curselection_from_radiobutton_list', return_value='file')
    def test_edit_file_rename_no_browser_type(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                                       mock_rename_file: MagicMock, mock_delete_file: MagicMock,
                                       mock_display_message_box: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = None
        self.file_manager_cls.edit_file('rename')
        mock_get_curselection_from_radiobutton_list.assert_not_called()
        mock_rename_file.assert_not_called()
        mock_delete_file.assert_not_called()
        mock_display_message_box.assert_called_once_with('ERROR', 'Please, select a file to rename', False, 300)

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, '_rename_file')
    @patch.object(FileManager, '_delete_file')
    @patch.object(FileManager, '_get_curselection_from_radiobutton_list', return_value='file')
    def test_edit_file_delete_no_browser_type(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                                       mock_rename_file: MagicMock, mock_delete_file: MagicMock,
                                       mock_display_message_box: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = None
        self.file_manager_cls.edit_file('delete')
        mock_get_curselection_from_radiobutton_list.assert_not_called()
        mock_rename_file.assert_not_called()
        mock_delete_file.assert_not_called()
        mock_display_message_box.assert_called_once_with('ERROR', 'Please, select a file to delete', False, 300)

    # @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.add_item')
    # @patch('os.listdir')
    # @patch.object(FileManager, '_get_extension')
    # @patch.object(FileManager.recordings_radiobutton_list, 'clear_list')
    # def test_update_list(self, _,_2, _3, _4) -> None:
    #     mock_recordings_radiobutton_list = MagicMock(0)
    #     self.file_manager_cls.recordings_radiobutton_list = MagicMock(return_value=mock_recordings_radiobutton_list)
    #     self.file_manager_cls.update_list('recordings')
    #     _.assert_called_once_with()
    #     _2.assert_called_once_with()
    #     _3.assert_called_once_with()
    #     _4.assert_called_once_with()

    def test_create_radiobutton_list(self) -> None:
        pass

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(FileManager, 'update_list')
    @patch('os.rename')
    @patch.object(FileManager, '_mute_playback')
    def test_rename_file_recording(self, mock_mute_playback: MagicMock, mock_os_rename: MagicMock,
                                   mock_update_list: MagicMock,  mock_notepad_title_field: MagicMock,
                                   mock_display_message_box) -> None:
        mock_tkinter_input_dialog.get_input.return_value = 'new_name'
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._rename_file('file')
        mock_mute_playback.assert_called_once_with()
        mock_os_rename.assert_called_once_with(
            f'{self.file_manager_cls.app_path}/recordings/file',
            f'{self.file_manager_cls.app_path}/recordings/new_name.wav'
        )
        mock_update_list.assert_called_once_with('recordings')
        mock_notepad_title_field.delete.assert_not_called()
        mock_notepad_title_field.insert.assert_not_called()
        mock_display_message_box.assert_not_called()

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(FileManager, 'update_list')
    @patch('os.rename')
    @patch.object(FileManager, '_mute_playback')
    def test_rename_file_note(self, mock_mute_playback: MagicMock, mock_os_rename: MagicMock,
                              mock_update_list: MagicMock, mock_notepad_title_field: MagicMock,
                              mock_display_message_box) -> None:
        mock_tkinter_input_dialog.get_input.return_value = 'new_name'
        self.file_manager_cls._current_browser_type = 'notes'
        self.file_manager_cls._rename_file('file')
        mock_mute_playback.assert_not_called()
        mock_os_rename.assert_called_once_with(
            f'{self.file_manager_cls.app_path}/notes/file', f'{self.file_manager_cls.app_path}/notes/new_name.txt'
        )
        mock_update_list.assert_called_once_with('notes')
        mock_notepad_title_field.delete.assert_called_once_with(0, 'end')
        mock_notepad_title_field.insert.assert_called_once_with(0, 'new_name')
        mock_display_message_box.assert_not_called()

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(FileManager, 'update_list')
    @patch('os.rename', side_effect=OSError(os_error.format(f'{FileManager.app_path}/recordings/file',
                                                            f'{FileManager.app_path}/recordings/???')))
    @patch.object(FileManager, '_mute_playback')
    def test_rename_file_os_error(self, mock_mute_playback: MagicMock, mock_os_rename: MagicMock,
                                  mock_update_list: MagicMock, mock_notepad_title_field: MagicMock,
                                  mock_display_message_box) -> None:
        mock_tkinter_input_dialog.get_input.return_value = '???'
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._rename_file('file')
        mock_mute_playback.assert_called_once_with()
        mock_os_rename.assert_called_once_with(
            f'{self.file_manager_cls.app_path}/recordings/file', f'{self.file_manager_cls.app_path}/recordings/???.wav'
        )
        mock_update_list.assert_not_called()
        mock_notepad_title_field.delete.assert_not_called()
        mock_notepad_title_field.insert.assert_not_called()
        mock_display_message_box.assert_called_once_with('ERROR', incorrect_file_error, False, 300)

    @patch.object(FileManager, 'update_list')
    @patch.object(FileManager, '_remove_file')
    @patch.object(FileManager, '_mute_playback')
    @patch.object(FileManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    def test_delete_file_recording(self, mock_display_message_box: MagicMock, mock_mute_playback: MagicMock,
                                   mock_remove_file: MagicMock, mock_update_list: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._delete_file('file')
        mock_tkinter_messagebox.get = MagicMock(return_value='Yes')
        # mock_mute_playback.assert_called_once_with()
        mock_tkinter_messagebox.destroy.assert_called_once_with()
        # mock_remove_file.assert_called_once_with()
        # mock_update_list.assert_called_once_with()
        # mock_tkinter_textbox.delete.assert_called_once_with()
        # mock_tkinter_entry.delete.assert_called_once_with()
        # msg = self._display_message_box('DELETE FILE', f'Do you want to delete\n{file_to_delete}?', True)
        # if msg.get() == 'Yes':
        #     if self._current_browser_type == 'recordings':
        #         self._mute_playback()
        #     self._remove_file(file_to_delete)
        #     self.update_list(self._current_browser_type)
        #     if self._current_browser_type == 'notes':
        #         self.notepad_text_area.delete('1.0', tkinter.END)
        #         self.notepad_title_field.delete(0, tkinter.END)
        # else:
        #     msg.destroy()

    def test_delete_file_note(self) -> None:
        pass

    def test_delete_file_canceled(self) -> None:
        pass

    @patch('os.remove')
    def test_remove_file(self, mock_os_remove: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._remove_file('file')
        mock_os_remove.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings/file')

    @patch('os.remove', side_effect=file_not_found_error.format(f'{FileManager.app_path}/recordings/not_existent'))
    def test_remove_file_not_existent(self, mock_os_remove: MagicMock) -> None:
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._remove_file('not_existent')
        mock_os_remove.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings/not_existent')

    @patch.object(FileManager, '_create_directory')
    @patch.object(FileManager, '_directory_exists', return_value=True)
    def test_get_full_filename_recording(self, mock_directory_exists: MagicMock,
                                         mock_create_directory: MagicMock) -> None:
        filename = self.file_manager_cls._get_full_filename('file', 'recordings', 'piano_')
        mock_directory_exists.assert_called_once_with('recordings')
        mock_create_directory.assert_not_called()
        self.assertEqual(filename, 'file.wav')

    @patch.object(FileManager, '_create_directory')
    @patch.object(FileManager, '_directory_exists', return_value=True)
    def test_get_full_filename_note(self, mock_directory_exists: MagicMock, mock_create_directory: MagicMock) -> None:
        filename = self.file_manager_cls._get_full_filename('file', 'notes', '')
        mock_directory_exists.assert_called_once_with('notes')
        mock_create_directory.assert_not_called()
        self.assertEqual(filename, 'file.txt')

    @patch('datetime.datetime')
    @patch.object(FileManager, '_create_directory')
    @patch.object(FileManager, '_directory_exists', return_value=True)
    def test_get_full_filename_default_recording(self, mock_directory_exists: MagicMock,
                                                 mock_create_directory: MagicMock, mock_date: MagicMock) -> None:
        mock_date.now.return_value = datetime.datetime
        filename = self.file_manager_cls._get_full_filename('', 'recordings', 'piano_')
        mock_directory_exists.assert_called_once_with('recordings')
        mock_create_directory.assert_not_called()
        self.assertEqual(filename, f'piano_recording_{mock_date.strftime()}.wav')

    @patch('datetime.datetime')
    @patch.object(FileManager, '_create_directory')
    @patch.object(FileManager, '_directory_exists', return_value=True)
    def test_get_full_filename_default_note(self, mock_directory_exists: MagicMock, mock_create_directory: MagicMock,
                                            mock_date: MagicMock) -> None:
        mock_date.now.return_value = datetime.datetime
        filename = self.file_manager_cls._get_full_filename('', 'notes', '')
        mock_directory_exists.assert_called_once_with('notes')
        mock_create_directory.assert_not_called()
        self.assertEqual(filename, f'note_{mock_date.strftime()}.txt')

    @patch.object(FileManager, '_create_directory')
    @patch.object(FileManager, '_directory_exists', return_value=False)
    def test_get_full_filename_no_directory(self, mock_directory_exists: MagicMock,
                                            mock_create_directory: MagicMock) -> None:
        filename = self.file_manager_cls._get_full_filename('file', 'recordings', '')
        mock_directory_exists.assert_called_once_with('recordings')
        mock_create_directory.assert_called_once_with('recordings')
        self.assertEqual(filename, 'file.wav')

    @patch.object(FileManager, '_search')
    def test_search_recordings(self, mock_search: MagicMock) -> None:
        self.file_manager_cls.search_recordings()
        mock_search.assert_called_once_with('recordings')

    @patch.object(FileManager, '_search')
    def test_search_notes(self, mock_search: MagicMock) -> None:
        self.file_manager_cls.search_notes()
        mock_search.assert_called_once_with('notes')

    # def test_search(self) -> None:
    #     radiobutton_list = getattr(self, f'{browser_type}_radiobutton_list')
    #     search_field = getattr(self, f'{browser_type}_search_field')
    #     radiobutton_list.clear_list()
    #     searched_item = search_field.get()
    #     for file in os.listdir(f'{self.app_path}/{browser_type}'):
    #         if searched_item in file:
    #             radiobutton_list.add_item(file)

    def test_get_extension_recordings(self) -> None:
        extension = self.file_manager_cls._get_extension('recordings')
        self.assertEqual(extension, 'wav')

    def test_get_extension_notes(self) -> None:
        extension = self.file_manager_cls._get_extension('notes')
        self.assertEqual(extension, 'txt')