from __future__ import annotations
import pygame
import abc

class AbstractEntity(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    surf: pygame.Surface
    rect: pygame.rect.Rect | pygame.rect.FRect
    mv: pygame.math.Vector2 # pixels per second, retains speed despite FPS
    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
    @abc.abstractmethod
    def tick(self) -> None:
        " tick this entity, do complex logic etc "
        pass
    @abc.abstractmethod
    def update(self, dt: float=1/60) -> None:
        " update this entity's position and other per-frame stuff, `dt` is in seconds "
        self.rect.move_ip(self.mv*dt)
    def render(self, surf: pygame.Surface) -> pygame.Rect:
        " render this entity onto `surf` and return pixels changed "
        return surf.blit(self.surf, self.rect)
