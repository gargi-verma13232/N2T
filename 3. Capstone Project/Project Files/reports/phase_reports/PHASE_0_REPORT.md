# Phase 0 Report: Requirements Analysis, Environment Setup & Test Baseline

**Project Title:** Capstone Project: Make the Computer Draw a Box  
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Degree:** B.Tech Computer Science & Engineering (Semester 3)  
**Phase Status:** **COMPLETED**  
**Date:** 2026-11-15  

---

## 1. Phase Overview
Phase 0 establishes the engineering foundation for the entire Nand to Tetris Capstone Project. During this phase, the primary specification document (`Capstone_Project.pdf`) was comprehensively analyzed, extracting all architectural, computational, and grading criteria. The physical host environment was inspected, runtime dependencies were cataloged, and official test fixtures and simulation software from the Nand to Tetris toolchain were obtained and validated. A modular student personalization framework was constructed to decouple generic architecture work from roll-number-dependent parameters.

---

## 2. Objectives
1. Perform deep textual and architectural analysis of `Capstone_Project.pdf`.
2. Map out all three major technical parts (Part A: Hardware, Part B: Assembler, Part C: Box Program).
3. Audit local host system tools (Python, Java JDK, Git, Nand2Tetris simulation suite).
4. Establish a clean, professional directory hierarchy isolating official test fixtures from custom student code.
5. Verify execution of the official `HardwareSimulatorMain` and `HackAssemblerMain` engines.
6. Build a automated test runner (`tools/run_hdl_test.py`) capable of running `.tst` test scripts and verifying `.out` against `.cmp` files.
7. Implement a student configuration manager (`student_config.py` and `student_config.json`) with placeholders for roll number and personal number $K$.
8. Formulate a comprehensive implementation roadmap and initialize the central progress tracking system (`PROJECT_PROGRESS.md`).

---

## 3. Tasks Completed
- [x] Read and digested both pages of `Capstone_Project.pdf` (School of Engineering & Technology, K.R. Mangalam University).
- [x] Extracted grading distribution: Part A (2.5 marks), Part B (3.0 marks), Part C (2.5 marks), Viva Voce (2.0 marks) = 10 Marks total.
- [x] Verified local software toolchain:
  - Python: `3.14.0` (`python.exe` at `C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe`).
  - Java: `OpenJDK 21.0.10 LTS` (`java.exe` at `C:\Program Files\Java\jdk-21.0.10\bin\java.exe`).
  - Version Control: `git version 2.51.0.windows.2`.
- [x] Acquired official Nand to Tetris toolchain (`tools/` folder containing JARs and built-in chip implementations).
- [x] Isolated official project test fixtures:
  - Hardware: `CPU.tst`, `CPU.cmp`, `Memory.tst`, `Memory.cmp`, `ComputerAdd.tst`, `ComputerAdd.cmp`, `ComputerMax.tst`, `ComputerMax.cmp`, `ComputerRect.tst`, `ComputerRect.cmp`, `Add.hack`, `Max.hack`, `Rect.hack`.
  - Assembler: `Add.asm`, `Max.asm`, `Rect.asm`, `Pong.asm`, together with official precompiled reference binaries (`*_expected.hack`).
- [x] Engineered `tools/run_hdl_test.py` for automated headless HDL verification using Java JDK 21.
- [x] Created `student_config.py` and `student_config.json` with dynamic calculation of starting row, box height, pixel/word width, and assembler feature codes based on roll number digits.
- [x] Authored `documentation/PROJECT_OVERVIEW.md` detailing the architectural scope.
- [x] Initialized `PROJECT_PROGRESS.md` as the single source of progress tracking.

---

## 4. Files Created
1. `student_config.json` — Configuration store for roll number and student metadata with clean placeholders.
2. `student_config.py` — Python utility module implementing formulas for $K$, box dimensions, and extra assembler feature selection.
3. `tools/run_hdl_test.py` — Automated Python harness running `HardwareSimulatorMain` and parsing test outcomes.
4. `documentation/PROJECT_OVERVIEW.md` — Complete technical overview and architecture description.
5. `PROJECT_PROGRESS.md` — Central requirements checklist and milestone tracking log.
6. `reports/phase_reports/PHASE_0_REPORT.md` — This formal report.

---

## 5. Files Modified
- None (all initial structures created fresh from scratch).

---

## 6. Implementation Explanation

### 6.1 Understanding the Architectural Challenge
The Nand to Tetris Hack computer is a 16-bit Von Neumann architecture consisting of:
- **CPU**: 16-bit processing unit with an A-register (Address/Data), D-register (Data), Program Counter (PC), and an Arithmetic Logic Unit (ALU).
- **Instruction Formats**:
  - **A-instruction (`@value`)**: Formatted as `0vvv vvvv vvvv vvvv`, loads a 15-bit constant into the A-register.
  - **C-instruction (`dest=comp;jump`)**: Formatted as `111a cccc ccdd djjj`, instructs the ALU to perform a computation (`comp`), route results to destinations (`dest`), and conditionally branch (`jump`) based on ALU status flags ($zr$, $ng$).
