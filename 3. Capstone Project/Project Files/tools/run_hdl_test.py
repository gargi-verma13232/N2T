#!/usr/bin/env python3
"""
HDL Test Runner for Nand to Tetris Capstone Project.
Executes official HardwareSimulatorMain via JDK 21 and validates output.
"""
import os
import sys
import subprocess
from pathlib import Path

# Locate repository root and tools directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
JAVA_EXE = r"C:\Program Files\Java\jdk-21.0.10\bin\java.exe"

# If default JDK path is not found, fallback to 'java'
if not os.path.exists(JAVA_EXE):
    JAVA_EXE = "java"

CLASSPATH = (
    ".;"
    "bin/classes;"
    "bin/lib/Hack.jar;"
    "bin/lib/HackGUI.jar;"
    "bin/lib/Simulators.jar;"
    "bin/lib/SimulatorsGUI.jar;"
    "bin/lib/Compilers.jar"
)

def run_test(tst_path: str):
    tst_file = Path(tst_path).resolve()
    if not tst_file.exists():
        print(f"Error: Test file not found: {tst_file}")
        return False, f"Test file not found: {tst_file}"

    cmd = [
        JAVA_EXE,
        "-classpath",
        CLASSPATH,
        "HardwareSimulatorMain",
        str(tst_file)
    ]

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(TOOLS_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        output = stdout + ("\n" + stderr if stderr else "")
        success = "Comparison ended successfully" in output or "End of script - Comparison ended successfully" in output
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Execution timed out (30 seconds)"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_hdl_test.py <path_to_tst>")
        sys.exit(1)
    
    passed, message = run_test(sys.argv[1])
    print(message)
    sys.exit(0 if passed else 1)

