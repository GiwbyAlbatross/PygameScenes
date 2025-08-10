" an object-oriented interface for making simple to complex pygame games "
# intentionally left otherwise blank (for now)

import pygame

from . import game
from . import scene
from . import entity

def run_game(game: game.AbstractGame, *init_args, **init_kwargs) -> int:
    game.init(*init_args, **init_kwargs)
    while game.runing:
        game.process_events(pygame.event.get())
        game.render_frame()
        pygame.display.flip()
    game.cleanup()
