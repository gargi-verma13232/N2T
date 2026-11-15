# Project Progress Tracker: Nand to Tetris Capstone
**Course:** ETCCNT301 — Nand to Tetris - I  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Gargi Verma  
**University Roll Number:** 2501010223  
**Personal Number (K):** 23  
**Project Title:** Make the Computer Draw a Box  
**Last Updated:** All Phases (0–7) Completed (100%)  

---

## Overall Status Summary
- **Overall Completion:** **100% COMPLETE**
- **Personalized Number K:** $23$ ($2501010223 \pmod{100}$)
- **Starting Row:** Row 23 (Row K)
- **Box Dimensions:** 64 pixels wide × 20 rows high (4 words per row)
- **Extra Assembler Feature:** Mode 2 ($K \bmod 3 = 2$: duplicate label declaration warning)
- **Deliverables Status:** Staged in `capstone/`, reports compiled in `reports/`, PDF ready.

---

## Master Requirements Checklist (From Capstone_Project.pdf)

### 1. General & Personalization Requirements — **[COMPLETED]**
- [x] Read and follow every instruction in `Capstone_Project.pdf` without skipping.
- [x] Set up development environment (Python 3.14, OpenJDK 21, Git, Nand2Tetris Toolchain).
- [x] Establish pristine project directory structure.
- [x] Roll number configured: `2501010223` $\rightarrow K = 23$.
- [x] Personalized box parameters calculated:
  - Starting row = $23$.
  - Height = $20$ rows (rows 23 to 42).
  - Width = $16 \times ((23 \bmod 4) + 1) = 64$ pixels ($4$ words).
- [x] Extra assembler feature configured: $23 \bmod 3 = 2$ (Duplicate label declaration warning).

---

### 2. Part A: Hardware Implementation (2.5 Marks) — **[COMPLETED]**
- [x] Implement `CPU.hdl` from scratch using standard Hack architecture.
  - [x] Instruction decoding logic (A-instruction vs C-instruction).
  - [x] A-register and D-register loading logic.
  - [x] ALU control inputs and data routing (`A` vs `M`).
  - [x] Memory write enable (`writeM`), output value (`outM`), memory address (`addressM`).
  - [x] Jump evaluation logic and Program Counter (`PC`) control (`load`, `inc`, `reset`).
- [x] Implement `Memory.hdl` from scratch using standard Hack memory map.
  - [x] RAM16K integration ($0 - 16383$).
  - [x] Screen integration ($16384 - 24575$).
  - [x] Keyboard integration ($24576$).
  - [x] Address decoding logic via `DMux` and `Mux16`.
- [x] Implement `Computer.hdl` from scratch.
  - [x] Integration of `ROM32K`, `CPU`, and `Memory`.
  - [x] Clock synchronization and reset wiring.
- [x] Execute official hardware tests and verify 100% pass:
  - [x] `CPU.tst` $\rightarrow$ `CPU.out` matches `CPU.cmp` (**PASSED**).
  - [x] `Memory.tst` $\rightarrow$ `Memory.out` matches `Memory.cmp` (**PASSED**).
  - [x] `ComputerAdd.tst` $\rightarrow$ `ComputerAdd.out` matches `ComputerAdd.cmp` (**PASSED**).
  - [x] `ComputerMax.tst` $\rightarrow$ `ComputerMax.out` matches `ComputerMax.cmp` (**PASSED**).
  - [x] `ComputerRect.tst` $\rightarrow$ `ComputerRect.out` matches `ComputerRect.cmp` (**PASSED**).
- [x] Capture test execution evidence and generate `PHASE_1_REPORT.md`.

---

### 3. Part B: Python Hack Assembler (3.0 Marks) — **[COMPLETED]**
- [x] Develop `assembler.py` from scratch (independent pure Python implementation).
- [x] First Pass implementation:
  - [x] Strip comments (`//...`) and trailing/leading whitespace.
  - [x] Discard blank lines.
  - [x] Maintain ROM address counter.
  - [x] Register label symbols `(LABEL)` in symbol table without advancing ROM address.
- [x] Second Pass implementation:
  - [x] Predefined Hack symbols (`SP`, `LCL`, `ARG`, `THIS`, `THAT`, `R0-R15`, `SCREEN`, `KBD`).
  - [x] Dynamic variable allocation starting at RAM address $16$.
  - [x] A-instruction binary translation (`0` + 15-bit address).
  - [x] C-instruction binary translation (`111` + comp bits + dest bits + jump bits).
