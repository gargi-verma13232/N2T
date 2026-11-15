# Nand to Tetris Capstone Project: Make the Computer Draw a Box
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Level:** B.Tech CSE (Semester 3)  
**Weightage:** 10 Marks (Individual Work)  
**Course Outcomes Addressed:** CO1–CO4  

---

## 1. Project Objective & Vision
The fundamental objective of this Capstone Project is to demonstrate complete, vertical integration across the computing hierarchy by constructing a general-purpose Hack computer from elementary logic gates, building a full two-pass machine language assembler in Python from scratch, and developing an interactive Hack assembly application that dynamically renders a graphic box on the screen driven by keyboard events.

The user experience goal is concise and visual:
> **When any keyboard key is pressed, a black rectangular box appears at a personalized screen position. When the key is released, the box immediately disappears.**

---

## 2. Problem Statement
Modern computer science education frequently abstracts away the physical and architectural foundations of computing. This project bridges the entire hardware-software chasm across three distinct layers:
1. **Hardware Level:** Realizing the digital logic, address decoding, arithmetic-logic unit (ALU), program counter, CPU control matrix, and memory-mapped input/output architecture in Hardware Description Language (HDL).
2. **System Software Level:** Translating human-readable Hack symbolic assembly code into binary machine instructions (`.asm` $\rightarrow$ `.hack`) using a custom-built two-pass assembler written in Python.
3. **Application Level:** Writing an optimized, low-level assembly program that directly reads physical memory addresses corresponding to the Hack keyboard (`RAM[24576]`) and manipulates the memory-mapped screen buffer (`RAM[16384..24575]`) in real-time.

---

## 3. Core Requirements & Personalized Specifications

### 3.1 Personal Number ($K$)
The project is personalized for each student using their university roll number:
$$\mathbf{K = \text{Last two digits of University Roll Number}}$$

### 3.2 Personalized Box Dimensions (Part C)
- **Starting Screen Row ($r$):** Row $K$
- **Box Height:** Exactly $20\text{ rows}$ (spanning rows $K$ to $K+19$)
- **Box Width (in pixels):** $16 \times ((K \bmod 4) + 1)\text{ pixels}$
- **Box Width (in Hack 16-bit words):** $(K \bmod 4) + 1\text{ words}$
- **Horizontal Alignment:** Flushed to the **left edge** of the display (starting at the first word of each row, offset 0).

