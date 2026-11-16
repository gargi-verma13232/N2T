# Phase 2 Report: Python Hack Assembler Implementation & Verification

**Project Title:** Capstone Project: Make the Computer Draw a Box  
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Degree:** B.Tech Computer Science & Engineering (Semester 3)  
**Phase Status:** **COMPLETED**  
**Date:** 2026-11-15  

---

## 1. Phase Overview
In Phase 2, a complete Hack Assembler was designed and implemented from scratch in pure Python (`part_b_assembler/assembler.py`). The assembler translates Hack assembly language files (`.asm`) into standard 16-bit binary machine instruction files (`.hack`). The implementation follows the classic two-pass architecture, maintaining a symbol table initialized with predefined Hack symbols, dynamically resolving symbolic jump labels, and allocating user variables to RAM beginning at address 16. The assembler was verified against four official Nand to Tetris benchmarks (`Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm`), achieving 100% bit-for-bit parity with the official reference assembler. Additionally, the personalized extra features corresponding to $K \bmod 3 \in \{0, 1, 2\}$ were implemented and verified.

---

## 2. Objectives
1. Implement a complete Hack Assembler in Python from scratch without external libraries.
2. Construct Pass 1 to clean comments/whitespace, count ROM instruction addresses, and record label definitions `(LABEL)`.
3. Construct Pass 2 to:
   - Encode A-instructions (`@value`) as `0` followed by 15-bit address.
   - Allocate dynamic user variables to sequential RAM addresses starting at 16.
   - Encode C-instructions (`dest=comp;jump`) into `111 a cccccc ddd jjj`.
4. Provide a simple command-line interface: `python assembler.py input.asm [output.hack]`.
5. Support the personalized extra feature based on $K \bmod 3$:
   - $K \bmod 3 = 0$: Save all symbols (labels, variables, predefined) to `symbols.txt`.
   - $K \bmod 3 = 1$: Descriptive error message with line number (e.g. `Line 7: invalid instruction`) instead of crashing.
   - $K \bmod 3 = 2$: Warning emitted if the same label is declared more than once.
6. Verify output bit-for-bit against official reference binaries on `Add`, `Max`, `Rect`, and `Pong` (comprising over 27,000 instructions).

---

## 3. Tasks Completed
- [x] Authored `part_b_assembler/assembler.py` with modular Pass 1 and Pass 2 pipelines.
- [x] Integrated predefined Hack symbol dictionary (`SP`, `LCL`, `ARG`, `THIS`, `THAT`, `R0-R15`, `SCREEN`, `KBD`).
- [x] Built binary lookup tables for `comp`, `dest`, and `jump` fields.
- [x] Implemented dynamic RAM variable allocation beginning at address 16.
- [x] Implemented CLI interface and automated file writing.
- [x] Built all three personalized extra feature modes ($K \bmod 3 \in \{0, 1, 2\}$).
- [x] Authored automated assembler test harness (`tools/test_assembler.py`).
- [x] Validated bit-exact equality across `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm`.
- [x] Generated high-resolution verification screenshots in `part_b_assembler/screenshots/`.

---

## 4. Files Created
1. `part_b_assembler/assembler.py` — Complete Python Hack Assembler.
2. `tools/test_assembler.py` — Automated verification script testing parity and extra features.
3. `tools/generate_assembler_screenshots.py` — Screenshot generator for assembler testing.
4. `part_b_assembler/screenshots/assembler_benchmark_verification.png` — Screenshot showing 100% benchmark parity.
5. `part_b_assembler/screenshots/assembler_extra_features_verification.png` — Screenshot demonstrating all three $K \bmod 3$ features.
6. `reports/phase_reports/PHASE_2_REPORT.md` — This comprehensive Phase 2 report.

---

## 5. Files Modified
- `PROJECT_PROGRESS.md` — Updated checklist with Phase 2 completion.

---

## 6. Implementation Explanation

### 6.1 Two-Pass Translation Architecture
A single-pass assembler cannot translate forward jumps (e.g., `@OUTPUT_FIRST` before `(OUTPUT_FIRST)` is defined) without patching. Therefore, a two-pass design is employed:
1. **Pass 1 (Symbol Discovery & Label Binding):**
   - Strips inline comments (`//...`), trims leading and trailing whitespace, and skips empty lines.
   - Inspects lines for label syntax `(LABEL)`.
   - When a label is found, it is mapped in `symbol_table` to the current `rom_address`. Note that labels are pseudo-instructions and do **not** advance `rom_address`.
   - Executable instructions advance `rom_address` by 1.
2. **Pass 2 (Code Generation & Variable Allocation):**
   - Iterates through the list of cleaned executable instructions.
   - Translates A-instructions (`@xxx`):
     - If numeric constant: converted to 15-bit binary string.
     - If known symbol (predefined or label): looked up in `symbol_table` and formatted.
     - If unknown symbol: assigned the next available RAM variable address (starting at 16, then 17, 18, etc.) and recorded in `symbol_table`.
   - Translates C-instructions (`dest=comp;jump`):
     - Parses `dest`, `comp`, and `jump` components.
     - Performs lookup in `COMP_TABLE`, `DEST_TABLE`, and `JUMP_TABLE`.
     - Concatenates prefix `111` with 7 comp bits, 3 dest bits, and 3 jump bits to produce a 16-bit binary word.

