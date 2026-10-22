"""Standalone helper — dumps candidate offsets for a given module.

Run: python -m deadlock_external.scripts.dump_offsets
Educational use only.
"""
from __future__ import annotations

import argparse
import logging

from deadlock_external.platform.win32_adapter import Win32Adapter
from deadlock_external.services.memory_service import MemoryService

log = logging.getLogger("dump_offsets")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="deadlock.exe")
    ap.add_argument("--base", type=lambda x: int(x, 0), default=0x140000000)
    args = ap.parse_args()

    adapter = Win32Adapter(process_name=args.process)
    if not adapter.attach():
        log.error("attach failed")
        return 1
    mem = MemoryService(adapter)
    mem.set_module_base(args.base)
    log.info("module base: 0x%X", args.base)
    for off in (0x1A2B3C40, 0x1A2B3C00, 0x1A2B3D80):
        val = mem.read_ptr(args.base + off)
        log.info("+0x%X -> %s", off, hex(val) if val else "null")
    adapter.detach()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())