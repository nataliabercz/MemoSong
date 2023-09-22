import unittest
import io
from mock import patch
from note_manager import NoteManager
from test_memo_song_data import *


class TestNoteManager(unittest.TestCase):
    def setUp(self) -> None:
        self.note_manager_cls = NoteManager()

    @patch.object(NoteManager, '_display_message_box')
    @patch.object(NoteManager, '_open_note')
    @patch.object(NoteManager, 'clear_notepad')
    @patch.object(NoteManager, '_remove_selection_from_radiobutton_list')
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value='note')
    def test_open_note(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                       mock_remove_selection_from_radiobutton_list: MagicMock, mock_clear_notepad: MagicMock,
                       mock_open_note: MagicMock, mock_display_message_box: MagicMock) -> None:
        self.note_manager_cls.open_note()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.notes_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.recordings_radiobutton_list)
        mock_clear_notepad.assert_called_once_with()
        mock_open_note.assert_called_once_with('note')
        mock_display_message_box.assert_not_called()

    @patch.object(NoteManager, '_display_message_box')
    @patch.object(NoteManager, '_open_note')
    @patch.object(NoteManager, 'clear_notepad')
    @patch.object(NoteManager, '_remove_selection_from_radiobutton_list')
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value=None)
    def test_open_note_no_note(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                               mock_remove_selection_from_radiobutton_list: MagicMock, mock_clear_notepad: MagicMock,
                               mock_open_note: MagicMock, mock_display_message_box: MagicMock) -> None:
        self.note_manager_cls.open_note()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.notes_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_not_called()
        mock_clear_notepad.assert_not_called()
        mock_open_note.assert_not_called()
        mock_display_message_box.assert_not_called()

    @patch.object(NoteManager, '_display_message_box')
    @patch.object(NoteManager, '_open_note', side_effect=UnicodeDecodeError('', b'', 0, 0, ''))
    @patch.object(NoteManager, 'clear_notepad')
    @patch.object(NoteManager, '_remove_selection_from_radiobutton_list')
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list')
    def test_open_note_error_1(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                               mock_remove_selection_from_radiobutton_list: MagicMock, mock_clear_notepad: MagicMock,
                               mock_open_note: MagicMock, mock_display_message_box: MagicMock) -> None:
        mock_get_curselection_from_radiobutton_list.return_value = 'note'
        self.note_manager_cls.open_note()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.notes_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.recordings_radiobutton_list)
        mock_clear_notepad.assert_called_once_with()
        mock_open_note.assert_called_once_with('note')
        mock_display_message_box.assert_called_once_with('ERROR', f'Invalid file!', False, 300)

    @patch.object(NoteManager, '_display_message_box')
    @patch.object(NoteManager, '_open_note', side_effect=FileNotFoundError)
    @patch.object(NoteManager, 'clear_notepad')
    @patch.object(NoteManager, '_remove_selection_from_radiobutton_list')
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list')
    def test_open_note_error_2(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                               mock_remove_selection_from_radiobutton_list: MagicMock, mock_clear_notepad: MagicMock,
                               mock_open_note: MagicMock, mock_display_message_box: MagicMock) -> None:
        mock_get_curselection_from_radiobutton_list.return_value = 'note'
        self.note_manager_cls.open_note()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.notes_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.recordings_radiobutton_list)
        mock_clear_notepad.assert_called_once_with()
        mock_open_note.assert_called_once_with('note')
        mock_display_message_box.assert_called_once_with('ERROR', f'Invalid file!', False, 300)

    @patch.object(NoteManager, '_display_message_box')
    @patch.object(NoteManager, '_open_note', side_effect=OSError)
    @patch.object(NoteManager, 'clear_notepad')
    @patch.object(NoteManager, '_remove_selection_from_radiobutton_list')
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list')
    def test_open_note_error_3(self, mock_get_curselection_from_radiobutton_list: MagicMock,
                               mock_remove_selection_from_radiobutton_list: MagicMock, mock_clear_notepad: MagicMock,
                               mock_open_note: MagicMock, mock_display_message_box: MagicMock) -> None:
        mock_get_curselection_from_radiobutton_list.return_value = 'note'
        self.note_manager_cls.open_note()
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.notes_radiobutton_list)
        mock_remove_selection_from_radiobutton_list.assert_called_once_with(
            self.note_manager_cls.recordings_radiobutton_list)
        mock_clear_notepad.assert_called_once_with()
        mock_open_note.assert_called_once_with('note')
        mock_display_message_box.assert_called_once_with('ERROR', f'Invalid file!', False, 300)

    @patch.object(NoteManager, 'notepad_text_area', side_effect=mock_tkinter_textbox)
    @patch.object(NoteManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    def test__open_note(self, mock_notepad_title_field: MagicMock, mock_notepad_text_area: MagicMock) -> None:
        file = io.StringIO('line1\nline2')
        file.write = MagicMock()
        file.close = MagicMock()
        with patch("builtins.open", return_value=file, create=True) as mock_open:
            self.note_manager_cls._open_note('note.txt')
            mock_open.assert_called_once_with(f'{self.note_manager_cls.app_path}/notes/note.txt')
            mock_notepad_text_area.insert.assert_has_calls([call('end', 'line1\n'), call('end', 'line2')])
            file.close.assert_called_once_with()
        mock_notepad_title_field.insert.assert_called_once_with(0, 'note')

    @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.notes_radiobutton_list')
    @patch.object(NoteManager, '_save_note')
    @patch.object(NoteManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    @patch.object(NoteManager, '_filename_exists', return_value=False)
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value=None)
    @patch.object(NoteManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(NoteManager, '_get_full_filename', return_value='file')
    def test_save_note_new_name(self, mock_get_full_filename: MagicMock, mock_notepad_title_field: MagicMock,
                                mock_get_curselection_from_radiobutton_list: MagicMock, mock_filename_exists: MagicMock,
                                mock_display_message_box: MagicMock, mock_save_note: MagicMock,
                                mock_notes_radiobutton_list: MagicMock) -> None:
        mock_notes_radiobutton_list.get_selected_item.return_value = 'different_file'
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.note_manager_cls.notes_radiobutton_list = mock_notes_radiobutton_list
        self.note_manager_cls.save_note()
        mock_get_full_filename.assert_called_once_with(mock_notepad_title_field.get(), 'notes')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(mock_notes_radiobutton_list)
        mock_filename_exists.assert_called_once_with('notes', 'file')
        mock_display_message_box.assert_not_called()
        mock_save_note.assert_called_once_with('file')
        mock_notes_radiobutton_list.add_item.assert_called_once_with('file')

    @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.notes_radiobutton_list')
    @patch.object(NoteManager, '_save_note')
    @patch.object(NoteManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    @patch.object(NoteManager, '_filename_exists', return_value=False)
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value=None)
    @patch.object(NoteManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(NoteManager, '_get_full_filename', return_value='file')
    def test_save_note_existing_name(self, mock_get_full_filename: MagicMock, mock_notepad_title_field: MagicMock,
                                     mock_get_curselection_from_radiobutton_list: MagicMock,
                                     mock_filename_exists: MagicMock, mock_display_message_box: MagicMock,
                                     mock_save_note: MagicMock, mock_notes_radiobutton_list: MagicMock) -> None:
        mock_notes_radiobutton_list.get_selected_item.return_value = 'file'
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.note_manager_cls.notes_radiobutton_list = mock_notes_radiobutton_list
        self.note_manager_cls.save_note()
        mock_get_full_filename.assert_called_once_with(mock_notepad_title_field.get(), 'notes')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(mock_notes_radiobutton_list)
        mock_filename_exists.assert_called_once_with('notes', 'file')
        mock_display_message_box.assert_not_called()
        mock_save_note.assert_called_once_with('file')
        mock_notes_radiobutton_list.add_item.assert_not_called()

    @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.notes_radiobutton_list')
    @patch.object(NoteManager, '_save_note')
    @patch.object(NoteManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    @patch.object(NoteManager, '_filename_exists', return_value=True)
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value=None)
    @patch.object(NoteManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(NoteManager, '_get_full_filename', return_value='file')
    def test_save_note_accepted(self, mock_get_full_filename: MagicMock, mock_notepad_title_field: MagicMock,
                                mock_get_curselection_from_radiobutton_list: MagicMock,
                                mock_filename_exists: MagicMock, mock_display_message_box: MagicMock,
                                mock_save_note: MagicMock, mock_notes_radiobutton_list: MagicMock) -> None:
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.note_manager_cls.notes_radiobutton_list = mock_notes_radiobutton_list
        self.note_manager_cls.save_note()
        mock_get_full_filename.assert_called_once_with(mock_notepad_title_field.get(), 'notes')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(mock_notes_radiobutton_list)
        mock_filename_exists.assert_called_once_with('notes', 'file')
        mock_display_message_box.assert_called_once_with('OVERWRITE FILE', 'The file\nfile already exists.\nOverwrite?',
                                                         True)
        mock_save_note.assert_called_once_with('file')
        mock_notes_radiobutton_list.add_item.assert_not_called()

    @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.notes_radiobutton_list')
    @patch.object(NoteManager, '_save_note')
    @patch.object(NoteManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    @patch.object(NoteManager, '_filename_exists', return_value=True)
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value=None)
    @patch.object(NoteManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(NoteManager, '_get_full_filename', return_value='file')
    def test_save_note_declined(self, mock_get_full_filename: MagicMock, mock_notepad_title_field: MagicMock,
                                mock_get_curselection_from_radiobutton_list: MagicMock,
                                mock_filename_exists: MagicMock, mock_display_message_box: MagicMock,
                                mock_save_note: MagicMock, mock_notes_radiobutton_list: MagicMock) -> None:
        mock_tkinter_messagebox.get.return_value = 'No'
        self.note_manager_cls.notes_radiobutton_list = mock_notes_radiobutton_list
        self.note_manager_cls.save_note()
        mock_get_full_filename.assert_called_once_with(mock_notepad_title_field.get(), 'notes')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(mock_notes_radiobutton_list)
        mock_filename_exists.assert_called_once_with('notes', 'file')
        mock_display_message_box.assert_called_once_with('OVERWRITE FILE', 'The file\nfile already exists.\nOverwrite?',
                                                         True)
        mock_save_note.assert_not_called()
        mock_notes_radiobutton_list.add_item.assert_not_called()

    @patch('scrollable_radiobutton_frame.ScrollableRadiobuttonFrame.notes_radiobutton_list')
    @patch.object(NoteManager, '_display_message_box', return_value=mock_tkinter_messagebox)
    @patch.object(NoteManager, '_save_note', side_effect=OSError)
    @patch.object(NoteManager, '_filename_exists', return_value=False)
    @patch.object(NoteManager, '_get_curselection_from_radiobutton_list', return_value=None)
    @patch.object(NoteManager, 'notepad_title_field', side_effect=mock_tkinter_entry)
    @patch.object(NoteManager, '_get_full_filename', return_value='file')
    def test_save_note_error(self, mock_get_full_filename: MagicMock, mock_notepad_title_field: MagicMock,
                             mock_get_curselection_from_radiobutton_list: MagicMock, mock_filename_exists: MagicMock,
                             mock_save_note: MagicMock, mock_display_message_box: MagicMock,
                             mock_notes_radiobutton_list: MagicMock) -> None:
        mock_notes_radiobutton_list.get_selected_item.return_value = '???'
        mock_tkinter_messagebox.get.return_value = 'Yes'
        self.note_manager_cls.notes_radiobutton_list = mock_notes_radiobutton_list
        self.note_manager_cls.save_note()
        mock_get_full_filename.assert_called_once_with(mock_notepad_title_field.get(), 'notes')
        mock_get_curselection_from_radiobutton_list.assert_called_once_with(mock_notes_radiobutton_list)
        mock_filename_exists.assert_called_once_with('notes', 'file')
        mock_save_note.assert_called_once_with('file')
        mock_display_message_box.assert_called_once_with('ERROR', 'Invalid name!', False, 300)
        mock_notes_radiobutton_list.add_item.assert_not_called()

    @patch.object(NoteManager, 'notepad_text_area', side_effect=mock_tkinter_textbox)
    def test__save_note(self, mock_notepad_text_area: MagicMock) -> None:
        file = io.StringIO('')
        file.write = MagicMock()
        file.close = MagicMock()
        with patch('builtins.open', return_value=file, create=True) as mock_open:
            mock_notepad_text_area.get = MagicMock()
            self.note_manager_cls._save_note('note.txt')
            mock_open.assert_called_once_with(f'{self.note_manager_cls.app_path}/notes/note.txt', 'w')
            mock_notepad_text_area.get.assert_called_once_with(1.0, 'end')
            file.write.assert_called_once_with(mock_notepad_text_area.get())
            file.close.assert_called_once_with()
