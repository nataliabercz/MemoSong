import tkinter
import customtkinter
from typing import List


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    recordings_radiobutton_list = []
    notes_radiobutton_list = []

    def __init__(self, master, item_list, browser_type, command, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.radiobutton_var = customtkinter.StringVar()
        self.browser_type = browser_type
        self.command = command
        self.update_list(item_list)

    def update_list(self, item_list: List[str]) -> None:
        for item in item_list:
            self.add_item(item)

    def add_item(self, item: str) -> None:
        radiobutton_list = getattr(self, f'{self.browser_type}_radiobutton_list')
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_var,
                                                   font=('Roboto', 10), radiobutton_width=8, radiobutton_height=8)
        radiobutton.pack(anchor=tkinter.W)
        radiobutton.configure(command=self.command)
        radiobutton_list.append(radiobutton)

    def clear_list(self) -> None:
        radiobutton_list = getattr(self, f'{self.browser_type}_radiobutton_list')
        for radiobutton in radiobutton_list:
            radiobutton.destroy()
        setattr(self, f'{self.browser_type}_radiobutton_list', [])

    def get_selected_item(self) -> str:
        return self.radiobutton_var.get()

    def remove_item_selection(self) -> None:
        self.radiobutton_var.set('0')
