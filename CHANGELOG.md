# Changelog

Pushing a `vX.Y.Z` tag runs `.github/workflows/release.yml`, which builds, tests and attaches
`UBER8.COM` to a GitHub release using that version's section below.

## [1.0.0] - 2026-10-10

First release as its own repository (it started life in
[uber-tiny-demos](https://github.com/djayuffe/uber-tiny-demos), where it went 8 -> 5 bytes).

- **UBER8.COM**, 5 bytes: every CP437 glyph, scrolling, with sound.
- `build.sh` enforces the 8-byte class and the 5-byte budget; `tests/run_tests.sh` runs it in an
  emulated 16-bit CPU; CI and tag-driven releases on GitHub Actions.
