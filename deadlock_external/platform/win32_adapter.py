"""Win32 platform adapter — process attach, module lookup, memory R/W.

Uses ctypes so no external native deps are required. Educational use only.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import struct
import sys

PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400


class Win32Adapter:
    def __init__(self, process_name: str = "deadlock.exe") -> None:
        self.process_name = process_name
        self._handle: int | None = None
        self._pid: int | None = None
        self._k32 = ctypes.WinDLL("kernel32", use_last_error=True)

    @staticmethod
    def is_supported() -> bool:
        return sys.platform == "win32"

    def _find_pid(self) -> int | None:
        import subprocess
        try:
            out = subprocess.check_output(
                ["tasklist", "/FI", f"IMAGENAME eq {self.process_name}", "/FO", "CSV", "/NH"],
                text=True, stderr=subprocess.DEVNULL,
            )
        except Exception:
            return None
        for line in out.splitlines():
            parts = [p.strip('"') for p in line.split('","')]
            if len(parts) >= 2 and parts[0].lower() == self.process_name.lower():
                try:
                    return int(parts[1])
                except ValueError:
                    continue
        return None

    def attach(self) -> bool:
        pid = self._find_pid()
        if pid is None:
            return False
        access = PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION
        h = self._k32.OpenProcess(access, False, pid)
        if not h:
            return False
        self._pid, self._handle = pid, h
        return True

    def detach(self) -> None:
        if self._handle:
            self._k32.CloseHandle(self._handle)
        self._handle = None
        self._pid = None

    def read(self, address: int, size: int) -> bytes | None:
        if not self._handle:
            return None
        buf = ctypes.create_string_buffer(size)
        read = wt.SIZE_T(0)
        ok = self._k32.ReadProcessMemory(self._handle, ctypes.c_void_p(address), buf, size, ctypes.byref(read))
        return buf.raw if ok else None

    def read_ptr(self, address: int) -> int | None:
        raw = self.read(address, 8)
        return struct.unpack("<Q", raw)[0] if raw else None

    def write(self, address: int, data: bytes) -> bool:
        if not self._handle:
            return False
        written = wt.SIZE_T(0)
        return bool(self._k32.WriteProcessMemory(self._handle, ctypes.c_void_p(address), data, len(data), ctypes.byref(written)))