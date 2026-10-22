"""Entity service — enumerates players/entities from the game's entity list."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from deadlock_external.services.memory_service import MemoryService

log = logging.getLogger(__name__)

ENTITY_LIST_OFFSET = 0x1A2B3C40   # placeholder — update per patch
ENTITY_STRIDE = 0x78
MAX_ENTITIES = 64


@dataclass
class Entity:
    index: int
    address: int
    health: int
    team: int
    origin: tuple[float, float, float]
    head: tuple[float, float, float]
    name: str


class EntityService:
    def __init__(self, memory: MemoryService) -> None:
        self.memory = memory
        self._cache: list[Entity] = []

    def refresh(self) -> list[Entity]:
        base = self.memory.module_base
        if not base:
            return []
        list_ptr = self.memory.read_ptr(base + ENTITY_LIST_OFFSET)
        if not list_ptr:
            return []

        out: list[Entity] = []
        for i in range(MAX_ENTITIES):
            addr = list_ptr + i * ENTITY_STRIDE
            health = self.memory.read_i32(addr + 0x10)
            if health is None or not (0 < health <= 1000):
                continue
            origin = self.memory.read_vec3(addr + 0x30)
            head = self.memory.read_vec3(addr + 0x3C)
            team = self.memory.read_i32(addr + 0x14) or 0
            if origin and head:
                out.append(Entity(i, addr, health, team, origin, head, f"player_{i}"))
        self._cache = out
        return out

    def local_player(self) -> Entity | None:
        for e in self._cache:
            if e.team == self._local_team():
                return e
        return None

    def _local_team(self) -> int:
        base = self.memory.module_base
        if not base:
            return -1
        return self.memory.read_i32(base + 0x1A2B3C00) or -1