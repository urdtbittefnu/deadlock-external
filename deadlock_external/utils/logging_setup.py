"""Logging helpers."""
from __future__ import annotations

import logging
import sys


def setup(level: str = "INFO") -> None:
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(logging.Formatter("[%(asctime)s] %(name)s %(levelname)s: %(message)s"))
    root = logging.getLogger("deadlock_external")
    root.setLevel(level.upper())
    root.addHandler(h)