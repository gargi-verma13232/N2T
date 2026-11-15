"""
Student and Course Configuration Module for Nand to Tetris Capstone.
Contains roll number configuration, personal number K calculation,
and derived parameters for Part B (assembler) and Part C (box drawing).
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any

CONFIG_FILE = Path(__file__).resolve().parent / "student_config.json"

DEFAULT_CONFIG = {
    "student_name": "[PENDING_STUDENT_NAME]",
    "roll_number": None,  # Example: 2501010223 or last two digits
    "k_value": None,       # Last two digits of roll number
    "university": "K.R. Mangalam University",
    "school": "School of Engineering & Technology",
    "course_code": "ETCCNT301",
    "course_name": "Nand to Tetris - I",
    "project_title": "Make the Computer Draw a Box"
}

def load_config() -> Dict[str, Any]:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def set_roll_number(roll_number_str: str, student_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Sets the roll number and calculates K = last two digits of roll number.
    """
    config = load_config()
    clean_str = roll_number_str.strip()
    config["roll_number"] = clean_str
    if student_name:
        config["student_name"] = student_name.strip()
    
    # Calculate K as integer of last 2 digits
    digits = "".join(filter(str.isdigit, clean_str))
    if len(digits) >= 2:
        k = int(digits[-2:])
    elif len(digits) == 1:
        k = int(digits)
    else:
        raise ValueError("Invalid roll number. Must contain digits.")
    
    config["k_value"] = k
    save_config(config)
    return get_parameters(k)

def get_parameters(k: Optional[int] = None) -> Dict[str, Any]:
    """
    Computes box parameters and assembler feature based on K.
    """
    if k is None:
        config = load_config()
        k = config.get("k_value")
    
    if k is None:
        return {
            "is_configured": False,
            "k": None,
            "starting_row": None,
            "height": 20,
            "width_words": None,
            "width_pixels": None,
            "assembler_feature_code": None,
            "assembler_feature_description": "Awaiting student roll number / K value."
        }

    k_mod_4 = k % 4
    width_words = k_mod_4 + 1
    width_pixels = 16 * width_words
    starting_row = k
    height = 20

    k_mod_3 = k % 3
    if k_mod_3 == 0:
        feat_desc = "Save all labels and variables with their addresses in symbols.txt."
    elif k_mod_3 == 1:
        feat_desc = "For a wrong line, print a clear message with the line number (e.g. Line 7: invalid instruction) instead of crashing."
    else:
        feat_desc = "Print a warning if the same label is written twice."

    return {
        "is_configured": True,
        "k": k,
        "starting_row": starting_row,
        "height": height,
        "width_words": width_words,
        "width_pixels": width_pixels,
        "assembler_feature_code": k_mod_3,
        "assembler_feature_description": feat_desc
    }

if __name__ == "__main__":
    params = get_parameters()
    print("Current Configuration Status:")
    for key, value in params.items():
        print(f"  {key}: {value}")

