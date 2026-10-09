#!/bin/sh
# Assemble UBER8.COM with NASM and enforce two size gates:
#   class  = the size class (8 bytes) - a hard ceiling;
#   budget = the size it has been shrunk to (5 bytes) - it may not grow back.
set -eu
cd "$(dirname "$0")"
command -v nasm >/dev/null 2>&1 || { echo 'ERROR: NASM is required.' >&2; exit 1; }
nasm -f bin -Wall -Werror uber8.asm -o UBER8.COM
size=$(wc -c < UBER8.COM | tr -d ' ')
printf '%s: %s bytes (class 8, budget 5)\n' UBER8.COM "$size"
[ "$size" -le 8 ] || { echo 'ERROR: UBER8.COM exceeds its 8-byte class' >&2; exit 2; }
[ "$size" -le 5 ] || { echo 'ERROR: UBER8.COM grew past its 5-byte budget' >&2; exit 2; }
if command -v sha256sum >/dev/null 2>&1; then sha256sum UBER8.COM > SHA256SUMS; else shasum -a 256 UBER8.COM > SHA256SUMS; fi
cat SHA256SUMS
