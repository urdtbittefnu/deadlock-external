"""Overlay renderer — borderless layered window, draws ESP boxes and aim assist."""
from __future__ import annotations

import time

from deadlock_external.config.loader import OverlayConfig
from deadlock_external.services.aim_service import AimService, Vec2
from deadlock_external.services.esp_service import EspService


class OverlayRenderer:
    def __init__(self, esp_service: EspService, aim_service: AimService, cfg: OverlayConfig) -> None:
        self.esp = esp_service
        self.aim = aim_service
        self.cfg = cfg
        self._running = False

    def run(self) -> None:
        self._running = True
        frame_time = 1.0 / max(1, self.cfg.fps_cap)
        while self._running:
            start = time.perf_counter()
            self._tick()
            elapsed = time.perf_counter() - start
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        boxes = self.esp.boxes()
        for b in boxes:
            self._draw_box(b.x, b.y, b.w, b.h)
        # aim assist runs alongside the overlay loop
        angles = Vec2(0.0, 0.0)
        target = self.aim.best_target((0.0, 0.0, 0.0), angles)
        if target:
            self.aim.smooth_step(angles, target)

    def _draw_box(self, x: float, y: float, w: float, h: float) -> None:
        # Placeholder — real implementation uses GDI/Direct2D via ctypes.
        pass