from mock import call, MagicMock
import tkinter
import customtkinter
import CTkMessagebox
import pyaudio

mock_tkinter_frame = MagicMock()
customtkinter.CTkFrame = MagicMock(return_value=mock_tkinter_frame)
mock_tkinter_label = MagicMock()
customtkinter.CTkLabel = MagicMock(return_value=mock_tkinter_label)
mock_tkinter_button = MagicMock()
customtkinter.CTkButton = MagicMock(return_value=mock_tkinter_button)
mock_tkinter_entry = MagicMock()
customtkinter.CTkEntry = MagicMock(return_value=mock_tkinter_entry)
mock_tkinter_image = MagicMock()
customtkinter.CTkImage = MagicMock(return_value=mock_tkinter_image)
mock_tkinter_textbox = MagicMock()
customtkinter.CTkTextbox = MagicMock(return_value=mock_tkinter_textbox)
mock_tkinter_input_dialog = MagicMock()
customtkinter.CTkInputDialog = MagicMock(return_value=mock_tkinter_input_dialog)
mock_tkinter_messagebox = MagicMock()
CTkMessagebox.CTkMessagebox = MagicMock(return_value=mock_tkinter_messagebox)
mock_tkinter_radiobutton1 = MagicMock()
mock_tkinter_radiobutton2 = MagicMock()
customtkinter.CTkRadioButton = MagicMock(side_effect=[mock_tkinter_radiobutton1, mock_tkinter_radiobutton2])
not_empty_radiobutton_list = [mock_tkinter_radiobutton1, mock_tkinter_radiobutton2]

mock_event = MagicMock()
tkinter.Event = MagicMock(return_value=mock_event)

mock_pyaudio = MagicMock()
pyaudio.PyAudio = MagicMock(return_value=mock_pyaudio)
mock_stream = mock_pyaudio.open

is_white_key = 3 * [True, False, True, False, True, True, False, True, False, True, False, True] + [True]

calls_each_key = [
    call('q'), call('2'), call('w'), call('3'), call('e'), call('r'), call('5'), call('t'), call('6'), call('y'),
    call('7'), call('u'), call('i'), call('9'), call('o'), call('0'), call('p'), call('['), call('='), call(']'),
    call('a'), call('z'), call('s'), call('x'), call('c'), call('f'), call('v'), call('g'), call('b'), call('n'),
    call('j'), call('m'), call('k'), call(','), call('l'), call('.'), call('/')
]

white_key_kwargs = {'fg_color': 'white', 'width': 47, 'height': 225, 'border_width': 1, 'border_color': 'black'}
black_key_kwargs = {'fg_color': 'black', 'width': 22, 'height': 140}
calls_configure_piano = [
    call(mock_tkinter_frame, 'q', 5, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'w', 50, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'e', 95, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'r', 140, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 't', 185, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'y', 230, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'u', 275, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'i', 320, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'o', 365, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'p', 410, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, '[', 455, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, ']', 500, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'z', 545, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'x', 590, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'c', 635, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'v', 680, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'b', 725, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'n', 770, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, 'm', 815, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, ',', 860, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, '.', 905, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, '/', 950, 3, 5, **white_key_kwargs),
    call(mock_tkinter_frame, '2', 40, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '3', 85, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '5', 175, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '6', 220, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '7', 265, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '9', 355, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '0', 400, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, '=', 490, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 'a', 535, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 's', 580, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 'f', 670, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 'g', 715, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 'j', 805, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 'k', 850, 4, 26, **black_key_kwargs),
    call(mock_tkinter_frame, 'l', 895, 4, 26, **black_key_kwargs)
]

calls_load_image_names = [
    call('idle'), call('keyboard'), call('logo'), call('mute'), call('pause_piano_recording'),
    call('pause_voice_recording'), call('playing'), call('start_piano_recording'), call('start_voice_recording'),
    call('stop_piano_recording'), call('stop_voice_recording')
]

