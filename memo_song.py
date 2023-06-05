import os
import time
import threading
import pygame
import tkinter
import customtkinter
from key_player import KeyPlayer
from piano_recorder import PianoRecorder
from voice_recorder import VoiceRecorder
from scrollable_radiobutton_frame import ScrollableRadiobuttonFrame
from generic_functions import GenericFunctions
from typing import Any


class MemoSong(GenericFunctions):
    notepad_title_field = None
    notepad_text_area = None
    recordings_radiobutton_list = None
    notes_radiobutton_list = None

    key_player = KeyPlayer()

    piano_recorder = PianoRecorder()
    piano_recording_title_field = None
    piano_recording_title = None

    voice_recorder = VoiceRecorder()
    voice_recording_title_field = None
    voice_recording_title = None

    filename = None
    keyboard_on = False
    current_browser_type = None
    is_overwritten = False

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

    def load_image_names(self) -> None:
        for image in os.listdir(f'{self.images_path}'):
            if '.png' in image:
                self.set_image_name(image.rsplit('.', 1)[0])

    def set_image_name(self, image_name) -> None:
        setattr(self, f'{image_name}_image', f'{self.images_path}/{image_name}.png')

    def configure_logo(self) -> None:
        logo_frame = customtkinter.CTkFrame(self.root, width=int(self.width/7), height=int(self.height/4),
                                            fg_color='transparent').grid(column=0, row=0, sticky=tkinter.NW)
        customtkinter.CTkLabel(logo_frame, image=self._open_image('logo_image', (110, 105)), text='')\
            .grid(column=0, row=0, sticky=tkinter.NW, padx=10, pady=20)
        self.add_piano_recorder_label(logo_frame)

    @staticmethod
    def add_piano_recorder_label(frame: customtkinter.CTkFrame) -> None:
        customtkinter.CTkLabel(frame, text='RECORD PIANO', fg_color='transparent').grid(column=0, row=0,
                                                                                        sticky=tkinter.SE, padx=20)

    def configure_voice_recorder(self) -> None:
        microphone_frame = customtkinter.CTkFrame(self.root, width=int(self.width/4), height=int(self.height/4),
                                                  fg_color='transparent')
        microphone_frame.grid(column=1, row=0, sticky=tkinter.NW, pady=10)
        customtkinter.CTkLabel(microphone_frame, text='RECORD VOICE', fg_color='transparent').pack(side=tkinter.TOP)
        self.add_voice_recorder_title_frame(microphone_frame)
        for item in ['start_voice_recording', 'pause_voice_recording', 'stop_voice_recording']:
            self._create_button_from_image(microphone_frame, item, (40, 55), getattr(self, item), tkinter.LEFT, width=60)

    def add_voice_recorder_title_frame(self, frame: customtkinter.CTkFrame) -> None:
        recording_title = customtkinter.CTkFrame(frame, fg_color='transparent')
        recording_title.pack(side=tkinter.BOTTOM)
        self.voice_recording_title_field = customtkinter.CTkEntry(recording_title, width=120)
        self.voice_recording_title_field.pack(side=tkinter.BOTTOM)
        customtkinter.CTkLabel(recording_title, text='Title: ').pack(side=tkinter.BOTTOM)

    def configure_control_panel(self) -> None:
        control_panel_frame = customtkinter.CTkFrame(self.root, width=int(self.width/4), height=int(self.height/3),
                                                     fg_color='transparent')
        control_panel_frame.grid(column=0, row=1, columnspan=2, sticky=tkinter.NSEW)
        self.add_piano_recorder_title_frame(control_panel_frame)
        self.add_update_file_frame(control_panel_frame)
        for item in ['start_piano_recording', 'pause_piano_recording', 'stop_piano_recording']:
            self._create_button_from_image(control_panel_frame, item, (60, 60), getattr(self, item), tkinter.LEFT)

    def add_update_file_frame(self, frame: customtkinter.CTkFrame) -> None:
        update_file_frame = customtkinter.CTkFrame(frame, fg_color='transparent')
        update_file_frame.pack(side=tkinter.RIGHT)
        customtkinter.CTkLabel(update_file_frame, text='EDIT FILE', fg_color='transparent').pack()
        for item in ['Rename', 'Delete']:
            customtkinter.CTkButton(update_file_frame, text=item, width=70, fg_color='#1f538d', border_color='gray13',
                                    border_width=1, command=lambda option=item.lower(): self.edit_file(option)).pack()

    def add_piano_recorder_title_frame(self, frame: customtkinter.CTkFrame) -> None:
        title_frame = customtkinter.CTkFrame(frame, height=int(self.height / 12), fg_color='transparent')
        title_frame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
        customtkinter.CTkLabel(title_frame, text='  Title: ').pack(side=tkinter.LEFT)
        self.piano_recording_title_field = customtkinter.CTkEntry(title_frame, width=105)
        self.piano_recording_title_field.pack(side=tkinter.LEFT)
        self._create_button_from_image(title_frame, 'keyboard', (45, 25), self.turn_keyboard_piano, tkinter.LEFT)
        self._create_button_from_image(title_frame, 'mute', (25, 25), self._mute_playback, tkinter.RIGHT)

    def configure_file_browser(self, browser_type: str, column_number: int) -> None:
        browser_frame = customtkinter.CTkFrame(self.root, fg_color='transparent')
        browser_frame.grid(column=column_number, row=0, rowspan=2, sticky=tkinter.NSEW)
        customtkinter.CTkLabel(browser_frame, text=browser_type.upper()).pack(side=tkinter.TOP)
        header_frame = customtkinter.CTkFrame(browser_frame, fg_color='transparent')
        header_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        customtkinter.CTkLabel(header_frame, text='Find: ').pack(side=tkinter.LEFT)
        browser_search_field = customtkinter.CTkEntry(header_frame, width=120)
        browser_search_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        setattr(self, f'{browser_type}_search_field', browser_search_field)
        customtkinter.CTkButton(header_frame, text='Search', command=getattr(self, f'search_{browser_type}'), width=1,
                                fg_color='#1f538d', border_color='gray13', border_width=1).pack(side=tkinter.LEFT)
        customtkinter.CTkButton(browser_frame, text='Update List', fg_color='#1f538d', border_color='gray13',
                                border_width=1, command=lambda: self.update_list(browser_type))\
            .pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)
        self.create_radiobutton_lists(browser_frame, browser_type)

    def create_radiobutton_lists(self, browser_frame: customtkinter.CTkFrame,
                                 browser_type: str) -> None:
        if not self._directory_exists(browser_type):
            self._create_directory(browser_type)
        files = []
        extension = self._get_extension(browser_type)
        for file in os.listdir(f'{self.app_path}/{browser_type}'):
            if extension in file:
                files.append(file)
        if browser_type == 'notes':
            command = self.open_note
        else:
            command = self.play_recording
        radiobutton_list = ScrollableRadiobuttonFrame(browser_frame, files, browser_type, command=command, width=1)
        radiobutton_list.bind('<<ListboxSelect>>', command)
        radiobutton_list.pack(fill=tkinter.BOTH)
        setattr(self, f'{browser_type}_radiobutton_list', radiobutton_list)

    def configure_notepad(self) -> None:
        notepad_frame = customtkinter.CTkFrame(self.root, height=self.height-200, fg_color='transparent')
        notepad_frame.grid(column=3, row=0, rowspan=2, sticky=tkinter.NSEW)
        customtkinter.CTkLabel(notepad_frame, text='NOTEPAD').pack(side=tkinter.TOP)
        header_frame = customtkinter.CTkFrame(notepad_frame, fg_color='transparent')
        header_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        customtkinter.CTkButton(header_frame, text='Save', width=1, fg_color='#1f538d', border_color='gray13',
                                border_width=1, command=self.save_note).pack(side=tkinter.LEFT)
        customtkinter.CTkLabel(header_frame, text='Title: ').pack(side=tkinter.LEFT)
        self.notepad_title_field = customtkinter.CTkEntry(header_frame, width=150)
        self.notepad_title_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.notepad_text_area = customtkinter.CTkTextbox(notepad_frame)
        self.notepad_text_area.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

    def configure_piano(self) -> None:
        piano_frame = customtkinter.CTkFrame(self.root, fg_color='transparent')
        piano_frame.grid(column=0, row=2, columnspan=5, sticky=tkinter.NSEW)

        key_swift = 45
        pad_x_white = 5
        pad_x_black = 40
        for key in self.key_map:
            if self._is_white_key(key):
                button = customtkinter.CTkButton(piano_frame, text='', command=lambda x=key: self.play_key(x),
                                                 border_width=1, border_color='black', fg_color='white', width=47,
                                                 height=225, corner_radius=0)
                button.grid(column=0, row=2, columnspan=5, sticky=tkinter.SW, padx=pad_x_white, pady=3)
                setattr(self, f'{key}_key', button)
                pad_x_white += key_swift

        for key in self.key_map:
            if key in ['e', 'u', 'p', 'x', 'b']:
                pad_x_black += key_swift
            if not self._is_white_key(key):
                button = customtkinter.CTkButton(piano_frame, text='', command=lambda x=key: self.play_key(x),
                                                 fg_color='black', corner_radius=0, width=22, height=140)
                button.grid(column=0, row=2, columnspan=26, sticky=tkinter.NW, padx=pad_x_black, pady=4)
                setattr(self, f'{key}_key', button)
                pad_x_black += key_swift

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

    def add_keyboard_text(self) -> None:
        for key in self.key_map:
            button = getattr(self, f'{key}_key')
            if self._is_white_key(key):
                text_color = 'black'
            else:
                text_color = 'white'
            button.configure(text=key, text_color=text_color, anchor=tkinter.S)

    def remove_keyboard_text(self) -> None:
        for key in self.key_map:
            button = getattr(self, f'{key}_key')
            button.configure(text='')

    def play_pressed_key(self, event) -> None:
        key = event.char.lower()
        if key in self.key_map:
            button = getattr(self, f'{key}_key')
            self.highlight_button(button)
            self.root.update_idletasks()
            self.play_key(key)
            time.sleep(0.05)
            self.remove_button_highlight(button, key)

    def play_key(self, key: str) -> None:
        self.key_player.key = key
        self.start_new_thread(self.key_player.play_key)
        self.update_piano_recorder_key(key)

    def update_piano_recorder_key(self, key: str) -> None:
        if self.piano_recorder.recording:
            self.piano_recorder.key = key

    @staticmethod
    def highlight_button(button: customtkinter.CTkButton) -> None:
        button.configure(fg_color=['#325882', '#14375e'])

    def remove_button_highlight(self, button: customtkinter.CTkButton, key: str) -> None:
        button.configure(fg_color='white') if self._is_white_key(key) else button.configure(fg_color='black')

    def save_note(self) -> None:
        is_overwritten = False
        filename = self._get_filename(self.notepad_title_field.get(), 'notes')
        current_selection = self._get_curselection_from_radiobutton_list(self.notes_radiobutton_list)
        if self._filename_exists('notes', filename) and filename != current_selection:
            msg = self._display_message_box('OVERWRITE FILE', f'The file\n{filename} already exists.\nOverwrite?', True)
            if msg.get() == 'Yes':
                self.save_file(filename)
                is_overwritten = True
            else:
                return
        else:
            self.save_file(filename)
        if filename != self.notes_radiobutton_list.get_selected_item() and not is_overwritten:
            self.notes_radiobutton_list.add_item(filename)

    def save_file(self, filename: str) -> None:
        with open(f'{self.app_path}/notes/{filename}', 'w') as file:
            file.write(self.notepad_text_area.get(1.0, tkinter.END))
            file.close()

    def search_recordings(self) -> None:
        self._search('recordings')

    def search_notes(self) -> None:
        self._search('notes')

    def _search(self, browser_type: str) -> None:
        radiobutton_list = getattr(self, f'{browser_type}_radiobutton_list')
        search_field = getattr(self, f'{browser_type}_search_field')
        radiobutton_list.clear_list()
        searched_item = search_field.get()
        for file in os.listdir(f'{self.app_path}/{browser_type}'):
            if searched_item in file:
                radiobutton_list.add_item(file)

    def update_list(self, browser_type: str) -> None:
        radiobutton_list = getattr(self, f'{browser_type}_radiobutton_list')
        radiobutton_list.clear_list()
        extension = self._get_extension(browser_type)
        for file in os.listdir(f'{self.app_path}/{browser_type}'):
            if extension in file:
                radiobutton_list.add_item(file)

    def open_note(self) -> None:
        self.current_browser_type = 'notes'
        # what if file suddenly doesn't exist
        try:
            if note := self._get_curselection_from_radiobutton_list(self.notes_radiobutton_list):
                self._remove_selection_from_radiobutton_list(self.recordings_radiobutton_list)
                self.notepad_title_field.delete(0, tkinter.END)
                self.notepad_text_area.delete('1.0', tkinter.END)
                with open(f'{self.app_path}/notes/{note}') as file:
                    for line in file:
                        self.notepad_text_area.insert(tkinter.END, line)
                    file.close()
                self.notepad_title_field.insert(0, ''.join(note.split('.')[0:-1]))
        except UnicodeDecodeError:
            self._display_message_box('ERROR', f'Invalid file!', False, 300)

    def play_recording(self) -> None:
        self.current_browser_type = 'recordings'
        try:
            if song := self._get_curselection_from_radiobutton_list(self.recordings_radiobutton_list):
                self._remove_selection_from_radiobutton_list(self.notes_radiobutton_list)
                pygame.mixer.music.load(f'{self.app_path}/recordings/{song}')
                pygame.mixer.music.play()
        except pygame.error:
            self._display_message_box('ERROR', f'Invalid file!', False, 300)

    def edit_file(self, option: str) -> None:
        if self.current_browser_type:
            file_to_edit = self._get_curselection_from_radiobutton_list(
                    getattr(self, f'{self.current_browser_type}_radiobutton_list'))
            self.rename_file(file_to_edit) if option == 'rename' else self.delete_file(file_to_edit)
        else:
            self._display_message_box('ERROR', f'Please, select a file to {option}', False, 300)

    def rename_file(self, file_to_rename: str) -> None:
        try:
            if new_name := customtkinter.CTkInputDialog(text='New Name', title='RENAME FILE').get_input():
                self._mute_playback()
                file_path = f'{self.app_path}/{self.current_browser_type}'
                os.rename(f'{file_path}/{file_to_rename}',
                          f'{file_path}/{new_name}.{self._get_extension(self.current_browser_type)}')
                self.update_list(self.current_browser_type)
            if self.current_browser_type == 'notes':
                self.notepad_title_field.delete(0, tkinter.END)
                self.notepad_title_field.insert(0, new_name)
        except OSError as e:
            self._display_message_box('ERROR', str(e).split('] ')[1].split(':')[0], False, 300)

    def delete_file(self, file_to_delete: str) -> None:
        try:
            msg = self._display_message_box('DELETE FILE', f'Do you want to delete\n{file_to_delete}?', True)
            if msg.get() == 'Yes':
                self._mute_playback()
                os.remove(f'{self.app_path}/{self.current_browser_type}/{file_to_delete}')
                self.update_list(self.current_browser_type)
                if self.current_browser_type == 'notes':
                    self.notepad_text_area.delete('1.0', tkinter.END)
                    self.notepad_title_field.delete(0, tkinter.END)
            else:
                msg.destroy()
        except Exception as e:
            # is it necessary ?? when it occurs?
            print(str(e))

    def start_piano_recording(self) -> None:
        self._start_recording('piano')

    def start_voice_recording(self) -> None:
        self._start_recording('voice')

    def _start_recording(self, recording_type: str) -> None:
        recorder = getattr(self, f'{recording_type}_recorder')
        if not recorder.recording:
            recorder.paused = False
            self._highlight_used_function(f'pause_{recording_type}_recording', 'off')
            self._highlight_used_function(f'start_{recording_type}_recording', 'on')
            title = self._get_recording_title(recording_type)
            if title in os.listdir(f'{self.app_path}/recordings'):
                # it should block application !!
                msg = self._display_message_box('OVERWRITE FILE', f'The file\n{title} already exists. Overwrite?', True)
                if msg.get() == 'Yes':
                    self.is_overwritten = True
                    self._setup_recorder(recorder, recording_type, title)
                else:
                    self._highlight_used_function(f'start_{recording_type}_recording', 'off')
            else:
                self._setup_recorder(recorder, recording_type, title)

    def _get_recording_title(self, recording_type: str) -> str:
        title_field = getattr(self, f'{recording_type}_recording_title_field')
        return self._get_filename(title_field.get(), 'recordings', f'{recording_type}_')

    def _setup_recorder(self, recorder: Any, recording_type: str, title: str) -> None:
        setattr(self, f'{recording_type}_recording_title', title)
        recorder.recording = True
        recorder.recording_full_name = f'{self.app_path}/recordings/{title}'
        recorder.current_time = time.time()
        self.start_new_thread(recorder.record)

    @staticmethod
    def start_new_thread(target: Any) -> None:
        threading.Thread(target=target).start()

    def pause_piano_recording(self) -> None:
        self._pause_recording('piano')

    def pause_voice_recording(self) -> None:
        self._pause_recording('voice')

    def _pause_recording(self, recording_type: str) -> None:
        recorder = getattr(self, f'{recording_type}_recorder')
        if recorder.paused:
            self._setup_pause(recorder, recording_type, 'off')
            return
        self._setup_pause(recorder, recording_type, 'on')

    def _setup_pause(self, recorder: Any, recording_type: str, option: str) -> None:
        self._highlight_used_function(f'pause_{recording_type}_recording', option)
        recorder.paused = True if option == 'on' else False

    def stop_piano_recording(self) -> None:
        self._stop_recording('piano')

    def stop_voice_recording(self) -> None:
        self._stop_recording('voice')

    def _stop_recording(self, recording_type: str) -> None:
        recorder = getattr(self, f'{recording_type}_recorder')
        if recorder.recording:
            self._highlight_used_function(f'start_{recording_type}_recording', 'off')
            recorder.recording = False
            # if not self.is_overwritten:
            #     self.update_list('recordings')
            #     self.is_overwritten = False
            self.recordings_radiobutton_list.add_item(getattr(self, f'{recording_type}_recording_title'))


if __name__ == '__main__':
    memo_song = MemoSong(customtkinter.CTk())
    memo_song.run_application()
