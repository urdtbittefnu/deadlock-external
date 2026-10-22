"""Patch-sensitive offset table for deadlock-external.

Update after every Deadlock patch. Values are placeholders — verify
against your own reversing notes before use.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Offsets:
    build: str = "2026-01-14"
    entity_list: int = 0x1A2B3C40
    local_player: int = 0x1A2B3C00
    view_matrix: int = 0x1A2B3D80
    view_angles: int = 0x1A2B3D90
    entity_stride: int = 0x78
    health: int = 0x10
    team: int = 0x14
    origin: int = 0x30
    head: int = 0x3C


DEFAULT = Offsets()