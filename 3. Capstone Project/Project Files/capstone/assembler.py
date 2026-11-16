#!/usr/bin/env python3
"""
Hack Assembler for Nand to Tetris Capstone Project.
Translates Hack Assembly (.asm) into 16-bit Hack machine language (.hack).
Developed from scratch in Python.

Supports:
- Predefined symbols (R0-R15, SP, LCL, ARG, THIS, THAT, SCREEN, KBD)
- Label resolution via Pass 1
- Dynamic RAM variable allocation starting at address 16 via Pass 2
- Instruction translation (A-instruction and C-instruction)
- Personalized features based on K mod 3:
    * K mod 3 = 0: Save all labels and variables with their addresses in symbols.txt
    * K mod 3 = 1: Clear error message with line number for invalid instructions
    * K mod 3 = 2: Print warning if the same label is declared twice
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add project root to sys.path to access student_config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from student_config import load_config, get_parameters
except ImportError:
    load_config = lambda: {}
    get_parameters = lambda k=None: {"assembler_feature_code": 0}

# -------------------------------------------------------------
# Predefined Symbol Table
# -------------------------------------------------------------
PREDEFINED_SYMBOLS: Dict[str, int] = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
}

# -------------------------------------------------------------
# C-Instruction Lookup Tables
# -------------------------------------------------------------
COMP_TABLE: Dict[str, str] = {
    # a = 0 (operations on A register)
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",

    # a = 1 (operations on M memory operand)
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101",
}

DEST_TABLE: Dict[str, str] = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "DM":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

JUMP_TABLE: Dict[str, str] = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

class HackAssembler:
    def __init__(self, feature_code: Optional[int] = None):
        if feature_code is None:
            params = get_parameters()
            self.feature_code = params.get("assembler_feature_code", 0)
        else:
            self.feature_code = feature_code
            
        self.symbol_table = PREDEFINED_SYMBOLS.copy()
        self.user_labels: Dict[str, int] = {}
        self.user_variables: Dict[str, int] = {}
        self.next_var_address = 16
        self.warnings: List[str] = []

    def clean_line(self, raw_line: str) -> str:
        """Removes comments and extraneous whitespace."""
        code = raw_line.split("//")[0]
        return code.strip().replace(" ", "")

    def pass_one(self, lines: List[str]) -> List[Tuple[int, str]]:
        """
        First reading: records label addresses in the symbol table.
        Labels do not advance the ROM instruction counter.
        Handles Feature 2: Warning on duplicate label declaration.
        """
        executable_lines: List[Tuple[int, str]] = []
        rom_address = 0

        for line_num, raw_line in enumerate(lines, start=1):
            cleaned = self.clean_line(raw_line)
            if not cleaned:
                continue

            if cleaned.startswith("(") and cleaned.endswith(")"):
                label = cleaned[1:-1].strip()
                if not label:
                    if self.feature_code == 1:
                        print(f"Line {line_num}: invalid instruction (empty label declaration)")
                    continue

                # Feature 2 check: duplicate label warning
                if label in self.symbol_table:
                    msg = f"Warning: Label '{label}' declared multiple times (duplicate found at line {line_num})"
                    self.warnings.append(msg)
                    if self.feature_code == 2:
                        print(msg)
                else:
                    self.symbol_table[label] = rom_address
                    self.user_labels[label] = rom_address
            else:
                executable_lines.append((line_num, cleaned))
                rom_address += 1

        return executable_lines

    def translate_a_instruction(self, line_num: int, instruction: str) -> str:
        """Translates @value into 16-bit binary."""
        symbol = instruction[1:]

        # Case 1: Non-negative integer constant
        if symbol.isdigit():
            val = int(symbol)
            if val > 32767:
                raise ValueError(f"Constant exceeds 15 bits (0..32767): {val}")
            return f"0{val:015b}"

        # Case 2: Existing symbol (predefined or label or already allocated variable)
        if symbol in self.symbol_table:
            val = self.symbol_table[symbol]
            return f"0{val:015b}"

        # Case 3: New variable -> allocate in RAM starting at 16
        val = self.next_var_address
        self.symbol_table[symbol] = val
        self.user_variables[symbol] = val
        self.next_var_address += 1
        return f"0{val:015b}"

    def translate_c_instruction(self, line_num: int, instruction: str) -> str:
        """Translates dest=comp;jump into 16-bit binary."""
        # Split dest
        if "=" in instruction:
            dest_part, remainder = instruction.split("=", 1)
        else:
            dest_part = ""
            remainder = instruction

        # Split jump
        if ";" in remainder:
            comp_part, jump_part = remainder.split(";", 1)
        else:
            comp_part = remainder
            jump_part = ""

        # Validate comp
        if comp_part not in COMP_TABLE:
            raise ValueError(f"Invalid computation field '{comp_part}'")

        # Validate dest
        if dest_part not in DEST_TABLE:
            raise ValueError(f"Invalid destination field '{dest_part}'")

        # Validate jump
        if jump_part not in JUMP_TABLE:
            raise ValueError(f"Invalid jump field '{jump_part}'")

        comp_bits = COMP_TABLE[comp_part]
        dest_bits = DEST_TABLE[dest_part]
        jump_bits = JUMP_TABLE[jump_part]

        return f"111{comp_bits}{dest_bits}{jump_bits}"

    def assemble(self, asm_filepath: str, output_filepath: Optional[str] = None) -> bool:
        """Assembles a Hack .asm file into .hack machine code."""
        asm_path = Path(asm_filepath).resolve()
        if not asm_path.exists():
            print(f"Error: Source file '{asm_filepath}' not found.")
            return False

        if output_filepath is None:
            out_path = asm_path.with_suffix(".hack")
        else:
            out_path = Path(output_filepath).resolve()

        with open(asm_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Pass 1: Parse labels
        executable_lines = self.pass_one(lines)

        # Pass 2: Translate instructions
        machine_code: List[str] = []
        has_error = False

        for line_num, instruction in executable_lines:
            try:
                if instruction.startswith("@"):
                    binary = self.translate_a_instruction(line_num, instruction)
                else:
                    binary = self.translate_c_instruction(line_num, instruction)
                machine_code.append(binary)
            except Exception as e:
                has_error = True
                # Feature 1: Print clean error message with line number
                if self.feature_code == 1:
                    print(f"Line {line_num}: invalid instruction ({e})")
                else:
                    print(f"Error at line {line_num} in '{instruction}': {e}")
                break

        if has_error:
            return False

        # Write output .hack file
        with open(out_path, "w", encoding="utf-8") as f:
            for code in machine_code:
                f.write(code + "\n")

        print(f"Assembly successful: '{asm_path.name}' -> '{out_path.name}' ({len(machine_code)} instructions)")

        # Feature 0: Save all labels and variables with addresses in symbols.txt
        # If feature_code == 0, save to symbols.txt in the same directory or project root
        if self.feature_code == 0 or self.feature_code is None:
            symbols_out_path = out_path.parent / "symbols.txt"
            self.export_symbols(str(symbols_out_path))

        return True

    def export_symbols(self, symbols_filepath: str):
        """Exports user-defined labels and variables to symbols.txt."""
        with open(symbols_filepath, "w", encoding="utf-8") as f:
            f.write("=== LABELS (ROM Addresses) ===\n")
            for label, addr in sorted(self.user_labels.items(), key=lambda x: x[1]):
                f.write(f"{label:24} : {addr}\n")

            f.write("\n=== VARIABLES (RAM Addresses) ===\n")
            for var, addr in sorted(self.user_variables.items(), key=lambda x: x[1]):
                f.write(f"{var:24} : {addr}\n")

            f.write("\n=== PREDEFINED SYMBOLS ===\n")
            for sym, addr in sorted(PREDEFINED_SYMBOLS.items(), key=lambda x: x[1]):
                f.write(f"{sym:24} : {addr}\n")
        print(f"Symbol table written to: '{symbols_filepath}'")


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <input.asm> [output.hack] [--feature <0|1|2>]")
        sys.exit(1)

    asm_file = sys.argv[1]
    out_file = None
    feature = None

    idx = 2
    while idx < len(sys.argv):
        arg = sys.argv[idx]
        if arg == "--feature" and idx + 1 < len(sys.argv):
            feature = int(sys.argv[idx + 1])
            idx += 2
        elif not arg.startswith("-") and out_file is None:
            out_file = arg
            idx += 1
        else:
            idx += 1

    assembler = HackAssembler(feature_code=feature)
    success = assembler.assemble(asm_file, out_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