- **Memory Map**:
  - $0\text{x}0000 - 0\text{x}3\text{FFF}$ ($0 - 16383$): Data RAM16K
  - $0\text{x}4000 - 0\text{x}5\text{FFF}$ ($16384 - 24575$): Screen memory map ($256$ rows $\times 32$ words/row)
  - $0\text{x}6000$ ($24576$): Keyboard memory-mapped register (`KBD`)

### 6.2 Formula Derivation & Personalization Logic
The student personalization logic in `student_config.py` implements:
1. $K = \text{Roll Number} \pmod{100}$ (last two digits).
2. Starting Row = $K$ (vertical screen coordinate).
3. Box Height = $20$ scanlines (rows $K$ through $K+19$).
4. Box Width = $16 \times ((K \bmod 4) + 1)$ pixels, equivalent to $(K \bmod 4) + 1$ full 16-bit words.
5. Extra Assembler Feature:
   - $K \bmod 3 = 0$: Dump symbols to `symbols.txt`.
   - $K \bmod 3 = 1$: Descriptive syntax errors with line numbers.
   - $K \bmod 3 = 2$: Duplicate label declaration warnings.

---

## 7. Technologies and Concepts Used
- **Hardware Architecture:** Von Neumann architecture, Harvard program bus split, memory-mapped I/O.
- **Languages:** Hack HDL, Hack Assembly, Python 3.14.
- **Runtimes & Tools:** OpenJDK 21 LTS, Git 2.51.
- **Automated Verification:** Subprocess execution, standard stream capturing, regression testing against official `.cmp` files.

---

## 8. Tests Performed
1. Verified Python environment execution and version string.
2. Verified Java 21 execution and JRE availability.
3. Tested `tools/run_hdl_test.py` against `part_a_hardware/tests/CPU.tst`.
4. Executed official `HackAssemblerMain` across `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` to establish golden reference `.hack` files (`*_expected.hack`).

---

## 9. Actual Test Results
- **Python check:** `Python 3.14.0` confirmed.
- **Java check:** `java version "21.0.10" 2026-01-20 LTS` confirmed.
- **Git check:** `git version 2.51.0.windows.2` confirmed.
- **Hardware test runner check:** Running `python tools/run_hdl_test.py part_a_hardware/tests/CPU.tst` properly detected missing `CPU.hdl` and exited with error code 1 as expected:
  ```
  Chip CPU is not found in the working and built in folders: load CPU.hdl
  ```
- **Official Assembler check:** Successfully assembled all four reference programs into `Add_expected.hack`, `Max_expected.hack`, `Rect_expected.hack`, and `Pong_expected.hack`.

---

## 10. Errors Encountered
1. **Broken Default Oracle Java Path:**
   - *Symptom:* Invoking `java` from PowerShell hung indefinitely without terminating.
   - *Investigation:* `C:\Program Files\Common Files\Oracle\Java\javapath\java.exe` was a stale symlink pointing to an unconfigured Oracle runtime.
   - *Solution:* Located valid OpenJDK 21 installation at `C:\Program Files\Java\jdk-21.0.10\bin\java.exe`. Configured all test scripts and runners to target this exact binary.
2. **Nand2Tetris Simulator Working Directory Sensitivity:**
   - *Symptom:* `HardwareSimulatorMain` reported missing `RAM16K` when run from root directory.
   - *Investigation:* Nand to Tetris simulator expects built-in Java classes (`builtInChips/`) to be resolvable relative to its classpath or tools directory.
   - *Solution:* Formatted `tools/run_hdl_test.py` to run with `cwd=tools` and include full classpath references.

---

## 11. Debugging and Solutions
- Identified and isolated the exact classpath required by Hack tools:
  `.;bin/classes;bin/lib/Hack.jar;bin/lib/HackGUI.jar;bin/lib/Simulators.jar;bin/lib/SimulatorsGUI.jar;bin/lib/Compilers.jar`
- Created automated python wrapper to prevent interactive GUI deadlocks in headless environments.

---

## 12. Screenshots and Evidence
- Verified directory listing:
  ```
  Directory: D:\KRMU 2025\SEMESTER-3\NAND\Nand2TetrisCapstone
  ├── capstone/
  ├── documentation/
  │   └── PROJECT_OVERVIEW.md
  ├── part_a_hardware/
  │   ├── screenshots/
  │   └── tests/
  ├── part_b_assembler/
  │   ├── generated/
  │   ├── screenshots/
  │   └── test_programs/
  ├── part_c_box_program/
  │   └── screenshots/
  ├── reports/
  │   ├── phase_reports/
  │   │   └── PHASE_0_REPORT.md
  │   └── test_reports/
  ├── tools/
  ├── PROJECT_PROGRESS.md
  ├── student_config.json
  └── student_config.py
  ```

---

## 13. Pending Tasks
- [ ] Receive student university roll number or its last two digits to resolve personal number $K$.
- [ ] Implement Part A HDL hardware files (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`).

---

## 14. Next Phase Overview (Phase 1)
In Phase 1, we will implement the complete hardware tier from absolute scratch:
1. `CPU.hdl` — Implementing instruction decoding, ALU multiplexing, A and D registers, PC control, and writeM/outM/addressM outputs.
2. `Memory.hdl` — Implementing address decoding for RAM16K, Screen buffer, and Keyboard register.
3. `Computer.hdl` — Integrating CPU, Memory, and ROM32K.
4. Testing each chip against official test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`) and logging all results.

