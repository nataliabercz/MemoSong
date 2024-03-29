import tkinter
from file_manager import FileManager


class NoteManager(FileManager):
    def open_note(self) -> None:
        FileManager._current_browser_type = 'notes'
        # what if file suddenly doesn't exist
        try:
            if note := self._get_curselection_from_radiobutton_list(self.notes_radiobutton_list):
                self._remove_selection_from_radiobutton_list(self.recordings_radiobutton_list)
                self.clear_notepad()
                self._open_note(note)
        except (UnicodeDecodeError, FileNotFoundError, OSError):
            self._display_message_box('ERROR', f'Invalid file!', False, 300)

    def _open_note(self, note: str) -> None:
        with open(f'{self.app_path}/notes/{note}') as file:
            for line in file:
                self.notepad_text_area.insert(tkinter.END, line)
        self.notepad_title_field.insert(0, ''.join(note.split('.')[0:-1]))

    def save_note(self) -> None:
        is_overwritten = False
        filename = self._get_full_filename(self.notepad_title_field.get(), 'notes')
        current_selection = self._get_curselection_from_radiobutton_list(self.notes_radiobutton_list)
        if self._filename_exists('notes', filename) and filename != current_selection:
            msg = self._display_message_box('OVERWRITE FILE', f'The file\n{filename} already exists.\nOverwrite?', True)
            if msg.get() == 'Yes':
                self._save_note(filename)
                is_overwritten = True
            else:
                return
        else:
            try:
                self._save_note(filename)
            except OSError:
                self._display_message_box('ERROR', f'Invalid name!', False, 300)
                return
        if filename != self.notes_radiobutton_list.get_selected_item() and not is_overwritten:
            self.notes_radiobutton_list.add_item(filename)

    def _save_note(self, filename: str) -> None:
        with open(f'{self.app_path}/notes/{filename}', 'w') as file:
            file.write(self.notepad_text_area.get(1.0, tkinter.END))
