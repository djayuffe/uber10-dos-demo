; UBER8 - an 8-byte-class DOS demo, in 5 bytes: every CP437 glyph, scrolling, with sound.
; NASM: nasm -f bin src/uber8.asm -o UBER8.COM      Target: DOS/DOSBox, any CPU
;
; DOS starts a .COM with AX = 0 and the screen already in 80x25 text mode, so there is
; nothing to set up: INT 29h (DOS "fast console output") prints AL, and AX just counts.
; The 256 codes go by in order - smileys, card suits, punctuation, digits, letters, box
; drawing - with CR/LF, backspace and BEL (07h, which beeps) doing their usual things.
; It never ends and never reads the keyboard (no bytes to spare): close DOSBox, or
; press Ctrl+F9 in it, to stop it.
BITS 16
ORG 100h
.l: int 29h           ; CD 29     print AL
    inc ax            ; 40        next code
    jmp short .l      ; EB FB
