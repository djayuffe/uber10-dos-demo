#!/usr/bin/env python3
"""Run the demo in an emulated 16-bit CPU (Unicorn), entered the way DOS enters a .COM."""
import pathlib, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INSN, UC_HOOK_INTR, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import *

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEG = 0x1000
LIN = SEG << 4
fails = []

def check(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok: fails.append(msg)

class Run:
    """One .COM in the emulator, entered the way DOS enters it (AX = 0)."""
    def __init__(self, name, esc_after=None):
        self.com = (ROOT / name).read_bytes()
        uc = self.uc = Uc(UC_ARCH_X86, UC_MODE_16)
        uc.mem_map(0, 0x10000); uc.mem_map(LIN, 0x10000); uc.mem_map(0xA0000, 0x10000)
        uc.mem_write(LIN + 0x100, self.com)
        uc.mem_write(LIN, b"\xCD\x20")                        # PSP: INT 20h
        for r in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS): uc.reg_write(r, SEG)
        uc.reg_write(UC_X86_REG_SP, 0xFFFE); uc.reg_write(UC_X86_REG_FLAGS, 0x202)
        uc.reg_write(UC_X86_REG_AX, 0)
        self.esc_after, self.polls, self.vs = esc_after, 0, 0
        self.modes, self.chars, self.frames, self.unmapped = [], [], [], []
        self.dac, self.idx, self.sub, self.cur, self.exited = {}, 0, 0, [0, 0, 0], False
        self.dac_writes = 0
        self.poll_hooks = []
        uc.hook_add(UC_HOOK_INSN, self.on_in, None, 1, 0, UC_X86_INS_IN)
        uc.hook_add(UC_HOOK_INSN, self.on_out, None, 1, 0, UC_X86_INS_OUT)
        uc.hook_add(UC_HOOK_INTR, self.on_intr)
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, lambda u, a, ad, sz, v, d: self.unmapped.append(hex(ad)) or False)

    def on_in(self, uc, port, size, ud):
        if port == 0x3DA:
            self.vs += 1
            return 8 if (self.vs // 2) % 2 else 0
        if port == 0x60:
            self.polls += 1
            for h in self.poll_hooks: h(uc)
            self.frames.append(bytes(uc.mem_read(0xA0000, 64000)))
            return 1 if self.esc_after is not None and self.polls > self.esc_after else 0
        return 0

    def on_out(self, uc, port, size, v, ud):
        v &= 0xFF
        if port == 0x3C9: v &= 63                     # the DAC keeps 6 bits
        if port == 0x3C8: self.idx, self.sub = v, 0
        elif port == 0x3C9:
            self.dac_writes += 1
            self.cur[self.sub] = v; self.sub += 1
            if self.sub == 3:
                self.dac[self.idx] = tuple(self.cur); self.idx, self.sub = (self.idx + 1) & 255, 0

    def on_intr(self, uc, n, ud):
        ax = uc.reg_read(UC_X86_REG_AX)
        if n == 0x10: self.modes.append(ax & 0xFF)
        elif n == 0x29: self.chars.append(ax & 0xFF)
        elif n == 0x20: self.exited = True; uc.emu_stop()

    def run(self, instructions=None, slice_=2_000_000, budget=3_000_000_000):
        used, started = 0, False
        limit = instructions or budget
        while not self.exited and used < limit:
            n = min(slice_, limit - used)
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_IP) if started else 0x100, 0xFFFF0, count=n)
            started = True; used += n
        return self

# ------------------------------------------------------------------- UBER10
from unicorn import UC_HOOK_CODE
print("== UBER10.COM (16-byte class) ==")
r = Run("UBER10.COM")
check(len(r.com) <= 16, f"fits the 16-byte class ({len(r.com)} bytes)")
check(len(r.com) <= 10, "and has not grown past its 10-byte budget")
check(r.com[0] == 0xF4, "starts with HLT (sleep until the next timer tick)")
r.uc.mem_write(LIN + 0x100, b"\x90")                     # emulate the timer tick: HLT -> NOP, counted below
ticks = []
r.uc.hook_add(UC_HOOK_CODE, lambda uc, addr, size, ud: ticks.append(len(r.chars)), None, LIN + 0x100, LIN + 0x100)
r.run(instructions=20000)
check(not r.modes, "sets no video mode: it relies on DOS's default 80x25 text mode")
check(len(ticks) > 100, f"waits for a tick before every burst ({len(ticks)} ticks)")
bursts = [b - a for a, b in zip(ticks, ticks[1:])]
check(set(bursts) == {8}, f"prints exactly 8 characters per tick (bursts {sorted(set(bursts))})")
check(r.chars[0] == 0 and all((b - a) % 256 == 1 for a, b in zip(r.chars, r.chars[1:])),
      "starts at code 0 (AX = 0 at entry) and counts up by one, wrapping at 256")
check(set(r.chars[:256]) == set(range(256)), "the first 256 characters are all 256 distinct codes")
check(7 in r.chars[:256], "includes BEL (07h): it beeps")
rate = 8 * 18.2
check(100 < rate < 200, f"at the 18.2 Hz timer that is {rate:.0f} characters a second: scrolls, and readable")
check(not r.unmapped, "touches no memory outside the program segment")

print("\nRESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED:\n  - " + "\n  - ".join(fails))
sys.exit(1 if fails else 0)
