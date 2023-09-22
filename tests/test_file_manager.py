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

    @patch.object(FileManager, '_list_files', return_value=['file.wav', 'file.txt'])
    @patch.object(FileManager, '_get_extension', return_value='wav')
    def test_update_list(self, mock_get_extension: MagicMock, mock_list_files: MagicMock) -> None:
        self.file_manager_cls.recordings_radiobutton_list = MagicMock()
        self.file_manager_cls.recordings_radiobutton_list.clear_list = MagicMock()
        self.file_manager_cls.recordings_radiobutton_list.add_item = MagicMock()
        self.file_manager_cls.update_list('recordings')
        self.file_manager_cls.recordings_radiobutton_list.clear_list.assert_called_once_with()
        mock_get_extension.assert_called_once_with('recordings')
        mock_list_files.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings')
        self.file_manager_cls.recordings_radiobutton_list.add_item.assert_called_once_with('file.wav')

    @patch.object(FileManager, '_list_files', return_value=[])
    @patch.object(FileManager, '_get_extension', return_value='txt')
    def test_update_list_empty(self, mock_get_extension: MagicMock, mock_list_files: MagicMock) -> None:
        self.file_manager_cls.notes_radiobutton_list = MagicMock()
        self.file_manager_cls.notes_radiobutton_list.clear_list = MagicMock()
        self.file_manager_cls.notes_radiobutton_list.add_item = MagicMock()
        self.file_manager_cls.update_list('notes')
        self.file_manager_cls.notes_radiobutton_list.clear_list.assert_called_once_with()
        mock_get_extension.assert_called_once_with('notes')
        mock_list_files.assert_called_once_with(f'{self.file_manager_cls.app_path}/notes')
        self.file_manager_cls.notes_radiobutton_list.add_item.assert_not_called()

    @patch.object(FileManager, '_create_radiobutton_list', return_value=mock_scrollable_radiobutton_frame)
    @patch.object(FileManager, '_get_extension', return_value='wav')
    @patch.object(FileManager, '_list_files', return_value=['file1.wav', 'file2.wav'])
    @patch.object(FileManager, '_create_directory')
    @patch.object(FileManager, '_directory_exists', return_value=True)
    def test_create_and_get_radiobutton_list(self, mock_directory_exists: MagicMock, mock_create_directory: MagicMock,
                                             mock_list_files: MagicMock, mock_get_extension: MagicMock,
                                             mock_create_radiobutton_list: MagicMock) -> None:
        radiobutton_list = self.file_manager_cls.create_and_get_radiobutton_list(mock_tkinter_frame, 'recordings',
                                                                                 'command')
        mock_directory_exists.assert_called_once_with('recordings')
        mock_create_directory.assert_not_called()
        mock_list_files.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings')
        mock_get_extension.assert_has_calls([call('recordings'), call('recordings')])
        mock_create_radiobutton_list.assert_called_once_with(mock_tkinter_frame, ['file1.wav', 'file2.wav'],
                                                             'recordings', command='command')
        mock_scrollable_radiobutton_frame.bind.assert_called_once_with('<<ListboxSelect>>', 'command')
        mock_scrollable_radiobutton_frame.pack.assert_called_once_with(fill='both')
        self.assertEqual(radiobutton_list, mock_scrollable_radiobutton_frame)

    @patch.object(FileManager, '_display_message_box')
    @patch.object(FileManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(FileManager, 'update_list')
    @patch('os.rename')
    @patch.object(FileManager, '_mute_playback')
    def test_rename_file_recording(self, mock_mute_playback: MagicMock, mock_os_rename: MagicMock,
                                   mock_update_list: MagicMock, mock_notepad_title_field: MagicMock,
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

    @patch.object(FileManager, 'clear_notepad')
    @patch.object(FileManager, 'update_list')
    @patch.object(FileManager, '_remove_file')
    @patch.object(FileManager, '_mute_playback')
    @patch.object(FileManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    def test_delete_file_recording(self, mock_display_message_box: MagicMock, mock_mute_playback: MagicMock,
                                   mock_remove_file: MagicMock, mock_update_list: MagicMock,
                                   mock_clear_notepad: MagicMock) -> None:
        mock_tkinter_messagebox.reset_mock()
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._delete_file('file')
        mock_display_message_box.assert_called_once_with('DELETE FILE', 'Do you want to delete\nfile?', True)
        mock_mute_playback.assert_called_once_with()
        mock_remove_file.assert_called_once_with('file')
        mock_update_list.assert_called_once_with('recordings')
        mock_clear_notepad.assert_not_called()
        mock_tkinter_messagebox.destroy.assert_not_called()

    @patch.object(FileManager, 'clear_notepad')
    @patch.object(FileManager, 'update_list')
    @patch.object(FileManager, '_remove_file')
    @patch.object(FileManager, '_mute_playback')
    @patch.object(FileManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    def test_delete_file_note(self, mock_display_message_box: MagicMock, mock_mute_playback: MagicMock,
                              mock_remove_file: MagicMock, mock_update_list: MagicMock,
                              mock_clear_notepad: MagicMock) -> None:
        mock_tkinter_messagebox.reset_mock()
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.file_manager_cls._current_browser_type = 'notes'
        self.file_manager_cls._delete_file('file')
        mock_display_message_box.assert_called_once_with('DELETE FILE', 'Do you want to delete\nfile?', True)
        mock_mute_playback.assert_not_called()
        mock_remove_file.assert_called_once_with('file')
        mock_update_list.assert_called_once_with('notes')
        mock_clear_notepad.assert_called_once_with()
        mock_tkinter_messagebox.destroy.assert_not_called()

    @patch.object(FileManager, 'clear_notepad')
    @patch.object(FileManager, 'update_list')
    @patch.object(FileManager, '_remove_file')
    @patch.object(FileManager, '_mute_playback')
    @patch.object(FileManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    def test_delete_file_cancelled(self, mock_display_message_box: MagicMock, mock_mute_playback: MagicMock,
                                   mock_remove_file: MagicMock, mock_update_list: MagicMock,
                                   mock_clear_notepad: MagicMock) -> None:
        mock_tkinter_messagebox.get.return_value = 'No'
        self.file_manager_cls._current_browser_type = 'recordings'
        self.file_manager_cls._delete_file('file')
        mock_display_message_box.assert_called_once_with('DELETE FILE', 'Do you want to delete\nfile?', True)
        mock_mute_playback.assert_not_called()
        mock_remove_file.assert_not_called()
        mock_update_list.assert_not_called()
        mock_clear_notepad.assert_not_called()
        mock_tkinter_messagebox.destroy.assert_called_once_with()

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

    @patch.object(FileManager, 'notepad_text_area', return_value=mock_tkinter_textbox)
    @patch.object(FileManager, 'notepad_title_field', return_value=mock_tkinter_entry)
    def test_clear_notepad(self, mock_notepad_title_field: MagicMock, mock_notepad_text_area: MagicMock) -> None:
        mock_notepad_title_field.delete = MagicMock()
        mock_notepad_text_area.delete = MagicMock()
        self.file_manager_cls.clear_notepad()
        mock_notepad_title_field.delete.assert_called_once_with(0, 'end')
        mock_notepad_text_area.delete.assert_called_once_with('1.0', 'end')

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

    @patch.object(FileManager, '_list_files', return_value=['file1', 'file2'])
    @patch.object(FileManager, 'recordings_radiobutton_list', return_value=not_empty_radiobutton_list)
    def test_search_whole_name(self, mock_recordings_radiobutton_list: MagicMock, mock_list_files: MagicMock) -> None:
        mock_recordings_radiobutton_list.clear_list = MagicMock()
        self.file_manager_cls.recordings_search_field = MagicMock()
        self.file_manager_cls.recordings_search_field.get = MagicMock(return_value='file1')
        self.file_manager_cls._search('recordings')
        mock_recordings_radiobutton_list.clear_list.assert_called_once_with()
        self.file_manager_cls.recordings_search_field.get.assert_called_once_with()
        mock_list_files.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings')
        mock_recordings_radiobutton_list.add_item.assert_called_once_with('file1')

    @patch.object(FileManager, '_list_files', return_value=['file1', 'file2', 'some_recording'])
    @patch.object(FileManager, 'recordings_radiobutton_list', return_value=not_empty_radiobutton_list)
    def test_search_regex(self, mock_recordings_radiobutton_list: MagicMock, mock_list_files: MagicMock) -> None:
        mock_recordings_radiobutton_list.clear_list = MagicMock()
        self.file_manager_cls.recordings_search_field = MagicMock()
        self.file_manager_cls.recordings_search_field.get = MagicMock(return_value='l')
        self.file_manager_cls._search('recordings')
        mock_recordings_radiobutton_list.clear_list.assert_called_once_with()
        self.file_manager_cls.recordings_search_field.get.assert_called_once_with()
        mock_list_files.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings')
        mock_recordings_radiobutton_list.add_item.assert_has_calls([call('file1'), call('file2')])

    @patch.object(FileManager, '_list_files', return_value=['file1', 'file2'])
    @patch.object(FileManager, 'recordings_radiobutton_list', return_value=not_empty_radiobutton_list)
    def test_search_not_found(self, mock_recordings_radiobutton_list: MagicMock, mock_list_files: MagicMock) -> None:
        mock_recordings_radiobutton_list.clear_list = MagicMock()
        self.file_manager_cls.recordings_search_field = MagicMock()
        self.file_manager_cls.recordings_search_field.get = MagicMock(return_value='file3')
        self.file_manager_cls._search('recordings')
        mock_recordings_radiobutton_list.clear_list.assert_called_once_with()
        self.file_manager_cls.recordings_search_field.get.assert_called_once_with()
        mock_list_files.assert_called_once_with(f'{self.file_manager_cls.app_path}/recordings')
        mock_recordings_radiobutton_list.add_item.assert_not_called()

    def test_get_extension_recordings(self) -> None:
        extension = self.file_manager_cls._get_extension('recordings')
        self.assertEqual(extension, 'wav')

    def test_get_extension_notes(self) -> None:
        extension = self.file_manager_cls._get_extension('notes')
        self.assertEqual(extension, 'txt')
