import os
import datetime
import tkinter
import customtkinter
from typing import List, Any, Optional
from generic_functions import GenericFunctions
from scrollable_radiobutton_frame import ScrollableRadiobuttonFrame


class FileManager(GenericFunctions):
    _current_browser_type = None
    recordings_radiobutton_list = None
    notes_radiobutton_list = None
    notepad_title_field = None
    notepad_text_area = None

    def edit_file(self, option: str) -> None:
        if self._current_browser_type:
            file_to_edit = self._get_curselection_from_radiobutton_list(
                    getattr(self, f'{self._current_browser_type}_radiobutton_list'))
            self._rename_file(file_to_edit) if option == 'rename' \
                else self._delete_file(file_to_edit)
        else:
            self._display_message_box('ERROR', f'Please, select a file to {option}', False, 300)

    def update_list(self, browser_type: str) -> None:
        radiobutton_list = getattr(self, f'{browser_type}_radiobutton_list')
        radiobutton_list.clear_list()
        extension = self._get_extension(browser_type)
        for file in self._list_files(f'{self.app_path}/{browser_type}'):
            if extension in file:
                radiobutton_list.add_item(file)

    def create_radiobutton_list(self, browser_frame: customtkinter.CTkFrame,
                                browser_type: str, command: Any) -> ScrollableRadiobuttonFrame:
        if not self._directory_exists(browser_type):
            self._create_directory(browser_type)
        files = []
        for file in self._list_files(f'{self.app_path}/{browser_type}'):
            if self._get_extension(browser_type) in file:
                files.append(file)
        radiobutton_list = ScrollableRadiobuttonFrame(browser_frame, files, browser_type, command=command, width=1)
        radiobutton_list.bind('<<ListboxSelect>>', command)
        radiobutton_list.pack(fill=tkinter.BOTH)
        return radiobutton_list

    def _rename_file(self, file_to_rename: str) -> None:
        try:
            if new_name := customtkinter.CTkInputDialog(text='New Name', title='RENAME FILE').get_input():
                if self._current_browser_type == 'recordings':
                    self._mute_playback()
                file_path = f'{self.app_path}/{self._current_browser_type}'
                os.rename(f'{file_path}/{file_to_rename}',
                          f'{file_path}/{new_name}.{self._get_extension(self._current_browser_type)}')
                self.update_list(self._current_browser_type)
            if self._current_browser_type == 'notes':
                self.notepad_title_field.delete(0, tkinter.END)
                self.notepad_title_field.insert(0, new_name)
        except OSError as e:
            self._display_message_box('ERROR', str(e).split('] ')[1].split(':')[0], False, 300)

    def _delete_file(self, file_to_delete: str) -> None:
        msg = self._display_message_box('DELETE FILE', f'Do you want to delete\n{file_to_delete}?', True)
        if msg.get() == 'Yes':
            if self._current_browser_type == 'recordings':
                self._mute_playback()
            self._remove_file(file_to_delete)
            self.update_list(self._current_browser_type)
            if self._current_browser_type == 'notes':
                self.notepad_text_area.delete('1.0', tkinter.END)
                self.notepad_title_field.delete(0, tkinter.END)
        else:
            msg.destroy()

    def _remove_file(self, file_to_delete: str) -> None:
        try:
            os.remove(f'{self.app_path}/{self._current_browser_type}/{file_to_delete}')
        except FileNotFoundError:
            pass

    def _get_full_filename(self, filename: str, browser_type: str, prefix: Optional[str] = '') -> str:
        if not self._directory_exists(browser_type):
            self._create_directory(browser_type)
        if filename == '':
            filename = f'{prefix}{browser_type[0:-1]}_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        return f'{filename}.{self._get_extension(browser_type)}'

    def search_recordings(self) -> None:
        self._search('recordings')

    def search_notes(self) -> None:
        self._search('notes')

    def _search(self, browser_type: str) -> None:
        radiobutton_list = getattr(self, f'{browser_type}_radiobutton_list')
        search_field = getattr(self, f'{browser_type}_search_field')
        radiobutton_list.clear_list()
        searched_item = search_field.get()
        for file in self._list_files(f'{self.app_path}/{browser_type}'):
            if searched_item in file:
                radiobutton_list.add_item(file)

    @staticmethod
    def _get_extension(browser_type: str) -> str:
        return 'txt' if browser_type == 'notes' else 'wav'
