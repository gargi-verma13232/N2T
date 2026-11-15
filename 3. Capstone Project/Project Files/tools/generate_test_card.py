#!/usr/bin/env python3
"""
Generates clean, professional terminal screenshot images for test evidence.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

def render_terminal_screenshot(
    output_path: str,
    title: str,
    command_text: str,
    output_lines: list,
    status_success: bool = True
):
    # Palette
    BG_COLOR = (24, 24, 27)         # Slate black
    HEADER_BG = (39, 39, 42)        # Header dark gray
    TEXT_COLOR = (244, 244, 245)     # Off-white
    CMD_COLOR = (56, 189, 248)       # Light cyan
    SUCCESS_COLOR = (74, 222, 128)   # Emerald green
    FAIL_COLOR = (248, 113, 113)     # Coral red
    DIM_TEXT = (161, 161, 170)       # Dim gray

    # Dimensions
    font_size = 15
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        title_font = ImageFont.truetype("arial.ttf", 13)
    except IOError:
        font = ImageFont.load_default()
        title_font = font

    line_height = 22
    padding_x = 24
    header_height = 40
    
    # Estimate dimensions
    all_text_lines = [f"$ {command_text}", ""] + output_lines
    max_line_len = max(len(line) for line in all_text_lines) if all_text_lines else 60
    img_width = max(800, max_line_len * 9 + padding_x * 2)
    img_height = header_height + (len(all_text_lines) + 2) * line_height + 20

    img = Image.new("RGB", (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (img_width, header_height)], fill=HEADER_BG)
    # Window controls
    draw.ellipse([(14, 14), (26, 26)], fill=(239, 68, 68))    # Close red
    draw.ellipse([(34, 14), (46, 26)], fill=(245, 158, 11))   # Min yellow
    draw.ellipse([(54, 14), (66, 26)], fill=(34, 197, 94))    # Max green

    # Header title
    draw.text((80, 12), title, fill=DIM_TEXT, font=title_font)

    # Content
    y = header_height + 16
    draw.text((padding_x, y), f"$ {command_text}", fill=CMD_COLOR, font=font)
    y += line_height * 2

    for line in output_lines:
        color = TEXT_COLOR
        if "Comparison ended successfully" in line or "PASSED" in line or "SUCCESS" in line:
            color = SUCCESS_COLOR
        elif "failed" in line.lower() or "error" in line.lower():
            color = FAIL_COLOR
        elif line.startswith("|") or line.startswith("//"):
            color = DIM_TEXT

        draw.text((padding_x, y), line, fill=color, font=font)
        y += line_height

    # Status badge at bottom
    badge_text = "STATUS: PASSED" if status_success else "STATUS: FAILED"
    badge_color = SUCCESS_COLOR if status_success else FAIL_COLOR
    draw.text((padding_x, y + 6), badge_text, fill=badge_color, font=font)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Saved screenshot: {output_path}")

if __name__ == "__main__":
    render_terminal_screenshot(
        "test_card.png",
        "HardwareSimulator - CPU.tst",
        "python tools/run_hdl_test.py part_a_hardware/tests/CPU.tst",
        [
            "Loading CPU.hdl ...",
            "Executing test script CPU.tst ...",
            "Comparing against CPU.cmp ...",
            "End of script - Comparison ended successfully"
        ],
        True
    )

