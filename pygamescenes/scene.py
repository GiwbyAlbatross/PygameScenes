from __future__ import annotations
import abc
from typing import 
import pygame
from . import game

class AbstractScene(game.BaseGame, metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def scene_over(self) -> bool:
        return not self.running
    @abc.abstractmethod
    def cleanup(self) -> int:
        return 0

class BaseSceneRunnerGame(game.AbstractGame):
    current_scene: AbstractScene
    def process_event(self, event: pygame.event.Event) -> None:
        super().process_event(event)
        self.current_scene.process_event(event)
    def render_frame(self) -> pygame.surface.Surface:
        return self.current_scene.render_frame()
    def update_frame(self, dt: float=1/60) -> None:
        self.current_scene.update_frame(dt)
    def update_tick(self) -> None:
        self.current_scene.update_tick()
    def cleanup(self) -> int:
        self.current_scene.cleanup()
        pygame.quit()
        return 0
class SingleSceneRunnerGame(BaseSceneRunnerGame):
    def __init__(self,
                 scr_size: tuple[int,int],
                 scene: AbstractScene,
                 dpy_flags: int=0, *,
                 open_window: bool=False,
                 screen: Optional[pygame.Surface]=None) -> None:
        super().__init__(scr_size, dpy_flags, open_window, screen)
        self.current_scene = scene
    def update_tick(self) -> None:
        super().update_tick()
        if self.current_scene.scene_over:
            self.cleanup()
class MultiSceneRunnerGame(BaseSceneRunnerGame, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_next_scene(self) -> AbstractScene:
        return NotImplemented
    def update_tick(self) -> None:
        super().update_tick()
        if self.current_scene.scene_over:
            self.current_scene.cleanup()
            self.current_scene = self.get_next_scene()
class LinearSceneRunnerGame(BaseSceneRunnerGame):
    scenes: list[AbstractScene]
    i: int
    def __init__(self,
                 scr_size: tuple[int,int],
                 scenes: list[AbstractScene],
                 dpy_flags: int=0, *,
                 open_window: bool=False,
                 screen: Optional[pygame.Surface]=None) -> None:
        super().__init__(scr_size, dpy_flags, open_window, screen)
        self.scenes = scenes
        self.current_scene = scenes[0]
        self.i = 0
    def get_next_scene(self) -> AbstractScene:
        self.i += 1
        return self.scene[self.i]
