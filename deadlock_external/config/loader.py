"""Config loader — reads config.toml and exposes typed Config object."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AimConfig:
    enabled: bool = False
    fov: float = 4.0
    smooth: float = 6.0
    bone: str = "head"
    keybind: str = "mouse5"


@dataclass
class EspConfig:
    enabled: bool = True
    box: bool = True
    skeleton: bool = True
    health_bar: bool = True
    name_tags: bool = True
    max_distance: float = 150.0


@dataclass
class OverlayConfig:
    vsync: bool = False
    fps_cap: int = 144
    font: str = "Consolas"


@dataclass
class Config:
    process_name: str = "deadlock.exe"
    log_level: str = "INFO"
    aim: AimConfig = field(default_factory=AimConfig)
    esp: EspConfig = field(default_factory=EspConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)


def _merge(dc, raw: dict):
    for k, v in raw.items():
        if hasattr(dc, k):
            cur = getattr(dc, k)
            if hasattr(cur, "__dataclass_fields__") and isinstance(v, dict):
                _merge(cur, v)
            else:
                setattr(dc, k, v)


def load_config(path: str | Path = "config.toml") -> Config:
    cfg = Config()
    p = Path(path)
    if p.exists():
        with p.open("rb") as fh:
            _merge(cfg, tomllib.load(fh))
    return cfg