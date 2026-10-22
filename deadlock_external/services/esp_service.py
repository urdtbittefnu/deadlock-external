"""ESP service — projects entity world positions to screen coordinates."""
from __future__ import annotations

import math
from dataclasses import dataclass

from deadlock_external.config.loader import EspConfig
from deadlock_external.services.entity_service import Entity, EntityService


@dataclass
class ScreenBox:
    x: float
    y: float
    w: float
    h: float
    entity: Entity


class EspService:
    def __init__(self, entities: EntityService, cfg: EspConfig) -> None:
        self.entities = entities
        self.cfg = cfg
        self._view_matrix: list[float] = [0.0] * 16
        self._screen = (1920, 1080)

    def update_view(self, matrix: list[float], screen: tuple[int, int]) -> None:
        self._view_matrix = matrix
        self._screen = screen

    def _project(self, world: tuple[float, float, float]) -> tuple[float, float] | None:
        m = self._view_matrix
        x = world[0] * m[0] + world[1] * m[4] + world[2] * m[8] + m[12]
        y = world[0] * m[1] + world[1] * m[5] + world[2] * m[9] + m[13]
        w = world[0] * m[3] + world[1] * m[7] + world[2] * m[11] + m[15]
        if w < 0.01:
            return None
        sw, sh = self._screen
        return ((x / w + 1.0) * 0.5 * sw, (1.0 - y / w) * 0.5 * sh)

    def boxes(self) -> list[ScreenBox]:
        if not self.cfg.enabled:
            return []
        local = self.entities.local_player()
        out: list[ScreenBox] = []
        for e in self.entities._cache:
            if local and e.team == local.team:
                continue
            top = self._project(e.head)
            bot = self._project(e.origin)
            if not top or not bot:
                continue
            h = abs(bot[1] - top[1])
            w = h * 0.55
            out.append(ScreenBox(top[0] - w / 2, top[1], w, h, e))
        return out

    def distance(self, a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        return math.dist(a, b)