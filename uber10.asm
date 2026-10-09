; UBER10 - a 10-byte DOS demo: the 256 CP437 glyphs, scrolling at a readable pace, with sound.
; NASM: nasm -f bin uber10.asm -o UBER10.COM      Target: DOS/DOSBox, any CPU
;
; DOS starts a .COM with AX = 0 in 80x25 text mode, so there is nothing to set up. INT 29h
; (DOS "fast console output") prints AL and AX just counts: smileys, card suits, punctuation,
; digits, letters, box drawing, with CR/LF, backspace and BEL (07h, which beeps) doing their
; usual things.
;
; A bare print loop (the 5-byte version) runs at emulator speed and is an unreadable blur.
; HLT sleeps until the next timer tick (18.2 Hz), so printing 8 codes per tick gives
; ~145 characters a second: about two lines a second, which scrolls but can be read.
; It never ends and never reads the keyboard: close DOSBox, or press Ctrl+F9 in it.
BITS 16
ORG 100h
.m: hlt               ; F4        sleep until the next timer tick
.l: int 29h           ; CD 29     print AL
    inc ax            ; 40        next code
    test al,7         ; A8 07     8 codes per tick
    jnz .l            ; 75 F9
    jmp short .m      ; EB F4
