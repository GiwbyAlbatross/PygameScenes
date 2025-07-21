from __future__ import annotations
import pygame
import abc

class AbstractEntity(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    surf: pygame.Surface
    rect: pygame.rect.Rect | pygame.rect.FRect
