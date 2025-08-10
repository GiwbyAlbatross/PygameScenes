from __future__ import annotations
import abc
from typing import Optional, Callable
from functools import wraps
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
    TICK_EVENT: int = pygame.USEREVENT
    TICK_RATE:  int = 1000//20 # 20 ticks per second, in milliseconds
    _eventhandlers: dict[str, set[Callable]]
    
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
        self.registerhandler(self.TICK_EVENT, self.update_tick)
        pygame.time.set_timer(self.TICK_EVENT, self.TICK_RATE)
    
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
    def default_event_handler(self, event: pygame.event.Event) -> None:
        " default event handler, signature of an event handler, reports `event` to stdout "
        print("Event:", repr(event), flush=True)
    def registerhandler(self, event_id: int | _constants.EventIDs=_constants.EventIDs.KEYDOWN, handler: Callable=default_event_handler) -> None:
        " register `handler` to respond to events with ID `event_id` "
        if isinstance(event_id, _constants.EventIDs):
            event_id = event_id.value
        self._eventhandlers[event_id].add(handler)
    def handler(self, event_id: int=_constants.EventIDs.KEYDOWN) -> Callable:
        " clever decorator to register event handlers "
        def _decorator(func: Callable) -> Callable:
            self._eventhandlers[event_id].add(func)
            return func
        return _decorator
    def process_events(self, events: list[pygame.event.Event]):
        for event in events:
            self.process_event(event)
            for handler in self._eventhandlers.get(event.type, []):
                handler(event)
    
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
        super().__init__(scr_size, dpy_flags, open_window=open_window, screen=screen)
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
            entity.update(dt)
    @abc.abstractmethod
    def update_tick(self) -> None:
        for entity in self.ticked:
            if entity not in self.entities:
                self.entities.add(entity) # add unknown entity to entities list
            entity.tick()
