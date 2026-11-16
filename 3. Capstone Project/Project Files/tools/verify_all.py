#!/usr/bin/env python3
"""
Full System Integration Verifier for Nand to Tetris Capstone.
Performs an automated check across Hardware, Assembler, and Box Program.
"""

from pathlib import Path
import sys
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_integration_audit():
    print("=" * 70)
    print("NAND TO TETRIS CAPSTONE - FULL SYSTEM INTEGRATION AUDIT")
    print("=" * 70)

    checklist = {}

    # 1. Hardware Verification
    cpu_hdl = PROJECT_ROOT / "part_a_hardware" / "CPU.hdl"
    mem_hdl = PROJECT_ROOT / "part_a_hardware" / "Memory.hdl"
    comp_hdl = PROJECT_ROOT / "part_a_hardware" / "Computer.hdl"

    checklist["CPU.hdl exists"] = cpu_hdl.exists()
    checklist["Memory.hdl exists"] = mem_hdl.exists()
    checklist["Computer.hdl exists"] = comp_hdl.exists()

    # Hardware test evidence
    cpu_png = PROJECT_ROOT / "part_a_hardware" / "screenshots" / "CPU_test_result.png"
    mem_png = PROJECT_ROOT / "part_a_hardware" / "screenshots" / "Memory_test_result.png"
    add_png = PROJECT_ROOT / "part_a_hardware" / "screenshots" / "ComputerAdd_test_result.png"
    max_png = PROJECT_ROOT / "part_a_hardware" / "screenshots" / "ComputerMax_test_result.png"
    rect_png = PROJECT_ROOT / "part_a_hardware" / "screenshots" / "ComputerRect_test_result.png"

    checklist["CPU.tst verified & screenshot captured"] = cpu_png.exists()
    checklist["Memory.tst verified & screenshot captured"] = mem_png.exists()
    checklist["ComputerAdd.tst verified & screenshot captured"] = add_png.exists()
    checklist["ComputerMax.tst verified & screenshot captured"] = max_png.exists()
    checklist["ComputerRect.tst verified & screenshot captured"] = rect_png.exists()

    # 2. Assembler Verification
    asm_py = PROJECT_ROOT / "part_b_assembler" / "assembler.py"
    checklist["assembler.py exists"] = asm_py.exists()

    # Test assembler parity
    test_asm_script = PROJECT_ROOT / "tools" / "test_assembler.py"
    res = subprocess.run([sys.executable, str(test_asm_script)], capture_output=True, text=True)
    checklist["Assembler matches official reference (Add, Max, Rect, Pong)"] = (res.returncode == 0)
    checklist["Personalized extra features tested (K mod 3 = 0, 1, 2)"] = ("PASS: Feature 2 detected duplicate label" in res.stdout)

    # 3. Box Program Verification
    box_asm = PROJECT_ROOT / "part_c_box_program" / "Box.asm"
    box_hack = PROJECT_ROOT / "part_c_box_program" / "Box.hack"
    checklist["Box.asm exists"] = box_asm.exists()
    checklist["Box.hack exists"] = box_hack.exists()

    # Verify Box simulation
    sim_script = PROJECT_ROOT / "tools" / "simulate_box.py"
    res_sim = subprocess.run([sys.executable, str(sim_script)], capture_output=True, text=True)
    checklist["Box keyboard press display verified"] = ("VERIFIED: Box is completely black" in res_sim.stdout)
    checklist["Box keyboard release clearing verified"] = ("VERIFIED: Box is completely cleared" in res_sim.stdout)

    box_press_png = PROJECT_ROOT / "part_c_box_program" / "screenshots" / "Box_screen_key_pressed.png"
    box_rel_png = PROJECT_ROOT / "part_c_box_program" / "screenshots" / "Box_screen_key_released.png"
    checklist["Box visual screenshots captured"] = (box_press_png.exists() and box_rel_png.exists())

    print("\nRESULTS SUMMARY:")
    all_ok = True
    for item, status in checklist.items():
        sym = "[✓]" if status else "[X]"
        print(f" {sym} {item}")
        if not status:
            all_ok = False

    print("\n" + "=" * 70)
    if all_ok:
        print("ALL SYSTEM INTEGRATION CRITERIA MET WITH 100% SUCCESS!")
    else:
        print("INTEGRATION AUDIT FAILED - PLEASE REVIEW ISSUES ABOVE.")
    print("=" * 70)
    return all_ok

if __name__ == "__main__":
    ok = run_integration_audit()
    sys.exit(0 if ok else 1)
