# Nand to Tetris Capstone Project: Make the Computer Draw a Box
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Gargi Verma  
**University Roll Number:** 2501010223  
**Personal Number (K):** 23  

---

## 1. Project Specifications
- **Hardware (Part A):** Full Hack computer architecture implemented in HDL (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`).
- **Assembler (Part B):** Custom two-pass Hack Assembler built from scratch in Python (`assembler.py`) with support for personalized Feature 2 ($K \bmod 3 = 2$: duplicate label declaration warning).
- **Box Program (Part C):** Interactive graphics program in Hack assembly (`Box.asm` $\rightarrow$ `Box.hack`):
  - Starting Row: $K = 23$
  - Height: $20$ scanlines (rows 23 to 42)
  - Width: $16 \times ((23 \bmod 4) + 1) = 64$ pixels ($4$ words per row)
  - Horizontal Position: Left edge of screen
  - Behavior: Displays black box while any keyboard key is pressed; erases back to pure white when released.

---

## 2. Submission Directory (`capstone/`)
According to the assignment specification, the required deliverables are staged in `capstone/`:
- `CPU.hdl`
- `Memory.hdl`
- `Computer.hdl`
- `assembler.py`
- `Box.asm`
- `Box.hack`

---

## 3. How to Run & Verify

### Running the Python Hack Assembler
```bash
python assembler.py Box.asm Box.hack
```

### Running Hardware Tests in Hardware Simulator
```bash
# In Nand to Tetris Hardware Simulator:
# Load CPU.tst, Memory.tst, ComputerAdd.tst, ComputerMax.tst, or ComputerRect.tst
# Or via automated test runner:
python tools/run_hdl_test.py part_a_hardware/tests/CPU.tst
```

### Running the Box Program in CPU Emulator
1. Open the Nand to Tetris **CPU Emulator**.
2. Load `capstone/Box.hack` (or `part_c_box_program/Box.hack`).
3. Set Animation speed to "No animation" (Fast forward).
4. Run the program.
5. Focus the emulator window and press any keyboard key: the black box appears at row 23 (height 20, width 64px).
6. Release the key: the box disappears immediately.

---

## 4. Verification & Testing Summary
- **CPU.tst:** PASSED (`End of script - Comparison ended successfully`)
- **Memory.tst:** PASSED (RAM and Screen addresses match `Memory.cmp` line-for-line)
- **ComputerAdd.tst:** PASSED (`End of script - Comparison ended successfully`)
- **ComputerMax.tst:** PASSED (`End of script - Comparison ended successfully`)
- **ComputerRect.tst:** PASSED (`End of script - Comparison ended successfully`)
- **Assembler Benchmarks:** `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` verified bit-for-bit identical with official Hack reference outputs.
- **Box Interaction:** Verified in emulation and simulation with complete screenshot evidence in `part_c_box_program/screenshots/`.
