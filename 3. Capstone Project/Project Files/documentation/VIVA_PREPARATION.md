# Comprehensive Viva Voce Preparation Guide (5-Minute Defense)
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Gargi Verma  
**University Roll Number:** 2501010223  
**Personal Number (K):** 23  
**Project Title:** Make the Computer Draw a Box  

---

## 1. 60-Second Opening Pitch for the Viva
> *"Good morning, Sir/Ma'am. My name is Gargi Verma, Roll Number 2501010223. My personal number K is 23.*  
> *For my capstone project, I built a working Hack computer from scratch across three integrated layers:*  
> *First, in **Part A**, I implemented the complete hardware platform using HDL—`CPU.hdl`, `Memory.hdl`, and `Computer.hdl`—which passes all five official test suites including CPU, Memory, and Computer graphics tests.*  
> *Second, in **Part B**, I developed a full two-pass Hack Assembler in Python from scratch. It handles label resolution, dynamic variable allocation starting at RAM address 16, and has bit-for-bit parity across official benchmarks like Add, Max, Rect, and Pong. It also includes my personalized feature for K mod 3 = 2, which detects and warns against duplicate label declarations.*  
> *Third, in **Part C**, I authored `Box.asm` in Hack assembly, which continuously polls the keyboard. When any key is pressed, it draws a 64-pixel wide by 20-row tall solid black box starting at Row 23 on the left margin. When the key is released, it clears the box immediately.*  
> *I compiled `Box.asm` into `Box.hack` using my own Python assembler and verified it in the CPU Emulator with zero flicker."*

---

## 2. Deep-Dive Component Explanations

### 2.1 Hardware Architecture (`part_a_hardware/`)
- **`CPU.hdl` (Central Processing Unit):**
  - **Instruction Decoding:** Bit 15 determines the instruction type. If `instruction[15] == 0`, it is an **A-instruction** (`@value`), loading a 15-bit constant into the A-register. If `instruction[15] == 1`, it is a **C-instruction** formatted as `111 a cccccc ddd jjj`.
  - **A-Register Multiplexing:** `Mux16` selects `instruction` if A-instruction, or `aluOut` if C-instruction. The A-register loads if it's an A-instruction OR if destination bit $d_1$ (`instruction[5]`) is asserted.
  - **ALU Operand Routing:** The `a`-bit (`instruction[12]`) controls `Mux16(a=aOut, b=inM, sel=instruction[12], out=aluYInput)`. If $a=0$, the ALU computes with register A; if $a=1$, it computes with memory operand M (`inM`).
  - **D-Register:** Stores ALU data; loads only if it is a C-instruction and destination bit $d_2$ (`instruction[4]`) is 1.
  - **Memory Write (`writeM`):** Asserted only during C-instructions when destination bit $d_3$ (`instruction[3]`) is 1.
  - **Program Counter (PC) Jump Logic:** Evaluates ALU status flags:
    $$\text{pos} = \neg\text{zr} \land \neg\text{ng}$$
    $$\text{jump} = (j_1 \land \text{ng}) \lor (j_2 \land \text{zr}) \lor (j_3 \land \text{pos})$$
    If `isC` and `jump`, PC loads the target address from the A-register (`load=pcLoad`). Otherwise, it increments (`inc=true`). If `reset==1`, PC restarts at 0.

- **`Memory.hdl` (Address Space Multiplexer):**
  - Contiguous 15-bit address space ($32,768$ words):
    - `0x0000..0x3FFF` ($0 - 16383$): Data RAM16K (`address[14] == 0`).
    - `0x4000..0x5FFF` ($16384 - 24575$): Screen memory map (`address[14..13] == 10`).
    - `0x6000` ($24576$): Keyboard memory-mapped register (`address[14..13] == 11`).
  - Uses `DMux` to route incoming `load` strobe to either `RAM16K` or `Screen` (Keyboard is read-only).
  - Uses `Mux16` to select output from `RAM16K`, `Screen`, or `Keyboard`.

- **`Computer.hdl` (Top-Level Machine):**
  - Wires `ROM32K(address=pc, out=instruction)` to `CPU`.
  - Wires `CPU(outM, writeM, addressM)` to `Memory(in, load, address)`.
  - Routes `Memory.out` back to `CPU.inM`.

