"""Aim service — computes target selection and smoothed angles."""
from __future__ import annotations

import math
from dataclasses import dataclass

from deadlock_external.config.loader import AimConfig
from deadlock_external.services.entity_service import EntityService
from deadlock_external.services.memory_service import MemoryService


@dataclass
class Vec2:
    x: float
    y: float


class AimService:
    def __init__(self, memory: MemoryService, entities: EntityService, cfg: AimConfig) -> None:
        self.memory = memory
        self.entities = entities
        self.cfg = cfg

    def best_target(self, view_origin: tuple[float, float, float], view_angles: Vec2) -> tuple[float, float] | None:
        local = self.entities.local_player()
        if local is None:
            return None
        best: tuple[float, float] | None = None
        best_delta = self.cfg.fov
        for e in self.entities.refresh():
            if e.team == local.team:
                continue
            dx = e.head[0] - view_origin[0]
            dy = e.head[1] - view_origin[1]
            dz = e.head[2] - view_origin[2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            if dist <= 0.01:
                continue
            yaw = math.degrees(math.atan2(dy, dx))
            pitch = -math.degrees(math.atan2(dz, math.hypot(dx, dy)))
            d_yaw = (yaw - view_angles.x + 180) % 360 - 180
            delta = math.hypot(d_yaw, pitch - view_angles.y)
            if delta < best_delta:
                best_delta = delta
                best = (yaw, pitch)
        return best

    def smooth_step(self, current: Vec2, target: tuple[float, float]) -> Vec2:
        t = max(1.0, self.cfg.smooth)
        return Vec2(
            current.x + (target[0] - current.x) / t,
            current.y + (target[1] - current.y) / t,
        )