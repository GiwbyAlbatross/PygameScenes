" run a oopygame game "

import pygame
import argparse
import sys

pygame.init()

game_name = sys.argv[-1]
game_mod = __import__(game_name)
game_obj = getattr(game_mod, game_mod.__game__)

if __name__ == '__main__':
    try:
        # do main loop here
        scr = pygame.display.set_mode([8,8])
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: raise SystemExit
    except BaseException as be: # yes i know that's bad practise but I re-raise
        pygame.quit()           # the exception
        raise be
    finally:
        pygame.quit()
