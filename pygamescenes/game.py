from __future__ import annotations
import abc
from typing import Optional
import pygame
from . import constants as _constants

class AbstractGame(abc.ABC):
    " abstract game class "
    scr: pygame.surface.Surface # display surface
    scr_size: tuple[int, int] # screen size
    scr_is_real: bool # whether self.scr is the real display surface
    entities: pygame.sprite.Group
    running: bool # is game running
    time: float # game running time
    
    def __init__(self,
                 scr_size: tuple[int,int]=(256,256),
                 dpy_flags: int=0, *,
                 open_window: bool=False,
                 screen: Optional[pygame.Surface]=None) -> None:
        self.running = False
        self.scr_size = scr_size
        if open_window:
            self.scr = pygame.display.set_mode(scr_size, dpy_flags)
            self.scr_is_real = True
        elif screen is not None:
            self.scr = screen
            self.scr_is_real = False
            self.scr_size = self.scr.size
        else:
            self.scr_is_real = False
    
    @abc.abstractmethod
    def init(self, *args, **kwargs) -> None:
        " initialise this game "
        pass
    @abc.abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        " process event "
        if event.type == _constants.EventIDs.QUIT:
            self.running = False
    @abc.abstractmethod
    def update_frame(self, dt: float=1/60) -> None:
        " update entity positions for this frame. `dt` is seconds passed "
        self.time += dt
    @abc.abstractmethod
    def update_tick(self) -> None:
        " update entities and logic "
        pass
    @abc.abstractmethod
    def render_frame(self) -> pygame.surface.Surface:
        " render current frame and return it "
        if self.scr_is_real: pygame.display.flip()
        return self.scr
    @abc.abstractmethod
    def cleanup(self) -> int:
        " clean up this game and return the return code "
        pygame.quit()
    
    @property
    def scr_w(self) -> int:
        return self.scr_size[0]
    @property
    def scr_h(self) -> int:
        return self.scr_size[1]

class BaseGame(AbstractGame):
    " basic game class, with basic quality-of-life functionality "
    backdrop: pygame.surface.Surface
    rendered: pygame.sprite.Group
    updated: pygame.sprite.Group
    ticked: pygame.sprite.Group
    def __init__(self,
                 scr_size: tuple[int,int]=(256,256),
                 dpy_flags: int=0, *,
                 open_window: bool=False,
                 screen: Optional[pygame.Surface]=None) -> None:
        super().__init__(scr_size, dpy_flags, open_window, screen)
        self.backdrop = pygame.Surface(scr_size)
        self.rendered = pygame.sprite.Group()
        self.updated  = pygame.sprite.Group()
        self.ticked   = pygame.sprite.Group()
    @abc.abstractmethod
    def render_frame(self) -> pygame.surface.Surface:
        self.scr.blit(self.backdrop, (0,0))
        for entity in self.rendered:
            entity.render(self.scr)
        return self.scr
    @abc.abstractmethod
    def update_frame(self, dt: float=1/60) -> None:
        for entity in self.ticked:
            entity.update()
    @abc.abstractmethod
    def update_tick(self) -> None:
        for entity in self.ticked:
            if entity not in self.entities:
                self.entities.add(entity) # add unknown entity to entities list
            entity.tick()
