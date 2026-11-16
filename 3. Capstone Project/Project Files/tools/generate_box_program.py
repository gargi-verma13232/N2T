#!/usr/bin/env python3
"""
Box Program Generator and Validator for Nand to Tetris Capstone.
Generates Box.asm based on the student's personal number K.

Formulas:
- Starting row = K
- Height = 20 rows
- Width = 16 * ((K mod 4) + 1) pixels = (K mod 4 + 1) words
- Row r base address = SCREEN + 32 * r = 16384 + 32 * r
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from student_config import get_parameters, load_config

def generate_box_asm(k: int) -> str:
    k_mod_4 = k % 4
    width_words = k_mod_4 + 1
    width_pixels = 16 * width_words
    starting_row = k
    height = 20
    start_addr = 16384 + 32 * starting_row

    asm_code = f"""// Capstone Project: Make the Computer Draw a Box
// Course: Nand to Tetris - I (ETCCNT301) - School of Engineering & Technology, KRMU
// Student Personal Number K = {k}
// Specifications:
// - Starting row: {starting_row}
// - Height: {height} rows (rows {starting_row} to {starting_row + height - 1})
// - Width: {width_pixels} pixels ({width_words} words per row)
// - Start memory address: SCREEN + 32 * {starting_row} = {start_addr}
// Behavior:
// - While any keyboard key is pressed (KBD != 0), draws black box (color = -1).
// - When key is released (KBD == 0), erases box (color = 0).

(POLL_KEYBOARD)
    // Read keyboard memory-mapped register KBD (RAM[24576])
    @KBD
    D=M

    // If D != 0 (key is pressed), set color to -1 (black pixels)
    @SET_BLACK
    D;JNE

(SET_WHITE)
    // Key released: color = 0 (white / erase)
    @color
    M=0
    @RENDER
    0;JMP

(SET_BLACK)
    // Key pressed: color = -1 (black / fill)
    @color
    M=-1

(RENDER)
    // Initialize row address pointer to the starting row of the box:
    // start_addr = 16384 + (32 * {starting_row}) = {start_addr}
    @{start_addr}
    D=A
    @row_ptr
    M=D

    // Initialize row loop counter: height = {height} rows
    @{height}
    D=A
    @rows_left
    M=D

(ROW_LOOP)
    // Check if all rows have been rendered
    @rows_left
    D=M
    @POLL_KEYBOARD
    D;JLE

    // Render columns in the current row
    // Base address of current row is stored in row_ptr
    @row_ptr
    D=M
    @col_ptr
    M=D

    // Number of 16-bit words per row: {width_words} ({width_pixels} pixels)
    @{width_words}
    D=A
    @cols_left
    M=D

(COL_LOOP)
    // Check if row words are complete
    @cols_left
    D=M
    @NEXT_ROW
    D;JLE

    // Write color (-1 or 0) into RAM[col_ptr]
    @color
    D=M
    @col_ptr
    A=M
    M=D

    // Advance to next word in this row: col_ptr = col_ptr + 1
    @col_ptr
    M=M+1

    // Decrement columns remaining: cols_left = cols_left - 1
    @cols_left
    M=M-1

    @COL_LOOP
    0;JMP

(NEXT_ROW)
    // Advance row pointer by 32 words (one full scanline on 512-pixel display):
    // row_ptr = row_ptr + 32
    @32
    D=A
    @row_ptr
    M=D+M

    // Decrement rows remaining: rows_left = rows_left - 1
    @rows_left
    M=M-1

    @ROW_LOOP
    0;JMP
"""
    return asm_code

def main():
    if len(sys.argv) > 1:
        k = int(sys.argv[1])
    else:
        cfg = load_config()
        k = cfg.get("k_value")
        if k is None:
            print("Personal number K is not configured in student_config.json.")
            print("Usage: python generate_box_program.py <K>")
            sys.exit(1)

    asm_content = generate_box_asm(k)
    out_file = PROJECT_ROOT / "part_c_box_program" / "Box.asm"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(asm_content)
    print(f"Generated Box.asm for K = {k} at: {out_file}")

if __name__ == "__main__":
    main()

