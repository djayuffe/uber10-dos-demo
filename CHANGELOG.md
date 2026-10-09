# Changelog

Pushing a `vX.Y.Z` tag runs `.github/workflows/release.yml`, which builds, tests and attaches
`UBER10.COM` to a GitHub release using that version's section below.

## [1.1.0] - 2026-10-10

### Changed
- **Fixed: it scrolled too fast to read.** v1.0.0 (`UBER8.COM`, 5 bytes) printed as fast as the
  machine allows, which on a modern emulator is an unreadable blur. It now sleeps with `HLT` until
  each 18.2 Hz timer tick and prints 8 codes per tick: about two lines a second, readable.
- **10 bytes** (was 5), so the repository is renamed `uber8-dos-demo` -> `uber10-dos-demo`, the
  binary `UBER8.COM` -> `UBER10.COM`, and its size class is now 16 bytes (a 10-byte program no
  longer fits the 8-byte class). GitHub redirects the old URL.
- The test checks the pacing: one tick before every burst, exactly 8 characters per burst.

## [1.0.0] - 2026-10-10

First release as its own repository (it started life in
[uber-tiny-demos](https://github.com/djayuffe/uber-tiny-demos), where it went 8 -> 5 bytes).

- **UBER8.COM (5 bytes) (5 bytes)**, 5 bytes: every CP437 glyph, scrolling, with sound.
- `build.sh` enforces the 8-byte class and the 5-byte budget; `tests/run_tests.sh` runs it in an
  emulated 16-bit CPU; CI and tag-driven releases on GitHub Actions.
