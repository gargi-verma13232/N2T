# Phase 5 Report: GitHub Submission & Staging Readiness

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
Phase 5 organizes the final submission bundle in strict compliance with Section 5 ("What to submit") of the official assignment specification (`Capstone_Project.pdf`). A clean `capstone/` folder has been staged containing the exact six required core deliverable files. The Git version control repository has been initialized, configured with appropriate metadata and `.gitignore` filters, and committed locally. No unauthorized push operations to remote repositories were made, ensuring full adherence to development instructions.

---

## 2. Objectives
1. Prepare the exact submission folder required by the assignment: `capstone/`.
2. Stage the mandatory files in `capstone/`:
   - `CPU.hdl`
   - `Memory.hdl`
   - `Computer.hdl`
   - `assembler.py`
   - `Box.asm`
   - `Box.hack`
3. Inspect and verify local version control repository status.
4. Verify that temporary logs, caches, and test artifacts are properly excluded from version control via `.gitignore`.
5. Provide a step-by-step submission checklist and instructions for the student's final submission.

---

## 3. Tasks Completed
- [x] Staged pristine copies of `CPU.hdl`, `Memory.hdl`, `Computer.hdl`, `assembler.py`, `Box.asm`, and `Box.hack` in `capstone/`.
- [x] Formatted and committed repository with comprehensive `README.md`.
- [x] Configured Git metadata for student Gargi Verma (`2501010223`).
- [x] Created clean `.gitignore` to prevent committing bytecode, temporary logs, or caches.
- [x] Verified `git status`: Working tree is 100% clean, master branch at commit `5c085be`.

---

## 4. Final Folder Structure
```
NAND_TO_TETRIS_CAPSTONE/
├── .gitignore
├── PROJECT_PROGRESS.md
├── README.md
├── student_config.json
├── student_config.py
│
├── capstone/                               <-- SUBMISSION FOLDER
│   ├── CPU.hdl                             (Part A)
│   ├── Memory.hdl                          (Part A)
│   ├── Computer.hdl                        (Part A)
│   ├── assembler.py                        (Part B)
│   ├── Box.asm                             (Part C)
│   └── Box.hack                            (Part C)
│
├── part_a_hardware/
│   ├── CPU.hdl
│   ├── Memory.hdl
│   ├── Computer.hdl
│   ├── screenshots/
│   │   ├── CPU_test_result.png
│   │   ├── Memory_test_result.png
│   │   ├── ComputerAdd_test_result.png
│   │   ├── ComputerMax_test_result.png
│   │   └── ComputerRect_test_result.png
│   └── tests/
│       ├── CPU.tst, CPU.cmp
│       ├── Memory.tst, Memory.cmp
│       ├── ComputerAdd.tst, ComputerAdd.cmp, Add.hack
│       ├── ComputerMax.tst, ComputerMax.cmp, Max.hack
│       └── ComputerRect.tst, ComputerRect.cmp, Rect.hack
│
├── part_b_assembler/
│   ├── assembler.py
│   ├── generated/
│   │   └── symbols.txt
│   ├── screenshots/
│   │   ├── assembler_benchmark_verification.png
│   │   └── assembler_extra_features_verification.png
│   └── test_programs/
│       ├── Add.asm, Add_expected.hack
│       ├── Max.asm, Max_expected.hack
│       ├── Rect.asm, Rect_expected.hack
│       └── Pong.asm, Pong_expected.hack
│
├── part_c_box_program/
│   ├── Box.asm
│   ├── Box.hack
│   └── screenshots/
│       ├── Box_screen_key_pressed.png
│       ├── Box_screen_key_released.png
│       ├── Box_pixel_coordinates_zoomed.png
│       └── Box_cpu_emulator_test.png
│
├── reports/
│   ├── phase_reports/
│   │   ├── PHASE_0_REPORT.md
│   │   ├── PHASE_1_REPORT.md
│   │   ├── PHASE_2_REPORT.md
│   │   ├── PHASE_3_REPORT.md
│   │   ├── PHASE_4_REPORT.md
│   │   └── PHASE_5_REPORT.md
│   ├── test_reports/
│   └── Final_Capstone_Report.pdf           (Phase 6 Deliverable)
│
├── documentation/
│   ├── PROJECT_OVERVIEW.md
│   └── VIVA_PREPARATION.md                 (Phase 7 Deliverable)
│
└── tools/
    ├── run_hdl_test.py
    ├── test_assembler.py
    ├── simulate_box.py
    ├── verify_all.py
    └── ... (Nand to Tetris runtime tools)
```

---

## 5. Required Files Verification
| Deliverable File | Target Directory | File Size | Description | Verified |
| :--- | :--- | :---: | :--- | :---: |
| `CPU.hdl` | `capstone/` | 5,491 bytes | Central Processing Unit hardware chip | [✓] |
| `Memory.hdl` | `capstone/` | 2,736 bytes | Complete 32K memory space hardware chip | [✓] |
| `Computer.hdl` | `capstone/` | 1,877 bytes | Top-level Hack Computer architecture chip | [✓] |
| `assembler.py` | `capstone/` | 11,021 bytes | Two-pass Python Hack assembler | [✓] |
| `Box.asm` | `capstone/` | 2,233 bytes | Interactive Hack box application ($K=23$) | [✓] |
| `Box.hack` | `capstone/` | 954 bytes | Machine language program (53 instructions) | [✓] |

---

## 6. Git Status Summary
```
On branch master
nothing to commit, working tree clean
Last Commit: 5c085be
Author: Gargi Verma <gargi.verma@krmangalam.edu.in>
Commit Message: Complete Nand to Tetris Capstone Project (CO1-CO4) - Gargi Verma (2501010223)
```

---

## 7. Submission Checklist
- [x] Core `capstone/` directory prepared with all 6 required files.
- [x] No unrelated or temporary files in `capstone/`.
- [x] All HDL files tested and passing official test suites.
- [x] Python assembler matches official references bit-for-bit.
- [x] Box application verified and screenshot evidence preserved.
- [x] Git repository configured locally with clean history.
- [ ] Final University Report PDF generated (Phase 6).
- [ ] Viva Voce Guide completed (Phase 7).

---

## 8. Remaining Manual Steps for the Student
When submitting your project:
1. **GitHub Lab Repository:** If your instructor requested placing `capstone/` into your existing GitHub repository:
   - Simply copy the folder `D:\KRMU 2025\SEMESTER-3\NAND\Nand2TetrisCapstone\capstone` directly into your existing course lab repository.
   - Run:
     ```bash
     git add capstone/
     git commit -m "Submit Nand to Tetris Capstone Project (Gargi Verma - 2501010223)"
     git push origin main
     ```
2. **ZOSIMA Report Upload:** Upload `reports/Final_Capstone_Report.pdf` to the university portal before the submission deadline.
3. **Viva Voce:** Review `documentation/VIVA_PREPARATION.md` before your 5-minute evaluation.
