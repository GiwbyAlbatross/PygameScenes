from pygame import locals as _pyg_locals
from enum import Enum as _Enum

class EventIDs(_Enum):
    QUIT = _pyg_locals.QUIT
    KEYDOWN =  _pyg_locals.KEYDOWN
    KEYUP = _pyg_locals.KEYUP
    MOUSEMOTION = _pyg_locals.MOUSEMOTION
    MOUSEBUTTONUP = _pyg_locals.MOUSEBUTTONUP
    MOUSEBUTTONDOWN = _pyg_locals.MOUSEBUTTONDOWN
    MOUSEWHEEL = _pyg_locals.MOUSEWHEEL