"""Entry point / bootstrap for deadlock-external.

Loads config, initializes platform adapter (Windows), wires services,
then hands control to the overlay loop. Educational use only.
"""
from __future__ import annotations

import logging
import sys

from deadlock_external.config.loader import load_config
from deadlock_external.platform.win32_adapter import Win32Adapter
from deadlock_external.services.memory_service import MemoryService
from deadlock_external.services.entity_service import EntityService
from deadlock_external.services.aim_service import AimService
from deadlock_external.services.esp_service import EspService
from deadlock_external.overlay.renderer import OverlayRenderer

log = logging.getLogger("deadlock_external")


def bootstrap() -> int:
    cfg = load_config()
    logging.basicConfig(level=cfg.log_level, format="[%(asctime)s] %(name)s %(levelname)s: %(message)s")

    if not Win32Adapter.is_supported():
        log.error("deadlock-external requires Windows 10/11 x64")
        return 1

    adapter = Win32Adapter(process_name=cfg.process_name)
    if not adapter.attach():
        log.error("could not attach to %s — is Deadlock running?", cfg.process_name)
        return 2

    memory = MemoryService(adapter)
    entities = EntityService(memory)
    aim = AimService(memory, entities, cfg.aim)
    esp = EspService(entities, cfg.esp)

    renderer = OverlayRenderer(esp_service=esp, aim_service=aim, cfg=cfg.overlay)
    try:
        renderer.run()
    except KeyboardInterrupt:
        log.info("shutdown requested")
    finally:
        adapter.detach()
    return 0


if __name__ == "__main__":
    sys.exit(bootstrap())