calls_add_keyboard_text = [
    call(text='q\nC', text_color='black', anchor='s'), call(text='2', text_color='white', anchor='s'),
    call(text='w\nD', text_color='black', anchor='s'), call(text='3', text_color='white', anchor='s'),
    call(text='e\nE', text_color='black', anchor='s'), call(text='r\nF', text_color='black', anchor='s'),
    call(text='5', text_color='white', anchor='s'), call(text='t\nG', text_color='black', anchor='s'),
    call(text='6', text_color='white', anchor='s'), call(text='y\nA', text_color='black', anchor='s'),
    call(text='7', text_color='white', anchor='s'), call(text='u\nB', text_color='black', anchor='s'),
    call(text='i\nC', text_color='black', anchor='s'), call(text='9', text_color='white', anchor='s'),
    call(text='o\nD', text_color='black', anchor='s'), call(text='0', text_color='white', anchor='s'),
    call(text='p\nE', text_color='black', anchor='s'), call(text='[\nF', text_color='black', anchor='s'),
    call(text='=', text_color='white', anchor='s'), call(text=']\nG', text_color='black', anchor='s'),
    call(text='a', text_color='white', anchor='s'), call(text='z\nA', text_color='black', anchor='s'),
    call(text='s', text_color='white', anchor='s'), call(text='x\nB', text_color='black', anchor='s'),
    call(text='c\nC', text_color='black', anchor='s'), call(text='f', text_color='white', anchor='s'),
    call(text='v\nD', text_color='black', anchor='s'), call(text='g', text_color='white', anchor='s'),
    call(text='b\nE', text_color='black', anchor='s'), call(text='n\nF', text_color='black', anchor='s'),
    call(text='j', text_color='white', anchor='s'), call(text='m\nG', text_color='black', anchor='s'),
    call(text='k', text_color='white', anchor='s'), call(text=',\nA', text_color='black', anchor='s'),
    call(text='l', text_color='white', anchor='s'), call(text='.\nB', text_color='black', anchor='s'),
    call(text='/\nC', text_color='black', anchor='s')
]

calls_remove_keyboard_text = [
    call(text='C', anchor='s'), call(text=''), call(text='D', anchor='s'), call(text=''),
    call(text='E', anchor='s'), call(text='F', anchor='s'), call(text=''), call(text='G', anchor='s'),
    call(text=''), call(text='A', anchor='s'), call(text=''), call(text='B', anchor='s'),
    call(text='C', anchor='s'), call(text=''), call(text='D', anchor='s'), call(text=''),
    call(text='E', anchor='s'), call(text='F', anchor='s'), call(text=''), call(text='G', anchor='s'),
    call(text=''), call(text='A', anchor='s'), call(text=''), call(text='B', anchor='s'),
    call(text='C', anchor='s'), call(text=''), call(text='D', anchor='s'), call(text=''),
    call(text='E', anchor='s'), call(text='F', anchor='s'), call(text=''), call(text='G', anchor='s'),
    call(text=''), call(text='A', anchor='s'), call(text=''), call(text='B', anchor='s'),
    call(text='C', anchor='s')
]

os_error = '[WinError 123] The filename, directory name, or volume label syntax is incorrect: {} -> {}'
incorrect_file_error = 'The filename, directory name, or volume label syntax is incorrect'
file_not_found_error = '[WinError 2] The system cannot find the file specified: {}/recordings/not_existent'

stream_read_data = b'\xef\xff\xee\xff\xee\xff\xec\xff\xea\xff\xe9\xff\xe9\xff\xe9\xff\xed\xff\xed\xff\xee\xff\xee\xff' \
                   b'\xed\xff\xeb\xff\xeb\xff\xeb\xff\xeb\xff\xed\xff\xee\xff\xee\xff\xef\xff\xef\xff\xee\xff\xed\xff' \
                   b'\xec\xff\xeb\xff\xeb\xff\xeb\xff\xed\xff\xee\xff\xee\xff\xee\xff\xef\xff\xef\xff\xee\xff\xef\xff' \
                   b'\xee\xff\xec\xff\xec\xff\xec\xff\xec\xff\xec\xff\xe9\xff\xe8\xff\xe8\xff\xea\xff\xed\xff\xef\xff' \
                   b'\xef\xff\xec\xff\xe9\xff\xe9\xff\xe9\xff\xea\xff\xea\xff\xec\xff\xed\xff\xee\xff\xef\xff\xee\xff' \
                   b'\xee\xff\xed\xff\xed\xff\xef\xff\xef\xff\xef\xff\xef\xff\xed\xff\xed\xff\xec\xff\xeb\xff\xec\xff' \
                   b'\xed\xff\xed\xff\xef\xff\xef\xff\xf0\xff\xee\xff\xee\xff\xee\xff\xf0\xff\xf1\xff\xee\xff\xec\xff' \
                   b'\xea\xff\xe9\xff\xec\xff\xef\xff\xf0\xff\xef\xff\xee\xff\xee\xff\xee\xff\xef\xff\xf0\xff\xf0\xff' \
                   b'\xee\xff\xed\xff\xed\xff\xee\xff\xed\xff\xed\xff\xec\xff\xec\xff\xed\xff\xee\xff\xef\xff\xef\xff' \
                   b'\xef\xff\xed\xff\xef\xff\xee\xff\xef\xff\xf0\xff\xf1\xff\xf0\xff\xef\xff\xef\xff\xef\xff\xf0\xff' \
                   b'\xf0\xff\xf0\xff\xf0\xff\xef\xff\xf0\xff\xf0\xff\xef\xff\xef\xff\xf0\xff\xf0\xff\xf1\xff\xf0\xff' \
                   b'\xf0\xff\xf1\xff\xf0\xff\xf1\xff\xf0\xff\xf0\xff\xf0\xff\xf0\xff\xf0\xff\xf0\xff\xf1\xff\xef\xff'
