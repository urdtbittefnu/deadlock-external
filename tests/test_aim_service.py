"""Unit tests for AimService math (no live process required)."""
from __future__ import annotations

import math
import unittest

from deadlock_external.config.loader import AimConfig
from deadlock_external.services.aim_service import AimService, Vec2
from deadlock_external.utils.vectors import normalize_angle


class _FakeMem:
    def read_ptr(self, _): return None
    def read_i32(self, _): return None
    def read_f32(self, _): return None
    def read_vec3(self, _): return None
    module_base = 0


class _FakeEntities:
    def local_player(self): return None
    def refresh(self): return []


class AimServiceTests(unittest.TestCase):
    def setUp(self):
        self.svc = AimService(_FakeMem(), _FakeEntities(), AimConfig(fov=10.0, smooth=4.0))

    def test_no_target_when_no_local_player(self):
        self.assertIsNone(self.svc.best_target((0, 0, 0), Vec2(0, 0)))

    def test_smooth_step_moves_toward_target(self):
        out = self.svc.smooth_step(Vec2(0.0, 0.0), (40.0, 20.0))
        self.assertAlmostEqual(out.x, 10.0)
        self.assertAlmostEqual(out.y, 5.0)

    def test_normalize_angle(self):
        self.assertAlmostEqual(normalize_angle(370.0), 10.0)
        self.assertAlmostEqual(normalize_angle(-190.0), 170.0)


if __name__ == "__main__":
    unittest.main()