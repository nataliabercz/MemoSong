import tkinter
import customtkinter
from typing import Dict, Any, Optional
from piano import Piano
from file_manager import FileManager
from note_manager import NoteManager
from recording_manager import RecordingManager
from generic_functions import GenericFunctions


class MemoSong(GenericFunctions):
    piano = Piano()
    file_manager = FileManager()
    note_manager = NoteManager()
    recording_manager = RecordingManager()
    keyboard_on = False

    def __init__(self, root) -> None:
        self.root = root

    def run_application(self) -> None:
        self.set_theme()
        self.prepare_layout()
        self.root.mainloop()

    def quit_application(self) -> None:
        self.root.destroy()

    def set_theme(self) -> None:
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme(f'{self.app_path}/data/theme.json')

    def prepare_layout(self) -> None:
        self.configure_window()
        self.load_image_names()
        self.configure_logo()
        self.configure_voice_recorder()
        self.configure_control_panel()
        self.configure_file_browser('recordings', 2)
        self.configure_notepad()
        self.configure_file_browser('notes', 4)
        self.configure_piano()
        self._initialize_sound_mixer()

    def configure_window(self) -> None:
        self.root.title(self.title)
        self.root.iconbitmap(f'{self.images_path}/logo.ico')
        self.root.configure()
        left = (self.root.winfo_screenwidth() - self.width) / 2
        top = (self.root.winfo_screenheight() - self.height) / 2
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, left, top))
        self.root.resizable(0, 0)
        self.root.columnconfigure(0, weight=1)

    def _create_main_frame(self, column: int, row: int, sticky: Optional[str] = tkinter.NSEW,
                           frame_data: Optional[Dict[str, Any]] = None,
                           grid_data: Optional[Dict[str, Any]] = None) -> customtkinter.CTkFrame:
        frame = customtkinter.CTkFrame(self.root, **frame_data or {})
        frame.grid(column=column, row=row, sticky=sticky, **grid_data or {})
        return frame

    def configure_logo(self) -> None:
        logo_frame = self._create_main_frame(0, 0, sticky=tkinter.NW, frame_data={'width': int(self.width/7),
                                                                                  'height': int(self.height/4)})
        self._create_label(logo_frame, '', image=self._open_image('logo_image', (110, 105)), padx=20, pady=20)

    def configure_voice_recorder(self) -> None:
        microphone_frame = self._create_main_frame(1, 0, sticky=tkinter.NW, frame_data={'width': int(self.width/4),
                                                                                        'height': int(self.height/4)})
        self._create_label(microphone_frame, 'RECORD VOICE', side=tkinter.TOP)
        self.add_voice_recorder_title_frame(microphone_frame)
        for item in ['start_voice_recording', 'pause_voice_recording', 'stop_voice_recording']:
            self._create_button_from_image(microphone_frame, item, (40, 55), getattr(self.recording_manager, item),
                                           tkinter.LEFT, self.recording_manager, width=60)

    def add_voice_recorder_title_frame(self, frame: customtkinter.CTkFrame) -> None:
        recording_title = customtkinter.CTkFrame(frame)
        recording_title.pack(side=tkinter.BOTTOM)
        self.recording_manager.voice_recording_title_field = customtkinter.CTkEntry(recording_title, width=120)
        self.recording_manager.voice_recording_title_field.pack(side=tkinter.BOTTOM)
        self._create_label(recording_title, 'Title: ', side=tkinter.BOTTOM)

    def configure_control_panel(self) -> None:
        control_panel_frame = self._create_main_frame(0, 1, frame_data={'width': int(self.width/4),
                                                                        'height': int(self.height/3)},
                                                      grid_data={'columnspan': 2})
        self._create_label(control_panel_frame, 'RECORD PIANO', anchor=tkinter.W, padx=68)
        self.add_piano_recorder_title_frame(control_panel_frame)
        self.add_update_file_frame(control_panel_frame)
        for item in ['start_piano_recording', 'pause_piano_recording', 'stop_piano_recording']:
            self._create_button_from_image(control_panel_frame, item, (60, 60), getattr(self.recording_manager, item),
                                           tkinter.LEFT, self.recording_manager)

    def add_update_file_frame(self, frame: customtkinter.CTkFrame) -> None:
        update_file_frame = customtkinter.CTkFrame(frame)
        update_file_frame.pack(side=tkinter.RIGHT)
        self._create_label(update_file_frame, 'EDIT FILE')
        for item in ['Rename', 'Delete']:
            self._create_control_button(update_file_frame, item,
                                        lambda option=item.lower(): self.file_manager.edit_file(option), width=70)

    def add_piano_recorder_title_frame(self, frame: customtkinter.CTkFrame) -> None:
        title_frame = customtkinter.CTkFrame(frame, height=int(self.height/12))
        title_frame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
        self._create_label(title_frame, '  Title: ', side=tkinter.LEFT)
        self.recording_manager.piano_recording_title_field = customtkinter.CTkEntry(title_frame, width=105)
        self.recording_manager.piano_recording_title_field.pack(side=tkinter.LEFT)
        self._create_button_from_image(title_frame, 'keyboard', (45, 25), self.turn_keyboard_piano, tkinter.LEFT, self)
        self._create_button_from_image(title_frame, 'mute', (25, 25), self._mute_playback, tkinter.RIGHT, self)

    def turn_keyboard_piano(self) -> None:
        if not self.keyboard_on:
            self.root.focus()
            self.keyboard_on = True
            self._highlight_used_function('keyboard', 'on')
            self.root.bind('<Key>', self.play_pressed_key)
            self.add_keyboard_text()
        else:
            self.keyboard_on = False
            self._highlight_used_function('keyboard', 'off')
            self.root.unbind('<Key>')
            self.remove_keyboard_text()

    def play_pressed_key(self, event) -> None:
        key = event.char.lower()
        if key in self.key_map:
            self.highlight_button(key)
            self.root.update_idletasks()
            self.play_key(key)

    def play_key(self, key: str) -> None:
        Piano.key = key
        self.start_new_thread(self.piano.play_key)

    def configure_file_browser(self, browser_type: str, column_number: int) -> None:
        browser_frame = self._create_main_frame(column_number, 0, grid_data={'rowspan': 2})
        self._create_label(browser_frame, browser_type.upper(), side=tkinter.TOP)
        header_frame = customtkinter.CTkFrame(browser_frame)
        header_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self._create_label(header_frame, 'Find: ', side=tkinter.LEFT)
        browser_search_field = customtkinter.CTkEntry(header_frame, width=120)
        browser_search_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        setattr(self.file_manager, f'{browser_type}_search_field', browser_search_field)
        self._create_control_button(header_frame, 'Search', getattr(self.file_manager, f'search_{browser_type}'),
                                    tkinter.LEFT, width=1)
        self._create_control_button(browser_frame, 'Update List', lambda: self.file_manager.update_list(browser_type),
                                    tkinter.BOTTOM)
        if browser_type == 'notes':
            command = self.note_manager.open_note
        else:
            command = self.recording_manager.play_recording
        self._create_radiobutton_list(browser_frame, browser_type, command)

    def _create_radiobutton_list(self, browser_frame: customtkinter.CTkFrame, browser_type: str, command: Any) -> None:
        radiobutton_list = self.file_manager.create_radiobutton_list(browser_frame, browser_type, command)
        setattr(FileManager, f'{browser_type}_radiobutton_list', radiobutton_list)

    def configure_notepad(self) -> None:
        notepad_frame = self._create_main_frame(3, 0, frame_data={'height': self.height-200}, grid_data={'rowspan': 2})
        self._create_label(notepad_frame, 'NOTEPAD', side=tkinter.TOP)
        header_frame = customtkinter.CTkFrame(notepad_frame)
        header_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self._create_control_button(header_frame, 'Save', self.note_manager.save_note, tkinter.LEFT, width=1)
        self._create_label(header_frame, 'Title: ', side=tkinter.LEFT)
        self._setup_notepad(header_frame, notepad_frame)

    @staticmethod
    def _setup_notepad(header_frame: customtkinter.CTkFrame, notepad_frame: customtkinter.CTkFrame) -> None:
        FileManager.notepad_title_field = customtkinter.CTkEntry(header_frame, width=150)
        FileManager.notepad_title_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        FileManager.notepad_text_area = customtkinter.CTkTextbox(notepad_frame)
        FileManager.notepad_text_area.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    def configure_piano(self) -> None:
        piano_frame = self._create_main_frame(0, 2, grid_data={'columnspan': 5})
        key_swift = 45
        pad_x_white = 5
        pad_x_black = 40
        for key in self.key_map:
            if self._is_white_key(key):
                self._create_piano_button(piano_frame, key, pad_x_white, 3, 5, fg_color='white', width=47, height=225,
                                          border_width=1, border_color='black')
                pad_x_white += key_swift
        for key in self.key_map:
            if key in ['e', 'u', 'p', 'x', 'b']:
                pad_x_black += key_swift
            if not self._is_white_key(key):
                self._create_piano_button(piano_frame, key, pad_x_black, 4, 26, fg_color='black', width=22, height=140)
                pad_x_black += key_swift

    def _create_piano_button(self, frame: customtkinter.CTkFrame, key: str, pad_x: int, pad_y: int, span: int,
                             **kwargs: Any) -> None:
        button = customtkinter.CTkButton(frame, command=lambda x=key: self.play_key(x), text='', corner_radius=0,
                                         **kwargs)
        button.grid(column=0, row=2, columnspan=span, sticky=tkinter.NW, padx=pad_x, pady=pad_y)
        if self._is_white_key(key):
            button.configure(text=self.key_map[key][0].upper(), text_color='black', anchor=tkinter.S)
        setattr(GenericFunctions, f'{key}_key', button)


if __name__ == '__main__':
    memo_song = MemoSong(customtkinter.CTk())
    memo_song.run_application()
