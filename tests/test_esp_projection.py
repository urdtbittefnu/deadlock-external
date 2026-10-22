"""Sanity tests for ESP world-to-screen projection."""
from __future__ import annotations

import unittest

from deadlock_external.config.loader import EspConfig
from deadlock_external.services.esp_service import EspService


class _FakeEntities:
    _cache = []
    def local_player(self): return None


class EspProjectionTests(unittest.TestCase):
    def setUp(self):
        self.esp = EspService(_FakeEntities(), EspConfig())
        # Identity view matrix
        self.esp.update_view(
            [1, 0, 0, 0,
             0, 1, 0, 0,
             0, 0, 1, 0,
             0, 0, 0, 1],
            (1920, 1080),
        )

    def test_center_projects_to_center(self):
        pt = self.esp._project((0.0, 0.0, 1.0))
        self.assertIsNotNone(pt)
        self.assertAlmostEqual(pt[0], 960.0)
        self.assertAlmostEqual(pt[1], 540.0)

    def test_behind_camera_returns_none(self):
        self.assertIsNone(self.esp._project((0.0, 0.0, -1.0)))


if __name__ == "__main__":
    unittest.main()