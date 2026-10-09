#!/bin/sh
# Assemble UBER10.COM with NASM and enforce two size gates:
#   class  = the size class (16 bytes) - a hard ceiling;
#   budget = the size it has been shrunk to (10 bytes) - it may not grow back.
set -eu
cd "$(dirname "$0")"
command -v nasm >/dev/null 2>&1 || { echo 'ERROR: NASM is required.' >&2; exit 1; }
nasm -f bin -Wall -Werror uber10.asm -o UBER10.COM
size=$(wc -c < UBER10.COM | tr -d ' ')
printf '%s: %s bytes (class 16, budget 10)\n' UBER10.COM "$size"
[ "$size" -le 16 ] || { echo 'ERROR: UBER10.COM exceeds its 16-byte class' >&2; exit 2; }
[ "$size" -le 10 ] || { echo 'ERROR: UBER10.COM grew past its 10-byte budget' >&2; exit 2; }
if command -v sha256sum >/dev/null 2>&1; then sha256sum UBER10.COM > SHA256SUMS; else shasum -a 256 UBER10.COM > SHA256SUMS; fi
cat SHA256SUMS
