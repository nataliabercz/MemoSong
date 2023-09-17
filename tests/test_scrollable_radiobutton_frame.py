import unittest
from mock import patch
from scrollable_radiobutton_frame import ScrollableRadiobuttonFrame
from test_memo_song_data import *


class TestScrollableRadiobuttonFrame(unittest.TestCase):
    def setUp(self) -> None:
        self.root = customtkinter.CTk()
        self.scrollable_radiobutton_frame_cls = ScrollableRadiobuttonFrame(self.root, [], 'recordings', 'command')

    @patch.object(ScrollableRadiobuttonFrame, 'add_item')
    def test_update_list_one_item(self, mock_add_item: MagicMock) -> None:
        self.scrollable_radiobutton_frame_cls.update_list(['file'])
        mock_add_item.assert_called_once_with('file')

    @patch.object(ScrollableRadiobuttonFrame, 'add_item')
    def test_update_list_multiple_items(self, mock_add_item: MagicMock) -> None:
        self.scrollable_radiobutton_frame_cls.update_list(['file1', 'file2'])
        mock_add_item.assert_has_calls([call('file1'), call('file2')])

    def test_add_item_empty(self) -> None:
        self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list = []
        self.scrollable_radiobutton_frame_cls.add_item('file')
        mock_tkinter_radiobutton_1.pack.assert_called_once_with(anchor='w')
        mock_tkinter_radiobutton_1.configure.assert_called_once_with(command='command')
        self.assertEqual(self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list,
                         [mock_tkinter_radiobutton_1])

    def test_add_item_not_empty(self) -> None:
        self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list = not_empty_radiobutton_list
        mock_tkinter_radiobutton_3 = MagicMock()
        customtkinter.CTkRadioButton = MagicMock(return_value=mock_tkinter_radiobutton_3)
        self.scrollable_radiobutton_frame_cls.add_item('file')
        mock_tkinter_radiobutton_3.pack.assert_called_once_with(anchor='w')
        mock_tkinter_radiobutton_3.configure.assert_called_once_with(command='command')
        self.assertEqual(self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list,
                         [mock_tkinter_radiobutton_1, mock_tkinter_radiobutton_2, mock_tkinter_radiobutton_3])

    def test_clear_list_empty(self) -> None:
        self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list = []
        self.scrollable_radiobutton_frame_cls.clear_list()
        mock_tkinter_radiobutton_1.destroy.assert_not_called()
        self.assertEqual(self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list, [])

    def test_clear_list_not_empty(self) -> None:
        self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list = not_empty_radiobutton_list
        self.scrollable_radiobutton_frame_cls.clear_list()
        mock_tkinter_radiobutton_1.destroy.assert_called_once_with()
        self.assertEqual(self.scrollable_radiobutton_frame_cls.recordings_radiobutton_list, [])

    def test_get_selected_item(self) -> None:
        self.scrollable_radiobutton_frame_cls.radiobutton_var.get = MagicMock(return_value='file')
        selected_item = self.scrollable_radiobutton_frame_cls.get_selected_item()
        self.scrollable_radiobutton_frame_cls.radiobutton_var.get.assert_called_once_with()
        self.assertEqual(selected_item, 'file')

    def test_remove_item_selection(self) -> None:
        self.scrollable_radiobutton_frame_cls.radiobutton_var.set = MagicMock()
        self.scrollable_radiobutton_frame_cls.remove_item_selection()
        self.scrollable_radiobutton_frame_cls.radiobutton_var.set.assert_called_once_with('0')
