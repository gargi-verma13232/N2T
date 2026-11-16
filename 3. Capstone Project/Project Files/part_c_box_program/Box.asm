// Capstone Project: Make the Computer Draw a Box
// Course: Nand to Tetris - I (ETCCNT301) - School of Engineering & Technology, KRMU
// Student Personal Number K = 23
// Specifications:
// - Starting row: 23
// - Height: 20 rows (rows 23 to 42)
// - Width: 64 pixels (4 words per row)
// - Start memory address: SCREEN + 32 * 23 = 17120
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
    // start_addr = 16384 + (32 * 23) = 17120
    @17120
    D=A
    @row_ptr
    M=D

    // Initialize row loop counter: height = 20 rows
    @20
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

    // Number of 16-bit words per row: 4 (64 pixels)
    @4
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
