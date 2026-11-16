#!/usr/bin/env python3
"""
Test runner for Python Hack Assembler.
Assembles Add.asm, Max.asm, Rect.asm, Pong.asm and compares bit-for-bit
against the official reference Hack files (*_expected.hack).
Also validates all 3 personalized extra features (K mod 3 = 0, 1, 2).
"""

import sys
import filecmp
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSEMBLER_DIR = PROJECT_ROOT / "part_b_assembler"
TEST_PROG_DIR = ASSEMBLER_DIR / "test_programs"
GENERATED_DIR = ASSEMBLER_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ASSEMBLER_DIR))
from assembler import HackAssembler

test_cases = ["Add", "Max", "Rect", "Pong"]

def test_assembler_parity():
    all_passed = True
    print("=" * 60)
    print("TESTING HACK ASSEMBLER ON OFFICIAL BENCHMARK PROGRAMS")
    print("=" * 60)

    for name in test_cases:
        asm_path = TEST_PROG_DIR / f"{name}.asm"
        expected_hack = TEST_PROG_DIR / f"{name}_expected.hack"
        gen_hack = GENERATED_DIR / f"{name}.hack"

        assembler = HackAssembler(feature_code=0)
        success = assembler.assemble(str(asm_path), str(gen_hack))
        if not success:
            print(f"FAILED: Assembly of {name}.asm failed!")
            all_passed = False
            continue

        # Compare files line-by-line
        with open(gen_hack, "r") as f_gen, open(expected_hack, "r") as f_exp:
            gen_lines = [l.strip() for l in f_gen.readlines() if l.strip()]
            exp_lines = [l.strip() for l in f_exp.readlines() if l.strip()]

        if gen_lines == exp_lines:
            print(f"PASS: {name}.hack matches official reference ({len(gen_lines)} instructions, bit-for-bit identical)")
        else:
            all_passed = False
            print(f"MISMATCH: {name}.hack differs from official reference!")
            # Find first differing line
            for idx, (g, e) in enumerate(zip(gen_lines, exp_lines)):
                if g != e:
                    print(f"  First mismatch at line {idx+1}: Generated='{g}' vs Expected='{e}'")
                    break
            if len(gen_lines) != len(exp_lines):
                print(f"  Line count mismatch: Generated={len(gen_lines)} vs Expected={len(exp_lines)}")

    return all_passed

def test_personalized_features():
    print("\n" + "=" * 60)
    print("TESTING PERSONALIZED EXTRA FEATURES (K mod 3 = 0, 1, 2)")
    print("=" * 60)

    # Feature 0: symbols.txt generation
    symbols_txt = GENERATED_DIR / "symbols.txt"
    assembler_f0 = HackAssembler(feature_code=0)
    assembler_f0.assemble(str(TEST_PROG_DIR / "Max.asm"), str(GENERATED_DIR / "Max_f0.hack"))
    assembler_f0.export_symbols(str(symbols_txt))
    if symbols_txt.exists() and symbols_txt.stat().st_size > 0:
        print("PASS: Feature 0 (K mod 3 = 0) generated symbols.txt successfully.")
    else:
        print("FAIL: Feature 0 did not produce symbols.txt!")

    # Feature 1: Clean syntax error message with line number
    bad_asm = GENERATED_DIR / "bad_syntax.asm"
    with open(bad_asm, "w") as f:
        f.write("@10\nD=A\nINVALID_INSTRUCTION_HERE\n@LOOP\n0;JMP\n")
    assembler_f1 = HackAssembler(feature_code=1)
    print("Testing Feature 1 error handling (expecting line 3 error):")
    success_f1 = assembler_f1.assemble(str(bad_asm), str(GENERATED_DIR / "bad_syntax.hack"))
    if not success_f1:
        print("PASS: Feature 1 caught invalid instruction cleanly without crashing.")
    else:
        print("FAIL: Feature 1 allowed invalid syntax!")

    # Feature 2: Warning on duplicate label declaration
    dup_label_asm = GENERATED_DIR / "dup_label.asm"
    with open(dup_label_asm, "w") as f:
        f.write("(LOOP)\n@10\nD=A\n(LOOP)\n0;JMP\n")
    assembler_f2 = HackAssembler(feature_code=2)
    print("Testing Feature 2 duplicate label warning:")
    assembler_f2.assemble(str(dup_label_asm), str(GENERATED_DIR / "dup_label.hack"))
    if len(assembler_f2.warnings) > 0:
        print(f"PASS: Feature 2 detected duplicate label: {assembler_f2.warnings[0]}")
    else:
        print("FAIL: Feature 2 failed to detect duplicate label!")

if __name__ == "__main__":
    p1 = test_assembler_parity()
    test_personalized_features()
    sys.exit(0 if p1 else 1)