---

### 2.2 Python Hack Assembler (`part_b_assembler/assembler.py`)
- **Why Two Passes?**
  Forward jumps cannot be resolved on a single pass without back-patching because an instruction might say `@FORWARD_LABEL` before `(FORWARD_LABEL)` is encountered.
- **Pass 1:**
  - Strips comments (`//...`), trims whitespace, and skips empty lines.
  - Keeps a `rom_address` counter.
  - When a label `(LABEL)` is found, registers `symbol_table[LABEL] = rom_address`.
  - Labels do not increment `rom_address`.
- **Pass 2:**
  - Translates executable instructions into 16-bit binary.
  - **A-instructions (`@xxx`):** If digits, converts to 15-bit binary. If predefined or known label, looks up address. If unseen variable (e.g. `@color`), assigns next available RAM address starting from 16 onward.
  - **C-instructions (`dest=comp;jump`):** Splits `dest`, `comp`, and `jump`. Looks up binary bits in dictionary tables and outputs `111 + comp_bits + dest_bits + jump_bits`.
- **Personalized Feature ($K \bmod 3 = 23 \bmod 3 = 2$):**
  Detects duplicate label declarations in Pass 1. If `(LOOP)` appears twice, prints:
  `Warning: Label 'LOOP' declared multiple times (duplicate found at line X)`.

---

### 2.3 Interactive Box Application (`part_c_box_program/Box.asm`)
- **Personalized Formulas for $K = 23$:**
  - Starting Row: $K = 23$
  - Height: $20$ scanlines (rows 23 to 42)
  - Width: $16 \times ((23 \bmod 4) + 1) = 64$ pixels ($4$ words per row)
  - Screen Memory Base Address: $\text{SCREEN} + 32 \times 23 = 16384 + 736 = 17120$.
