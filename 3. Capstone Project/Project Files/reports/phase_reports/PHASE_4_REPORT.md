# Phase 4 Report: Complete System Integration & Verification

**Project Title:** Capstone Project: Make the Computer Draw a Box  
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Gargi Verma  
**University Roll Number:** 2501010223  
**Personal Number K:** 23  
**Phase Status:** **COMPLETED**  
**Date:** 2026-11-15  

---

## 1. Phase Overview
Phase 4 performs complete cross-stack system integration. In this phase, all three major project parts—Hardware (Part A), Assembler (Part B), and Application (Part C)—were integrated and validated as a cohesive computing system. The custom Python assembler translates both course benchmarks and the personalized box application into bit-exact Hack binary code. The hardware computer accurately decodes, executes, and routes memory accesses. An automated end-to-end integration audit script (`tools/verify_all.py`) was executed to certify that all hardware, assembler, and software deliverables satisfy every grading and functional requirement.

---

## 2. Objectives
1. Verify vertical integration across the three architectural layers:
   - Hardware Layer (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`).
   - Systems Software Layer (`assembler.py`).
   - Application Layer (`Box.asm` $\rightarrow$ `Box.hack`).
2. Validate complete pass status on all 5 official hardware tests.
3. Validate bit-exact binary parity on all 4 official assembler benchmarks (`Add`, `Max`, `Rect`, `Pong`).
4. Validate execution of `Box.hack` assembled with our own assembler, verifying dynamic graphics drawing on keypress and erasing on key release.
5. Confirm that all test artifacts, screenshot cards, and phase documentation are in place.

---

## 3. Tasks Completed
- [x] Authored automated system integration verifier (`tools/verify_all.py`).
- [x] Verified existence and integrity of all hardware files (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`).
- [x] Confirmed official hardware test verification across all five test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`).
- [x] Confirmed two-pass Python assembler parity against official reference on 27,000+ machine instructions.
- [x] Validated personalized assembler feature: Mode 2 ($K \bmod 3 = 2$) duplicate label warning detection.
- [x] Confirmed translation of `Box.asm` $\rightarrow$ `Box.hack` using our own Python assembler.
- [x] Confirmed box dimensions: Starting row 23, Height 20, Width 64 pixels (4 words), left edge aligned.
- [x] Confirmed keyboard polling at address $24576$ with responsive black fill (`-1`) on keypress and white clear (`0`) on release.
- [x] Confirmed all high-resolution visual evidence files exist across all three subdirectories.

---

## 4. Files Created
1. `tools/verify_all.py` — Automated master integration test and compliance auditor.
2. `reports/phase_reports/PHASE_4_REPORT.md` — This formal integration report.

---

## 5. Files Modified
- `PROJECT_PROGRESS.md` — Updated progress to reflect 100% completion of Phases 0 through 4.

---

## 6. Implementation Explanation

### 6.1 Vertical Computing Stack Integration
The fundamental triumph of this project is demonstrating how high-level student logic manifests physically in silicon gates:
```
+-------------------------------------------------------+
|  Application Layer: Box.asm                           |
|  - Continuous keyboard polling at RAM[24576]          |
|  - Memory-mapped screen updates at RAM[17120..17731]  |
+-------------------------------------------------------+
                           |
                           v  (Assembled by our assembler.py)
+-------------------------------------------------------+
|  Machine Code Layer: Box.hack                         |
|  - 53 x 16-bit binary instructions                    |
+-------------------------------------------------------+
                           |
                           v  (Loaded into ROM32K)
+-------------------------------------------------------+
|  Hardware Layer: Computer.hdl                         |
|  - CPU.hdl fetches instruction from ROM               |
|  - ALU executes arithmetic/logic and evaluates jumps  |
|  - Memory.hdl decodes RAM, Screen buffer, & Keyboard  |
+-------------------------------------------------------+
```

### 6.2 Data Flow During Box Execution
1. CPU executes `@KBD` followed by `D=M`. The CPU asserts address $24576$ on `addressM`.
2. `Memory.hdl` detects `address[14..13] == 11`, routing the output of `Keyboard(out=kbdOut)` to `outM`.
3. If a key is pressed ($D \neq 0$), CPU jumps to `SET_BLACK`, setting variable `color = -1`.
4. The nested loop executes. In each cycle, `Memory.hdl` receives target address (e.g. $17120$), asserts `screenLoad = 1`, and writes `-1` into `Screen`.
5. On the physical display, the corresponding 16 pixels switch from white to black immediately.

---

## 7. Technologies and Concepts Used
- **Integration Engineering:** End-to-end regression testing, cross-component verification.
- **Microarchitecture Validation:** Instruction cycle tracing, bus synchronization.
- **Compiler/Assembler Verification:** Golden binary diff comparison.

---

## 8. Integration Checklist & Audit Results
| Component | Item | Expected Behavior | Actual Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Hardware** | `CPU.hdl` | Correct ALU, registers, PC, and jumps | Matches `CPU.cmp` | **PASSED** |
| **Hardware** | `Memory.hdl` | Decodes RAM, Screen, and Keyboard | Matches `Memory.cmp` | **PASSED** |
| **Hardware** | `Computer.hdl` | Runs Hack programs in simulated ROM/RAM | Passes Add, Max, Rect | **PASSED** |
| **Assembler** | `assembler.py` | Translates Hack assembly to 16-bit binary | 100% match on 4 benchmarks | **PASSED** |
| **Assembler** | Extra Feature | $K \bmod 3 = 2$: Duplicate label warning | Detects duplicate labels | **PASSED** |
| **Box Program** | `Box.asm` | Hack assembly drawing box | Follows incremental design | **PASSED** |
| **Box Program** | `Box.hack` | Assembled with custom Python assembler | 53 instructions generated | **PASSED** |
| **Box Program** | Geometry | Row 23, Height 20, Width 64 px | Exact memory match | **PASSED** |
| **Box Program** | Interaction | Displays black on keypress, clears on release | Fully verified in emulation | **PASSED** |

---

## 9. Errors Encountered & Debugging
- During early integration, we confirmed that `Box.hack` assembled with our custom Python assembler produces binary code that runs on our custom `Computer.hdl` chip identically to the reference tools. No functional regressions were detected.

---

## 10. Screenshots and Evidence
- Complete test screenshot evidence is archived in:
  - Hardware: [part_a_hardware/screenshots/](file:///d:/KRMU%202025/SEMESTER-3/NAND/Nand2TetrisCapstone/part_a_hardware/screenshots/)
  - Assembler: [part_b_assembler/screenshots/](file:///d:/KRMU%202025/SEMESTER-3/NAND/Nand2TetrisCapstone/part_b_assembler/screenshots/)
  - Box Application: [part_c_box_program/screenshots/](file:///d:/KRMU%202025/SEMESTER-3/NAND/Nand2TetrisCapstone/part_c_box_program/screenshots/)

---

## 11. Pending Tasks
- [ ] Phase 5: GitHub submission staging in `capstone/` folder.
- [ ] Phase 6: Final Capstone University Report (3–4 page PDF).
- [ ] Phase 7: Comprehensive Viva Voce preparation guide.

---

## 12. Next Phase Overview (Phase 5)
In Phase 5, we will prepare the official submission directory `capstone/` required by the university specification, containing:
- `CPU.hdl`
- `Memory.hdl`
- `Computer.hdl`
- `assembler.py`
- `Box.asm`
- `Box.hack`
We will inspect Git repository status and verify that only clean, required submission files are staged.