### 3.3 Screen Memory Architecture
- Total Screen Resolution: $512\text{ pixels wide} \times 256\text{ pixels high}$.
- Screen Memory Map: Addresses $16384$ (`0x4000`) through $24575$ (`0x5FFF`), totaling $8192$ words.
- Each row of the screen consists of 32 consecutive 16-bit words ($32 \times 16 = 512$ pixels).
- The memory base address for screen row $r$ is:
$$\text{Row Address}(r) = \text{SCREEN} + 32 \times r = 16384 + 32 \times r$$
- To draw a continuous horizontal block of 16 black pixels, the corresponding 16-bit memory word is set to `-1` (in 16-bit two's complement binary: `1111111111111111`).
- To clear 16 pixels to white, the memory word is set to `0` (`0000000000000000`).

### 3.4 Personalized Assembler Feature (Part B)
Based on $K \bmod 3$, the custom Python assembler incorporates one specific feature:
| $K \bmod 3$ | Extra Assembler Feature |
| :---: | :---|
| **0** | Save all symbol table entries (labels and allocated variables) with their resolved addresses into `symbols.txt`. |
| **1** | Provide syntax error handling: For any malformed instruction, output an informative error message indicating the exact line number (e.g., `Line 7: invalid instruction`) instead of crashing. |
| **2** | Symbol collision detection: Emit a descriptive warning if the same label (e.g., `(LOOP)`) is declared more than once in the source code. |

---

## 4. Architectural Components

### Part A: Hardware Construction (`part_a_hardware/`)
- **`CPU.hdl`**: The central processing unit of the Hack computer. Integrates the Hack ALU, A-register, D-register, Program Counter (PC), instruction decoder, and jump/control branching logic. Handles both A-instructions (`@value`) and C-instructions (`dest=comp;jump`).
- **`Memory.hdl`**: The complete Hack address space ($32\text{K}$ addressable words):
  - $0\text{x}0000 - 0\text{x}3\text{FFF}$ ($0 - 16383$): Standard Data RAM ($16\text{K}$).
  - $0\text{x}4000 - 0\text{x}5\text{FFF}$ ($16384 - 24575$): Screen memory map ($8\text{K}$).
  - $0\text{x}6000$ ($24576$): Keyboard memory-mapped register ($1\text{ word}$).
- **`Computer.hdl`**: Top-level chip integrating `ROM32K` (program memory), `CPU`, and `Memory` with clock synchronization and reset control.

### Part B: Hack Assembler (`part_b_assembler/assembler.py`)
- Independent Python application developed strictly from scratch (no reliance on external assembler binaries).
- **First Pass:** Strips comments (`//...`), trims leading/trailing whitespace, discards empty lines, tracks ROM program counter address increments, and records label declarations `(LABEL)` in a symbol table.
- **Second Pass:** Translates A-instructions (`@xxx` with immediate numbers, predefined symbols, labels, or auto-allocated RAM variables starting at RAM address 16) and C-instructions (`dest=comp;jump`) into 16-bit binary strings.
- Enforces the student's personalized $K \bmod 3$ feature.
- Validates bit-exact parity against official reference outputs on `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm`.

### Part C: Interactive Box Application (`part_c_box_program/Box.asm`)
- Written in pure Hack assembly language.
- Continuously polls keyboard register `KBD` (`24576`).
- If `KBD != 0` (key pressed): Paints pixels black (`-1`) across $20$ rows starting at row $K$, spanning $(K \bmod 4) + 1$ words per row.
- If `KBD == 0` (no key pressed): Paints pixels white (`0`) across the exact same region to erase the box.
- Assembled into `Box.hack` using our own Python assembler from Part B.
- Tested and verified in the official CPU Emulator.

---

## 5. Development Roadmap & Milestones

```
+-------------------------------------------------------------+
| Phase 0: Requirements Analysis, Setup & Baseline Validation | <--- (COMPLETED)
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 1: Hardware Implementation (CPU, Memory, Computer)    |
| - Implement HDL files from scratch                          |
| - Verify against 5 official .tst scripts in HardwareSim     |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 2: Python Hack Assembler Implementation               |
| - Develop two-pass assembler from scratch                   |
| - Incorporate K mod 3 extra feature                         |
| - Validate against Add, Max, Rect, Pong official .hack      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 3: Box Assembly Program (Part C)                      |
| - Implement incremental drawing logic in Hack assembly      |
| - Integrate keyboard polling & clearing                     |
| - Assemble with our own assembler.py -> Box.hack            |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 4: Full System Integration & Verification             |
| - End-to-end execution on simulated hardware                |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 5: Submission Staging (`capstone/` folder & Git)      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 6: Final Capstone University Report (3-4 pages PDF)   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 7: Viva Voce Comprehensive Preparation Guide          |
+-------------------------------------------------------------+
```

---

## 6. Deliverables Checklist
- [x] Complete directory hierarchy established.
- [x] Official Nand to Tetris Java toolchain and test suites verified in environment.
- [x] Student configuration manager (`student_config.py`, `student_config.json`) initialized with clear placeholders for roll number / $K$.
- [ ] Part A: `CPU.hdl`, `Memory.hdl`, `Computer.hdl` passing official tests.
- [ ] Part B: `assembler.py` passing official test programs and supporting personalized feature.
- [ ] Part C: `Box.asm` and `Box.hack` rendering personalized box on keypress.
- [ ] Central `PROJECT_PROGRESS.md` maintained after every phase.
- [ ] Detailed Phase Reports in `reports/phase_reports/`.
- [ ] Clean submission bundle in `capstone/`.
- [ ] Final 3–4 page university PDF report.
- [ ] 5-minute Viva guide with 20+ questions and live-code modifications.

