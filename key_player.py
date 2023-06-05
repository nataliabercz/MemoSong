import pygame
from generic_functions import GenericFunctions


class KeyPlayer(GenericFunctions):
    key = None

    def play_key(self) -> None:
        pygame.mixer.Sound.play(pygame.mixer.Sound(f'{self.keys_path}/{self.key_map[self.key]}.wav'))
