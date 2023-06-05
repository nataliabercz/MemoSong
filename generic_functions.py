import os
import datetime
import pygame
import tkinter
import customtkinter
import CTkMessagebox
from PIL import Image
from typing import Tuple, Optional, Any
from scrollable_radiobutton_frame import ScrollableRadiobuttonFrame


class GenericFunctions:
    width = 1000
    height = 535
    title = 'MemoSong'
    key_map = {'q': 'c3', '2': 'c#3', 'w': 'd3', '3': 'd#3', 'e': 'e3', 'r': 'f3', '5': 'f#3', 't': 'g3', '6': 'g#3',
               'y': 'a3', '7': 'a#3', 'u': 'b3', 'i': 'c4', '9': 'c#4', 'o': 'd4', '0': 'd#4', 'p': 'e4', '[': 'f4',
               '=': 'f#4', ']': 'g4', 'a': 'g#4', 'z': 'a4', 's': 'a#4', 'x': 'b4', 'c': 'c5', 'f': 'c#5', 'v': 'd5',
               'g': 'd#5', 'b': 'e5', 'n': 'f5', 'j': 'f#5', 'm': 'g5', 'k': 'g#5', ',': 'a5', 'l': 'a#5', '.': 'b5',
               '/': 'c6'}
    app_path = os.path.dirname(os.path.realpath(__file__))
    images_path = f'{app_path}/data/images'
    keys_path = f'{app_path}/data/keys'

    def _is_white_key(self, key: str) -> bool:
        return '#' not in self.key_map[key]

    def _get_filename(self, filename: str, browser_type: str, prefix: Optional[str] = '') -> str:
        if not self._directory_exists(browser_type):
            self._create_directory(browser_type)
        if filename == '':
            filename = f'{prefix}{browser_type[0:-1]}_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        return f'{filename}.{self._get_extension(browser_type)}'

    @staticmethod
    def _get_extension(browser_type: str) -> str:
        return 'txt' if browser_type == 'notes' else 'wav'

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
                                  command: Any, side: tkinter.constants, width: Optional[int] = None) -> None:
        if not width:
            width = image_size[0]
        button = customtkinter.CTkButton(frame, text='', width=width, command=command,
                                         image=self._open_image(f'{button_name}_image', image_size))
        button.pack(side=side)
        setattr(self, f'{button_name}_button', button)

    @staticmethod
    def _get_curselection_from_radiobutton_list(radiobutton_list: ScrollableRadiobuttonFrame) -> str:
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
                'icon_size': (30, 30), 'icon': 'warning'}
        if options:
            data.update({'option_1': 'No', 'option_2': 'Yes'})
        return CTkMessagebox.CTkMessagebox(**data)
