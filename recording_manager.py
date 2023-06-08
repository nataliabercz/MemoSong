import os
import time
import pygame
from typing import Any
from key_player import KeyPlayer
from piano_recorder import PianoRecorder
from voice_recorder import VoiceRecorder
from file_manager import FileManager


class RecordingManager(FileManager):
    key_player = KeyPlayer()
    piano_recorder = PianoRecorder()
    voice_recorder = VoiceRecorder()
    file_manager = FileManager()

    def play_recording(self) -> None:
        FileManager.current_browser_type = 'recordings'
        try:
            if song := self._get_curselection_from_radiobutton_list(self.recordings_radiobutton_list):
                self._remove_selection_from_radiobutton_list(self.notes_radiobutton_list)
                pygame.mixer.music.load(f'{self.app_path}/recordings/{song}')
                pygame.mixer.music.play()
        except pygame.error:
            self._display_message_box('ERROR', f'Invalid file!', False, 300)

    def start_piano_recording(self) -> None:
        self.start_recording('piano')

    def start_voice_recording(self) -> None:
        self.start_recording('voice')

    def pause_piano_recording(self) -> None:
        self.pause_recording('piano')

    def pause_voice_recording(self) -> None:
        self.pause_recording('voice')

    def stop_piano_recording(self) -> None:
        self.stop_recording('piano')

    def stop_voice_recording(self) -> None:
        self.stop_recording('voice')

    def start_recording(self, recording_type: str) -> None:
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
                    self._setup_recorder(recorder, recording_type, title)
                    self._mute_playback()
                    os.remove(f'{self.app_path}/recordings/{title}')
                    self.update_list('recordings') # it would be better to remove only 1 item from this list
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

    def pause_recording(self, recording_type: str) -> None:
        recorder = getattr(self, f'{recording_type}_recorder')
        if recorder.paused:
            self._setup_pause(recorder, recording_type, 'off')
            return
        self._setup_pause(recorder, recording_type, 'on')

    def _setup_pause(self, recorder: Any, recording_type: str, option: str) -> None:
        self._highlight_used_function(f'pause_{recording_type}_recording', option)
        recorder.paused = True if option == 'on' else False

    def stop_recording(self, recording_type: str) -> None:
        recorder = getattr(self, f'{recording_type}_recorder')
        if recorder.recording:
            self._highlight_used_function(f'start_{recording_type}_recording', 'off')
            recorder.recording = False
            self.recordings_radiobutton_list.add_item(getattr(self, f'{recording_type}_recording_title'))
