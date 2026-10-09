# UBER8

**A 5-byte DOS demo: every CP437 glyph, scrolling, with sound.**

[![CI](https://github.com/djayuffe/uber8-dos-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/djayuffe/uber8-dos-demo/actions/workflows/ci.yml)

![UBER8.COM running in DOSBox](screenshot.jpg)

Five bytes. No setup, no assets, no libraries: it prints the 256 character codes in order, forever. Smileys, card suits, punctuation, digits, letters, box drawing, with CR/LF, backspace and BEL (07h, which beeps) doing their usual things.

| | |
|---|---|
| Size | **5 bytes** (class 8; a build gate stops it growing back) |
| CPU | any (8086 and up) |
| Video | 80x25 text (the DOS default) |
| Audio | the PC speaker beeps on BEL |

## Run it

Download `UBER8.COM` from the [latest release](../../releases/latest) and run it in DOSBox
(`mount c .`, `c:`, `UBER8.COM`), or build it:

```sh
./build.sh        # NASM build + size gates
./run-dosbox.sh   # run it in DOSBox
```

Needs [NASM](https://www.nasm.us/) and [DOSBox](https://www.dosbox.com/)
(macOS: `brew install nasm` and `brew install --cask dosbox`).

**UBER8 never exits** (there are no bytes left to read the keyboard): close DOSBox, or press Ctrl+F9 in it.

## How it works

```
.l: int 29h       ; CD 29     DOS "fast console output": print AL
    inc ax        ; 40        next code
    jmp short .l  ; EB FB
```

DOS starts a `.COM` with `AX = 0` and the screen already in 80x25 text mode, so there is nothing to set
up: `INT 29h` prints `AL` and `AX` just counts. The loop itself needs two bytes, the `INT` two and the
increment one, which is why this is the floor for a printing loop. (The 8-byte version used `int 10h` to
set 40x25 mode and stepped by 83 to look random; dropping both saves three bytes.) It relies on the DOS
entry convention `AX = 0`.

## Testing

`tests/run_tests.sh` runs the real binary in an emulated 16-bit CPU (Unicorn), entered the way DOS enters
a `.COM`. It checks that the binary fits the 8-byte class, sets no video mode, prints code 0 first and then counts up by one (wrapping at 256, all 256 distinct codes, including BEL), and touches no memory outside its segment. CI runs it on every push; a `vX.Y.Z` tag publishes a release.

## Related

Part of a small family of DOS size-coding demos, each in its own repository:
[uber8-dos-demo](https://github.com/djayuffe/uber8-dos-demo) (5 bytes),
[uber128-dos-demo](https://github.com/djayuffe/uber128-dos-demo) (77 bytes),
[uber256-rotozoomer](https://github.com/djayuffe/uber256-rotozoomer) (171 bytes),
[uber256-dos-intro](https://github.com/djayuffe/uber256-dos-intro) (131 bytes), and the big one,
[uber40k-dos-demo](https://github.com/djayuffe/uber40k-dos-demo) (a 20-scene show with a 3D engine and
Sound Blaster music). The index is [uber-tiny-demos](https://github.com/djayuffe/uber-tiny-demos).

## License

MIT