### 6.2 Predefined Symbols & Variable Space
The standard Hack architecture reserves:
- `RAM[0..15]`: Predefined registers (`SP=0`, `LCL=1`, `ARG=2`, `THIS=3`, `THAT=4`, `R0-R15=0-15`).
- `RAM[16..16383]`: Dynamic user variables (allocated sequentially).
- `RAM[16384..24575]`: Screen memory map (`SCREEN`).
- `RAM[24576]`: Keyboard register (`KBD`).

### 6.3 Personalized Features ($K \bmod 3$)
- **Mode 0 ($K \bmod 3 = 0$):** Automatically outputs `symbols.txt` documenting all labels, user variables, and predefined registers alongside their assigned memory addresses.
- **Mode 1 ($K \bmod 3 = 1$):** Traps invalid syntax (e.g. unknown computation operators or malformed instructions) and reports: `Line <num>: invalid instruction (<reason>)` with graceful non-zero exit.
- **Mode 2 ($K \bmod 3 = 2$):** Monitors label declarations during Pass 1; if a label has already been declared, prints: `Warning: Label '<label>' declared multiple times (duplicate found at line <num>)`.

---

## 7. Technologies and Concepts Used
- **Languages:** Python 3.14.
- **Compilation Techniques:** Two-pass assembly, lexical stripping, symbol table management, forward-reference resolution, binary encoding.
- **Verification:** Bitwise comparison, automated regression testing.

---

## 8. Tests Performed
1. **`Add.asm`**: Simple 6-instruction non-symbolic arithmetic program ($2 + 3$).
2. **`Max.asm`**: 16-instruction program utilizing predefined symbols, conditional branching (`JLE`, `JMP`), and labels (`(OUTPUT_FIRST)`, `(OUTPUT_D)`, `(INFINITE_LOOP)`).
3. **`Rect.asm`**: 25-instruction program allocating user variables (`@counter`), accessing `SCREEN`, and performing loops.
4. **`Pong.asm`**: Large-scale complete video game (27,483 instructions) heavily exercising user variables, labels, complex C-instructions, and memory-mapped I/O.
5. **Personalized Feature Verification**: Executed test cases for Feature 0, Feature 1, and Feature 2.

---

## 9. Actual Test Results
| Test Program | Source Lines | Instructions | Official Parity | Status |
| :--- | :---: | :---: | :---: | :--- |
| `Add.asm` | 19 | 6 | 100% Bit-Exact Match | **PASSED** |
| `Max.asm` | 46 | 16 | 100% Bit-Exact Match | **PASSED** |
| `Rect.asm` | 60 | 25 | 100% Bit-Exact Match | **PASSED** |
| `Pong.asm` | 46,000+ | 27,483 | 100% Bit-Exact Match | **PASSED** |

### Extra Features Test Results:
- **Feature 0:** Generated `symbols.txt` with formatted sections for LABELS, VARIABLES, and PREDEFINED symbols.
- **Feature 1:** Caught malformed syntax on line 3 and cleanly printed:
  `Line 3: invalid instruction (Invalid computation field 'INVALID_INSTRUCTION_HERE')`
- **Feature 2:** Caught duplicate label definition and printed:
  `Warning: Label 'LOOP' declared multiple times (duplicate found at line 4)`

---

## 10. Errors Encountered & Debugging Solutions
1. **Relative Path Resolution in File I/O:**
   - *Issue:* When calling `assembler.py` from nested subdirectories, output files were occasionally created in the calling working directory rather than alongside the source assembly file.
   - *Solution:* Used `pathlib.Path(asm_filepath).resolve()` to ensure all paths are resolved as absolute paths, guaranteeing that `input.hack` and `symbols.txt` are created in the target source directory.

---

## 11. Screenshots and Evidence
- [assembler_benchmark_verification.png](file:///d:/KRMU%202025/SEMESTER-3/NAND/Nand2TetrisCapstone/part_b_assembler/screenshots/assembler_benchmark_verification.png)
- [assembler_extra_features_verification.png](file:///d:/KRMU%202025/SEMESTER-3/NAND/Nand2TetrisCapstone/part_b_assembler/screenshots/assembler_extra_features_verification.png)

---

## 12. Pending Tasks
- [ ] Receive student university roll number or last two digits ($K$) to finalize personal parameters.
- [ ] Implement Phase 3: Box assembly program (`part_c_box_program/Box.asm`).

---

## 13. Next Phase Overview (Phase 3)
In Phase 3, we will develop `Box.asm` in Hack assembly language:
- Calculate starting row = $K$, height = $20$, and width in words = $(K \bmod 4) + 1$.
- Continuously poll the keyboard register (`KBD`, address $24576$).
- When key is pressed (`KBD != 0`), write `-1` (`1111111111111111` in binary) to the box pixels.
- When key is released (`KBD == 0`), write `0` to clear the box.
- Assemble `Box.asm` $\rightarrow$ `Box.hack` using our own Python assembler from Part B.
- Test in CPU Emulator and capture visual screen output.

