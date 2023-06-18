import os
import pygame
import tkinter
import threading
import customtkinter
import CTkMessagebox
from PIL import Image
from typing import Tuple, Optional, Any
from scrollable_radiobutton_frame import ScrollableRadiobuttonFrame


class GenericFunctions:
    _width = 1000
    _height = 535
    _title = 'MemoSong'
    key_map = {'q': 'c3', '2': 'c#3', 'w': 'd3', '3': 'd#3', 'e': 'e3', 'r': 'f3', '5': 'f#3', 't': 'g3', '6': 'g#3',
               'y': 'a3', '7': 'a#3', 'u': 'b3', 'i': 'c4', '9': 'c#4', 'o': 'd4', '0': 'd#4', 'p': 'e4', '[': 'f4',
               '=': 'f#4', ']': 'g4', 'a': 'g#4', 'z': 'a4', 's': 'a#4', 'x': 'b4', 'c': 'c5', 'f': 'c#5', 'v': 'd5',
               'g': 'd#5', 'b': 'e5', 'n': 'f5', 'j': 'f#5', 'm': 'g5', 'k': 'g#5', ',': 'a5', 'l': 'a#5', '.': 'b5',
               '/': 'c6'}
    app_path = os.path.dirname(os.path.realpath(__file__))
    images_path = f'{app_path}/data/images'
    keys_path = f'{app_path}/data/keys'

    def _set_theme(self) -> None:
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme(f'{self.app_path}/data/theme.json')

    def _is_white_key(self, key: str) -> bool:
        return '#' not in self.key_map[key]

    def _filename_exists(self, browser_type: str, filename: str) -> bool:
        return filename in os.listdir(f'{self.app_path}/{browser_type}')

    def _directory_exists(self, browser_type: str) -> bool:
        return browser_type in os.listdir(self.app_path) and os.path.isdir(f'{self.app_path}/{browser_type}')

    def _create_directory(self, browser_type: str) -> None:
        os.mkdir(f'{self.app_path}/{browser_type}')

    def _open_image(self, image_name: str, size=None) -> customtkinter.CTkImage:
        return customtkinter.CTkImage(Image.open(getattr(self, image_name)), size=size)

    def _highlight_used_function(self, button_name: str, option: str) -> None:
        button = getattr(self, f'{button_name}_button')
        button.configure(border_width=1) if option == 'on' else button.configure(border_width=0)

    @staticmethod
    def _initialize_sound_mixer() -> None:
        pygame.mixer.init()

    def _mute_playback(self) -> None:
        pygame.mixer.quit()
        self._initialize_sound_mixer()

    def _create_button_from_image(self, frame: customtkinter.CTkFrame, button_name: str, image_size: Tuple[int, int],
                                  command: Any, side: tkinter.constants, obj: Any, width: Optional[int] = None) -> None:
        if not width:
            width = image_size[0]
        button = customtkinter.CTkButton(frame, text='', width=width, command=command,
                                         image=self._open_image(f'{button_name}_image', image_size))
        button.pack(side=side)
        setattr(obj, f'{button_name}_button', button)

    @staticmethod
    def _get_curselection_from_radiobutton_list(radiobutton_list: Any) -> str:
        try:
            return radiobutton_list.get_selected_item()
        except tkinter.TclError:
            # when is it used?
            pass

    @staticmethod
    def _remove_selection_from_radiobutton_list(radiobutton_list: ScrollableRadiobuttonFrame) -> None:
        radiobutton_list.remove_item_selection()

    @staticmethod
    def _display_message_box(title: str, message: str, options: bool, width: int = 600) -> CTkMessagebox.CTkMessagebox:
        data = {'title': title, 'message': message, 'width': width, 'height': 1, 'fade_in_duration': 1,
                'icon_size': (30, 30), 'icon': 'warning', 'bg_color': ['gray90', 'gray13']}
        if options:
            data.update({'option_1': 'No', 'option_2': 'Yes'})
        return CTkMessagebox.CTkMessagebox(**data)

    @staticmethod
    def _start_new_thread(target: Any) -> None:
        threading.Thread(target=target).start()

    def _highlight_button(self, key) -> None:
        button = self._get_button_from_key(key)
        button.configure(fg_color=['#325882', '#14375e'])

    def _remove_button_highlight(self, key: str) -> None:
        button = self._get_button_from_key(key)
        button.configure(fg_color='white') if self._is_white_key(key) else button.configure(fg_color='black')

    def _add_keyboard_text(self) -> None:
        for key in self.key_map:
            button = self._get_button_from_key(key)
            if self._is_white_key(key):
                text = key + '\n' + self.key_map[key][0].upper()
                text_color = 'black'
            else:
                text = key
                text_color = 'white'
            button.configure(text=text, text_color=text_color, anchor=tkinter.S)

    def _remove_keyboard_text(self) -> None:
        for key in self.key_map:
            button = self._get_button_from_key(key)
            if self._is_white_key(key):
                button.configure(text=self.key_map[key][0].upper(), anchor=tkinter.S)
            else:
                button.configure(text='')

    def _load_image_names(self) -> None:
        for image in os.listdir(f'{self.images_path}'):
            if '.png' in image:
                self._set_image_name(image.rsplit('.', 1)[0])

    def _set_image_name(self, image_name) -> None:
        setattr(self, f'{image_name}_image', f'{self.images_path}/{image_name}.png')

    @staticmethod
    def _create_control_button(frame: customtkinter.CTkFrame, text: str, command: Any, side: Optional[str] = None,
                               **kwargs: Any) -> None:
        customtkinter.CTkButton(frame, text=text, fg_color='#1f538d', border_color='gray13',
                                border_width=1, command=command, **kwargs).pack(side=side, fill=tkinter.BOTH)

    @staticmethod
    def _create_label(frame: customtkinter.CTkFrame, text: str, image: Optional[customtkinter.CTkImage] = None,
                      **kwargs: Optional[Any]) -> None:
        data = {'text': text, 'image': image} if image else {'text': text}
        customtkinter.CTkLabel(frame, **data).pack(**kwargs)

    def _get_button_from_key(self, key: str) -> customtkinter.CTkButton:
        return getattr(self, f'{key}_key')

    def _add_key_names(self, button: customtkinter.CTkButton, key: str) -> None:
        if self._is_white_key(key):
            button.configure(text=self.key_map[key][0].upper(), text_color='black', anchor=tkinter.S)
