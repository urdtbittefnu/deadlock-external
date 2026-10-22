"""Memory service — wraps platform adapter with typed reads and chain walking."""
from __future__ import annotations

import struct
from typing import Optional

from deadlock_external.platform.win32_adapter import Win32Adapter


class MemoryService:
    def __init__(self, adapter: Win32Adapter) -> None:
        self.adapter = adapter
        self._module_base: int | None = None

    @property
    def module_base(self) -> Optional[int]:
        return self._module_base

    def set_module_base(self, base: int) -> None:
        self._module_base = base

    def read_i32(self, addr: int) -> Optional[int]:
        raw = self.adapter.read(addr, 4)
        return struct.unpack("<i", raw)[0] if raw else None

    def read_f32(self, addr: int) -> Optional[float]:
        raw = self.adapter.read(addr, 4)
        return struct.unpack("<f", raw)[0] if raw else None

    def read_vec3(self, addr: int) -> Optional[tuple[float, float, float]]:
        raw = self.adapter.read(addr, 12)
        return struct.unpack("<fff", raw) if raw else None

    def read_ptr(self, addr: int) -> Optional[int]:
        return self.adapter.read_ptr(addr)

    def walk_chain(self, base: int, offsets: list[int]) -> Optional[int]:
        cur = base
        for off in offsets[:-1]:
            nxt = self.read_ptr(cur + off)
            if not nxt:
                return None
            cur = nxt
        return cur + offsets[-1]