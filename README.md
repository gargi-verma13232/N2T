# Nand to Tetris — Complete Coursework & Capstone Project

**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Gargi Verma  
**University Roll Number:** 2501010223  
**Personal Parameter (K):** 23  

---

## 📌 Repository Overview

This repository houses the complete academic and practical submissions for the **Nand to Tetris – I (ETCCNT301)** course, spanning foundational theory, hands-on laboratory experiments, and an end-to-end computer engineering Capstone Project.

```
N2T/
├── 1. Theory Assignments/            # Unit Theory Assignments (Boolean logic, sequential chips, architecture)
│   ├── GargiVerma_2501010223_Unit1.pdf
│   └── GargiVerma_2501010223_Unit2.pdf
│
├── 2. Lab Assignments/               # Practical Laboratory Submissions
│   ├── GargiVerma_2501010223_Lab1.pdf
│   └── GargiVerma_2501010223_Lab2.pdf
│
└── 3. Capstone Project/              # End-to-End Hack Computer & Box Application
    └── Project Files/
        ├── capstone/                 # Final submission deliverables (CPU, Memory, Computer, Assembler, Box)
        ├── documentation/            # Architecture overview and comprehensive Viva preparation guide
        ├── part_a_hardware/          # HDL chips (CPU, Memory, Computer) and official test suites
        ├── part_b_assembler/         # Custom Python Hack Assembler with personalized features
        ├── part_c_box_program/       # Interactive graphics Box application in Hack assembly
        ├── reports/                  # Phase-by-phase reports and final 4-page academic report
        └── tools/                    # Hardware simulator, CPU emulator, test scripts, and runners
```

---

## 🏆 Capstone Project: "Make the Computer Draw a Box"

### Project Specifications
- **Hardware Architecture (Part A):** Full Hack computer architecture implemented in HDL (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`). Verified 100% against official Nand to Tetris test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`).
- **Hack Assembler (Part B):** Independent two-pass Python Hack Assembler (`assembler.py`) supporting symbol resolution, binary instruction generation, and personalized Feature 2 ($K \bmod 3 = 2$: duplicate label declaration detection). Verified bit-for-bit against official benchmarks (`Add`, `Max`, `Rect`, `Pong`).
- **Interactive Box Program (Part C):** Real-time keyboard-driven graphics application written directly in Hack assembly (`Box.asm` $\rightarrow$ `Box.hack`):
  - **Starting Row:** Row 23 ($K = 23$)
  - **Height:** 20 scanlines (Rows 23 to 42)
  - **Width:** 64 pixels ($16 \times ((23 \bmod 4) + 1)$) across 4 16-bit words
  - **Behavior:** Dynamically renders a solid black rectangle when any key is pressed; immediately clears back to clean white screen when released.

---

## 🚀 Quick Execution Guide

### 1. Assemble the Box Program
```bash
cd "3. Capstone Project/Project Files"
python capstone/assembler.py capstone/Box.asm capstone/Box.hack
```

### 2. Verify Hardware in Hardware Simulator
```bash
python tools/run_hdl_test.py part_a_hardware/tests/CPU.tst
python tools/run_hdl_test.py part_a_hardware/tests/Memory.tst
python tools/run_hdl_test.py part_a_hardware/tests/ComputerAdd.tst
```

### 3. Run System-Wide Audit
```bash
python tools/verify_all.py
```

---

## 👤 Author
**Gargi Verma**  
School of Engineering & Technology  
K.R. Mangalam University  
Roll Number: `2501010223`  
GitHub: [@gargi-verma13232](https://github.com/gargi-verma13232)
