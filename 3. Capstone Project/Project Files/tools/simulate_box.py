#!/usr/bin/env python3
"""
Accurate Hack Computer Simulator and Screen Renderer.
Executes Box.hack to verify:
1. When KBD != 0 (key pressed): Box is rendered black (-1) from row 23 to 42, width 64 pixels (4 words).
2. When KBD == 0 (key released): Box is completely cleared (0).
3. Generates high-fidelity visual screenshots of the Hack 512x256 display buffer.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class HackSimulator:
    def __init__(self, hack_file: str):
        with open(hack_file, "r") as f:
            self.rom = [int(line.strip(), 2) for line in f if line.strip()]
        self.ram = [0] * 32768
        self.d = 0
        self.a = 0
        self.pc = 0

    def step(self):
        if self.pc >= len(self.rom):
            return False

        instr = self.rom[self.pc]

        # A-instruction
        if (instr & 0x8000) == 0:
            self.a = instr & 0x7FFF
            self.pc += 1
            return True

        # C-instruction: 111 a c1..c6 d1..d3 j1..j3
        a_bit = (instr >> 12) & 1
        c_bits = (instr >> 6) & 0x3F
        d_bits = (instr >> 3) & 7
        j_bits = instr & 7

        x = self.d
        y = self.ram[self.a] if a_bit else self.a

        # ALU computation
        zx = (c_bits >> 5) & 1
        nx = (c_bits >> 4) & 1
        zy = (c_bits >> 3) & 1
        ny = (c_bits >> 2) & 1
        f  = (c_bits >> 1) & 1
        no = c_bits & 1

        if zx: x = 0
        if nx: x = (~x) & 0xFFFF
        if zy: y = 0
        if ny: y = (~y) & 0xFFFF

        out = (x + y) & 0xFFFF if f else (x & y) & 0xFFFF
        if no: out = (~out) & 0xFFFF

        # Convert to signed 16-bit for condition flags
        signed_out = out if out < 0x8000 else out - 0x10000
        zr = 1 if signed_out == 0 else 0
        ng = 1 if signed_out < 0 else 0
        pos = 1 if signed_out > 0 else 0

        # Destination routing
        if d_bits & 1:  # d3 -> M
            if 0 <= self.a < 24576:
                self.ram[self.a] = signed_out
        if d_bits & 2:  # d2 -> D
            self.d = signed_out
        if d_bits & 4:  # d1 -> A
            self.a = out & 0x7FFF

        # Jump condition
        j1 = (j_bits >> 2) & 1
        j2 = (j_bits >> 1) & 1
        j3 = j_bits & 1

        jump = (j1 and ng) or (j2 and zr) or (j3 and pos)

        if jump:
            self.pc = self.a
        else:
            self.pc += 1

        return True

    def run_cycles(self, cycles: int):
        for _ in range(cycles):
            self.step()

    def set_keyboard(self, key_code: int):
        self.ram[24576] = key_code

    def render_screen(self, output_path: str, caption: str, show_zoom: bool = False):
        """
        Renders the 512x256 Hack screen memory (16384..24575).
        Each 16-bit word represents 16 pixels.
        Bit 0 is the leftmost pixel of the word, Bit 15 is the rightmost.
        Value -1 (all 1s) means 16 black pixels.
        Value 0 means 16 white pixels.
        """
        screen_img = Image.new("1", (512, 256), 1)  # 1 = white background
        pixels = screen_img.load()

        for row in range(256):
            for col_word in range(32):
                addr = 16384 + (row * 32) + col_word
                word_val = self.ram[addr] & 0xFFFF
                for bit in range(16):
                    # Bit 0 is leftmost pixel
                    pixel_on = (word_val >> bit) & 1
                    # 1 = black pixel (0 in PIL "1" mode), 0 = white pixel (1 in PIL)
                    pixels[col_word * 16 + bit, row] = 0 if pixel_on else 1

        # Scale up to crisp high-res display with bezel and frame
        scale = 2
        scaled_w = 512 * scale
        scaled_h = 256 * scale
        resized_screen = screen_img.resize((scaled_w, scaled_h), Image.NEAREST).convert("RGB")

        # Create canvas with emulator window frame
        bezel = 24
        header_h = 50
        footer_h = 40
        canvas_w = scaled_w + bezel * 2
        canvas_h = scaled_h + header_h + bezel + footer_h

        canvas = Image.new("RGB", (canvas_w, canvas_h), (30, 41, 59))  # Slate frame
        draw = ImageDraw.Draw(canvas)

        # Header bar
        draw.rectangle([(0, 0), (canvas_w, header_h)], fill=(15, 23, 42))
        # Window buttons
        draw.ellipse([(14, 18), (26, 30)], fill=(239, 68, 68))
        draw.ellipse([(34, 18), (46, 30)], fill=(245, 158, 11))
        draw.ellipse([(54, 18), (66, 30)], fill=(34, 197, 94))

        # Title
        try:
            title_font = ImageFont.truetype("arial.ttf", 16)
            font = ImageFont.truetype("consola.ttf", 14)
        except IOError:
            title_font = ImageFont.load_default()
            font = title_font

        draw.text((80, 16), "Nand to Tetris - Hack Screen Simulator (512 x 256)", fill=(241, 245, 249), font=title_font)

        # Paste screen
        screen_x = bezel
        screen_y = header_h + 12
        # Draw border around screen
        draw.rectangle([(screen_x - 2, screen_y - 2), (screen_x + scaled_w + 1, screen_y + scaled_h + 1)], outline=(71, 85, 105), width=2)
        canvas.paste(resized_screen, (screen_x, screen_y))

        # Footer caption
        draw.text((bezel, screen_y + scaled_h + 12), caption, fill=(56, 189, 248), font=font)

        canvas.save(output_path, "PNG")
        print(f"Saved Hack screen screenshot: {output_path}")

def main():
    hack_path = PROJECT_ROOT / "part_c_box_program" / "Box.hack"
    screenshots_dir = PROJECT_ROOT / "part_c_box_program" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    sim = HackSimulator(str(hack_path))

    # Test 1: Key Pressed (e.g. key 'K' = ASCII 75)
    print("Testing Key Pressed behavior (KBD = 75)...")
    sim.set_keyboard(75)
    sim.run_cycles(3000)

    # Validate memory state for K=23:
    # Starting row: 23, Height: 20 rows (23..42), Width: 4 words (64 pixels)
    # Check that rows 23..42, words 0..3 are -1 (0xFFFF)
    all_black = True
    for r in range(23, 43):
        for w in range(4):
            addr = 16384 + (r * 32) + w
            val = sim.ram[addr]
            if val != -1:
                all_black = False
                print(f"Error: RAM[{addr}] at row {r}, col {w} expected -1 but got {val}")

    if all_black:
        print("VERIFIED: Box is completely black (64x20 pixels at row 23) when key is pressed!")

    # Render key pressed screenshot
    sim.render_screen(
        str(screenshots_dir / "Box_screen_key_pressed.png"),
        "EVENT: Key Pressed (KBD = 75) -> Black Box displayed (Row 23..42, Width 64 px [4 words], Height 20 px)"
    )

    # Test 2: Key Released (KBD = 0)
    print("\nTesting Key Released behavior (KBD = 0)...")
    sim.set_keyboard(0)
    sim.run_cycles(3000)

    # Validate memory state: all box words should now be 0
    all_white = True
    for r in range(23, 43):
        for w in range(4):
            addr = 16384 + (r * 32) + w
            val = sim.ram[addr]
            if val != 0:
                all_white = False
                print(f"Error: RAM[{addr}] at row {r}, col {w} expected 0 but got {val}")

    if all_white:
        print("VERIFIED: Box is completely cleared (all 0s) when key is released!")

    # Render key released screenshot
    sim.render_screen(
        str(screenshots_dir / "Box_screen_key_released.png"),
        "EVENT: Key Released (KBD = 0) -> Box cleared, Screen is 100% white"
    )

if __name__ == "__main__":
    main()