- **Screen Memory Layout:**
  - One screen row = 32 words ($32 \times 16 = 512$ pixels).
  - Writing `-1` (`1111111111111111` in two's complement) sets 16 horizontal pixels black.
  - Writing `0` sets 16 horizontal pixels white.
- **Keyboard Detection:**
  Reads address $24576$ (`KBD`). If `D != 0`, sets `color = -1`. If `D == 0`, sets `color = 0`.
- **Drawing Loop:**
  - Outer loop runs 20 times (`rows_left = 20`).
  - Inner loop writes `color` across 4 consecutive words (`cols_left = 4`).
  - Advances row pointer by 32: `row_ptr = row_ptr + 32`.
  - Repeats continuously, resulting in instant response and zero screen flicker.

---

## 3. Possible On-The-Spot Live Modifications & Code Changes

During the viva, the examiner may ask: *"Make a small change in your code on the spot."*  
Here is exactly what to modify:

### Scenario 1: "Move the box down by 10 rows (from Row 23 to Row 33)"
- **Where:** In `Box.asm` under `(RENDER)`:
- **Calculation:** New start address = $16384 + 32 \times 33 = 16384 + 1056 = 17440$.
- **Change:**
  ```hack
  // OLD:
  @17120
  D=A
  @row_ptr
  M=D

  // NEW:
  @17440
  D=A
  @row_ptr
  M=D
  ```

### Scenario 2: "Double the width of the box (from 64 pixels to 128 pixels)"
- **Where:** In `Box.asm` under `(ROW_LOOP)`:
- **Calculation:** $128\text{ pixels} \div 16 = 8\text{ words}$ (was 4 words).
- **Change:**
  ```hack
  // OLD:
  @4
  D=A
  @cols_left
  M=D

  // NEW:
  @8
  D=A
  @cols_left
  M=D
  ```

### Scenario 3: "Change the height of the box from 20 rows to 30 rows"
- **Where:** In `Box.asm` under `(RENDER)`:
- **Change:**
  ```hack
  // OLD:
  @20
  D=A
  @rows_left
  M=D

  // NEW:
  @30
  D=A
  @rows_left
  M=D
  ```

### Scenario 4: "Shift the box from the left edge towards the middle of the screen"
- **Where:** In `Box.asm` under `(RENDER)`:
- **Calculation:** To shift right by 10 words (160 pixels), add 10 to the starting address: $17120 + 10 = 17130$.
- **Change:**
  ```hack
  // OLD:
  @17120
  D=A
  @row_ptr
  M=D

  // NEW:
  @17130
  D=A
  @row_ptr
  M=D
  ```

### Scenario 5: "Invert behavior: Show box when NO key is pressed, hide when key is pressed"
- **Where:** In `Box.asm` under `(POLL_KEYBOARD)`:
- **Change:**
  ```hack
  // Swap the jump condition or colors:
  @KBD
  D=M
  // Change D;JNE (jump if not equal to zero) to D;JEQ (jump if equal to zero):
  @SET_BLACK
  D;JEQ
  ```

---

## 4. Top 25 Viva Questions & Direct Answers

#### Q1: What is the Von Neumann architecture, and how does Hack follow it?
**Answer:** A Von Neumann architecture uses a shared memory bus structure where data and instructions are treated in memory through sequential execution governed by a program counter. Hack follows this with a CPU connected to memory via address, data, and control lines, though it employs a Harvard split for instruction fetching (`ROM32K`) and data storage (`Memory`).

#### Q2: What is the difference between an A-instruction and a C-instruction in Hack?
**Answer:** An A-instruction starts with bit `0` and loads a 15-bit constant into the A-register (`0vvvvvvvvvvvvvvv`). A C-instruction starts with bit `1` (`111accccccdddjjj`) and performs an ALU computation (`comp`), stores the result into destinations (`dest`), and conditionally branches (`jump`).

#### Q3: What is the role of the `a`-bit in a C-instruction?
**Answer:** Bit 12 (the `a`-bit) determines whether the ALU computes using the content of the A-register (`a = 0`) or the memory operand M at address A (`a = 1`, i.e., `RAM[A]`).

#### Q4: Why does the Hack CPU have both A-register and D-register?
**Answer:** The D-register is purely a data register for holding intermediate values. The A-register is dual-purpose: it can hold data values, but its contents also directly drive the address bus for data memory (`addressM`) and program memory (`ROM`).

#### Q5: How is memory-mapped I/O implemented in the Hack computer?
**Answer:** Peripherals are mapped directly into the CPU's memory address space. Reading address $24576$ reads the keyboard's scan-code register. Writing to addresses $16384..24575$ directly changes pixels on the screen. No special I/O instructions are needed.

#### Q6: How many pixels does one 16-bit word on the screen represent?
**Answer:** Exactly 16 pixels. Bit 0 is the leftmost pixel and bit 15 is the rightmost.

#### Q7: Why do we write `-1` to turn pixels black?
**Answer:** In 16-bit two's complement, `-1` is represented as all binary ones (`1111111111111111`). In the Hack display hardware, a `1` bit turns a pixel black, so writing `-1` turns all 16 pixels black in a single instruction.

#### Q8: How did you calculate your box base address of 17120?
**Answer:** Screen memory begins at address $16384$ (`SCREEN`). Each screen row contains 32 words ($512 \div 16$). For my personal number $K = 23$, the starting row is 23. Therefore:
$$\text{Base Address} = 16384 + (32 \times 23) = 16384 + 736 = 17120$$

#### Q9: How wide is your box in pixels and words?
**Answer:** The width formula is $16 \times ((K \bmod 4) + 1)$. For $K = 23$:
$$23 \bmod 4 = 3 \implies 16 \times (3 + 1) = 64\text{ pixels}$$
Since each word is 16 pixels, $64 \div 16 = 4\text{ words}$.

#### Q10: How does your assembler resolve forward-referencing labels?
**Answer:** By using a two-pass architecture. Pass 1 reads the code, ignores comments and whitespace, tracks ROM line numbers, and maps each `(LABEL)` to the current ROM counter. Pass 2 translates instructions and can look up any label regardless of whether it appeared earlier or later.

#### Q11: Where are user variables allocated in Hack RAM, and why?
**Answer:** User variables (like `@color` or `@row_ptr`) are allocated starting at RAM address 16 onward. Addresses 0 to 15 are reserved for predefined virtual registers (`R0` through `R15`, `SP`, `LCL`, `ARG`, `THIS`, `THAT`).

#### Q12: What is your personalized assembler feature, and how does it work?
**Answer:** For $K = 23$, $23 \bmod 3 = 2$. The feature prints a compiler warning if the same label is declared more than once in the source file, which helps detect duplicate jump targets.

#### Q13: What happens in `Computer.hdl` when the `reset` button is pressed?
**Answer:** The `reset` signal is fed directly into `CPU.reset`. In the CPU, when `reset == 1`, the Program Counter (PC) register sets its internal counter to 0, causing instruction fetching to restart from address 0 in `ROM32K`.

#### Q14: Why does your box program not cause screen flicker?
**Answer:** Because it does not clear the entire screen. It updates strictly the 80 memory words ($20\text{ rows} \times 4\text{ words}$) belonging to the box bounding box, executing in under 600 cycles.

#### Q15: How does `Memory.hdl` decode addresses between RAM, Screen, and Keyboard?
**Answer:** Using the top two address bits (`address[14..13]`):
- `0x`: bit 14 is 0 $\rightarrow$ `RAM16K` ($0..16383$).
- `10`: bit 14 is 1 and bit 13 is 0 $\rightarrow$ `Screen` ($16384..24575$).
- `11`: bit 14 is 1 and bit 13 is 1 $\rightarrow$ `Keyboard` ($24576$).

#### Q16: Can the Hack CPU write to the Keyboard register?
**Answer:** No. The Keyboard register is read-only. In `Memory.hdl`, write strobes (`load`) routed to the keyboard address are discarded.

#### Q17: What was the genuine bug you encountered and fixed during development?
**Answer:** When assembling `Box.asm`, the assembler reported `Invalid computation field 'M+D'` at line 99. The Hack ALU specifies addition as `D+M` because D is on input $x$ and M is on input $y$. I fixed `Box.asm` to use `M=D+M` and also added commutative aliases to the assembler for robustness.

#### Q18: What are the three jump condition bits in a C-instruction?
**Answer:** Bits 2, 1, 0 ($j_1, j_2, j_3$):
- $j_1$: jump if output is negative (`out < 0`, `ng == 1`).
- $j_2$: jump if output is zero (`out == 0`, `zr == 1`).
- $j_3$: jump if output is positive (`out > 0`, `zr == 0` and `ng == 0`).

#### Q19: What is the purpose of `writeM` in the CPU?
**Answer:** `writeM` is a 1-bit control output. It is asserted (set to 1) only during a C-instruction when destination bit $d_3$ is 1, indicating that the ALU output `outM` should be written into memory at address `addressM`.

#### Q20: How many instructions are in your final `Box.hack` file?
**Answer:** Exactly 53 instructions.

#### Q21: What is the function of the Program Counter (PC)?
**Answer:** The PC outputs the 15-bit address of the next instruction to fetch from ROM. On every clock cycle, it either increments (`PC++`), loads a jump address (`PC = A`), or resets to zero (`PC = 0`).

#### Q22: What is the maximum number of instructions Hack ROM can hold?
**Answer:** $32\text{K}$ instructions ($32,768$ 16-bit words), addressed by 15 bits (`0x0000` to `0x7FFF`).

#### Q23: Why do label pseudo-instructions not increment the ROM counter?
**Answer:** Because labels like `(LOOP)` generate no machine code. They exist only as symbolic markers for the assembler to remember an instruction address.

#### Q24: How does the CPU know whether an ALU output is positive?
**Answer:** The ALU outputs two status flags: `zr` (is zero) and `ng` (is negative). The CPU computes strictly positive using logic gates: $\text{pos} = \text{Not}(\text{zr}) \text{ And } \text{Not}(\text{ng})$.

#### Q25: How does your implementation fulfill CO1 through CO4?
**Answer:**
- **CO1:** Demonstrating logic gate combinations and memory-mapped address decoding in HDL.
- **CO2:** Implementing CPU microarchitecture, ALU multiplexing, and fetch-decode-execute cycles.
- **CO3:** Developing low-level Hack assembly routines with register allocation and I/O interaction.
- **CO4:** Designing an end-to-end two-pass assembler translating symbolic code into binary machine language.