- [x] Personalized Extra Feature ($K \bmod 3 = 2$):
  - [x] Mode 0 ($K \bmod 3 = 0$): Export symbols to `symbols.txt` (**PASSED**).
  - [x] Mode 1 ($K \bmod 3 = 1$): Line number syntax error reporting (**PASSED**).
  - [x] Mode 2 ($K \bmod 3 = 2$): Duplicate label declaration warning (**PASSED**).
- [x] Verification against official Hack test programs:
  - [x] `Add.asm` $\rightarrow$ bit-exact match with official reference (**PASSED**).
  - [x] `Max.asm` $\rightarrow$ bit-exact match with official reference (**PASSED**).
  - [x] `Rect.asm` $\rightarrow$ bit-exact match with official reference (**PASSED**).
  - [x] `Pong.asm` $\rightarrow$ bit-exact match with official reference (**PASSED**).
- [x] Capture visual evidence and generate `PHASE_2_REPORT.md`.

---

### 4. Part C: Box Hack Assembly Program (2.5 Marks) — **[COMPLETED]**
- [x] Implement `Box.asm` from scratch in Hack assembly:
  - [x] Starting row = $23$ ($K$).
  - [x] Box height = $20$ rows (rows 23 through 42).
  - [x] Box width = $64$ pixels ($4$ words per row).
  - [x] Continuous keyboard polling at memory address $24576$ (`KBD`).
  - [x] When key is pressed (`KBD != 0`), fill box pixels with black (`-1`).
  - [x] When key is released (`KBD == 0`), clear box pixels to white (`0`).
- [x] Assemble `Box.asm` into `Box.hack` strictly using our own Python assembler (`assembler.py`).
- [x] Verify execution in Nand to Tetris CPU Emulator.
- [x] Capture visual evidence and screenshots.
- [x] Generate `PHASE_3_REPORT.md`.

---

### 5. Integration, Packaging & Final Reports (2.0 Marks + Submission) — **[COMPLETED]**
- [x] Complete Phase 4 end-to-end integration checklist and report (`PHASE_4_REPORT.md`).
- [x] Populate clean submission staging folder `capstone/` with:
  - `CPU.hdl`
  - `Memory.hdl`
  - `Computer.hdl`
  - `assembler.py`
  - `Box.asm`
  - `Box.hack`
  - `Final_Capstone_Report.pdf`
- [x] Generate `PHASE_5_REPORT.md` (Submission Readiness).
- [x] Generate Final Capstone University Report (`Final_Capstone_Report.pdf`, exactly 4 pages).
- [x] Prepare comprehensive Viva Voce Guide (`VIVA_PREPARATION.md`) with 25+ Q&A and 5 live-code modification scenarios.

---

## Phase Execution History
| Phase | Title | Status | Date Completed | Key Deliverables |
| :---: | :--- | :---: | :---: | :--- |
| **0** | Requirements Analysis & Environment Setup | **COMPLETED** | 2026-11-15 | `PROJECT_OVERVIEW.md`, `student_config.py`, `student_config.json`, `tools/run_hdl_test.py`, `PHASE_0_REPORT.md` |
| **1** | Hardware Construction (HDL) | **COMPLETED** | 2026-11-15 | `CPU.hdl`, `Memory.hdl`, `Computer.hdl`, 5 official tests passed, 5 screenshot cards, `PHASE_1_REPORT.md` |
| **2** | Python Hack Assembler | **COMPLETED** | 2026-11-15 | `assembler.py`, 4 benchmark programs bit-exact, extra features verified, 2 screenshot cards, `PHASE_2_REPORT.md` |
| **3** | Box Drawing Assembly Program | **COMPLETED** | 2026-11-15 | `Box.asm`, `Box.hack` (own assembler), 4 screenshot cards, `PHASE_3_REPORT.md` |
| **4** | System Integration & End-to-End Testing | **COMPLETED** | 2026-11-15 | Automated audit tool `verify_all.py` (100% pass), `PHASE_4_REPORT.md` |
| **5** | GitHub Submission Staging | **COMPLETED** | 2026-11-15 | Clean `capstone/` folder, local Git repo initialized & committed, `PHASE_5_REPORT.md` |
| **6** | Final University Report (PDF) | **COMPLETED** | 2026-11-15 | `Final_Capstone_Report.pdf` (exactly 4 pages, professional layout) |
| **7** | Viva Voce Preparation Guide | **COMPLETED** | 2026-11-15 | `VIVA_PREPARATION.md` (25 Q&A, 5 on-the-spot live modifications) |
