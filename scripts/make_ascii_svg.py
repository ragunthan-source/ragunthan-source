"""
make_ascii_svg.py

Converts a preprocessed photo into a 100 x 55 ASCII character grid and renders
it into an animated SVG vector graphic with monochrome terminal styling.

Features:
- Density ramp: " .`:-=+*cs#%@"
- 100 columns x 55 rows grid size
- Monochrome light-gray terminal text on black (#0d1117)
- SVG-native pure CSS self-typing animation (row by row reveal)
- Terminal block cursor animation
- One-time animation (no infinite loop)
"""

import os
import sys
import argparse
import html
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from PIL import Image


class AsciiSvgGenerator:
    """Converts images to monochrome ASCII art embedded in SVG with typing animations."""

    DENSITY_RAMP = " .`:-=+*cs#%@"

    def __init__(
        self,
        image_path: str,
        output_svg_path: str,
        cols: int = 100,
        rows: int = 55,
        bg_color: str = "#0d1117",
        text_color: str = "#c9d1d9",
        font_family: str = "'Fira Code', 'JetBrains Mono', Consolas, monospace",
    ):
        self.image_path = image_path
        self.output_svg_path = output_svg_path
        self.cols = cols
        self.rows = rows
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_family = font_family

    def _pixel_to_char(self, pixel_value: int) -> str:
        """Map 0-255 pixel intensity to ASCII density ramp character."""
        # 255 is white (lightest) -> space or '.'
        # 0 is black (darkest) -> dense char '@' or '%'
        scale = (len(self.DENSITY_RAMP) - 1) / 255.0
        # Invert intensity so dark areas produce dense characters
        inverted_val = 255 - pixel_value
        index = int(inverted_val * scale)
        index = max(0, min(len(self.DENSITY_RAMP) - 1, index))
        return self.DENSITY_RAMP[index]

    def generate_ascii_grid(self) -> list[str]:
        """Load image, resize to cols x rows, and map to ASCII lines."""
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Input prepped image not found: {self.image_path}")

        img = Image.open(self.image_path).convert("L")
        # Resize image to exact ASCII grid dimensions
        img_resized = img.resize((self.cols, self.rows), Image.Resampling.LANCZOS)
        np_img = np.array(img_resized)

        ascii_lines = []
        for r in range(self.rows):
            line_chars = [self._pixel_to_char(np_img[r, c]) for c in range(self.cols)]
            ascii_lines.append("".join(line_chars))

        return ascii_lines

    def build_svg(self, ascii_lines: list[str]) -> str:
        """Build animated monochrome SVG containing the ASCII grid."""
        # Font measurements for viewBox calculation
        char_width = 7.2
        line_height = 10.5
        padding_x = 20
        padding_y = 25
        header_height = 35

        width = int(self.cols * char_width + padding_x * 2)
        height = int(self.rows * line_height + padding_y * 2 + header_height)

        # Build line elements and CSS keyframe delays
        svg_lines = []
        total_lines = len(ascii_lines)
        step_delay = 0.035  # seconds per row
        start_delay = 0.2

        for idx, raw_line in enumerate(ascii_lines):
            escaped_line = html.escape(raw_line)
            y_pos = int(padding_y + header_height + idx * line_height)
            delay = round(start_delay + idx * step_delay, 3)
            svg_lines.append(
                f'    <text x="{padding_x}" y="{y_pos}" class="ascii-row row-{idx}" '
                f'style="animation-delay: {delay}s;">{escaped_line}</text>'
            )

        cursor_delay = round(start_delay + total_lines * step_delay + 0.1, 3)
        cursor_y = int(padding_y + header_height + (total_lines - 1) * line_height)

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: {self.bg_color}; rx: 8px; }}
      .border {{ fill: none; stroke: #30363d; stroke-width: 1.5px; rx: 8px; }}
      .title-bar {{ fill: #161b22; }}
      .title-text {{ fill: #8b949e; font-family: {self.font_family}; font-size: 12px; font-weight: 600; }}
      .window-dot {{ r: 5px; }}
      
      .ascii-text {{
        font-family: {self.font_family};
        font-size: 8.8px;
        fill: {self.text_color};
        white-space: pre;
        letter-spacing: 0px;
      }}
      
      .ascii-row {{
        opacity: 0;
        animation: typeRow 0.04s ease-out forwards;
      }}
      
      .cursor {{
        fill: #58a6ff;
        opacity: 0;
        animation: cursorBlink 0.8s infinite step-end {cursor_delay}s, cursorFade 0.01s forwards {cursor_delay}s;
      }}
      
      @keyframes typeRow {{
        0% {{ opacity: 0; transform: translateY(1px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      @keyframes cursorFade {{
        to {{ opacity: 1; }}
      }}

      @keyframes cursorBlink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Terminal Window Container -->
  <rect width="{width}" height="{height}" class="bg" />
  
  <!-- Terminal Header Bar -->
  <path d="M 0,8 A 8,8 0 0 1 8,0 L {width-8},0 A 8,8 0 0 1 {width},8 L {width},{header_height} L 0,{header_height} Z" class="title-bar" />
  <circle cx="18" cy="18" class="window-dot" fill="#ff5f56" />
  <circle cx="34" cy="18" class="window-dot" fill="#ffbd2e" />
  <circle cx="50" cy="18" class="window-dot" fill="#27c93f" />
  <text x="{width // 2}" y="22" text-anchor="middle" class="title-text">ragunthan@github: ~/ascii-portrait</text>

  <!-- Terminal Border -->
  <rect width="{width}" height="{height}" class="border" />

  <!-- Animated ASCII Content -->
  <g class="ascii-text">
{"\n".join(svg_lines)}
    <rect x="{width - padding_x - 12}" y="{cursor_y - 8}" width="7" height="10" class="cursor" />
  </g>
</svg>
"""
        return svg_content

    def render(self) -> str:
        """Execute complete ASCII grid generation and SVG rendering."""
        print(f"[+] Converting {self.image_path} to {self.cols}x{self.rows} ASCII grid...")
        ascii_lines = self.generate_ascii_grid()
        svg_code = self.build_svg(ascii_lines)

        output_dir = os.path.dirname(self.output_svg_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(self.output_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)

        print(f"[OK] Successfully rendered ASCII SVG -> {self.output_svg_path}")
        return self.output_svg_path


def main():
    parser = argparse.ArgumentParser(description="Generate animated SVG ASCII art from prepped image.")
    parser.add_argument("--input", default="data/source-prepped.png", help="Path to prepped image")
    parser.add_argument("--output", default="assets/ascii-profile.svg", help="Output SVG path")
    parser.add_argument("--cols", type=int, default=100, help="ASCII grid columns (default 100)")
    parser.add_argument("--rows", type=int, default=55, help="ASCII grid rows (default 55)")
    args = parser.parse_args()

    generator = AsciiSvgGenerator(args.input, args.output, cols=args.cols, rows=args.rows)
    generator.render()


if __name__ == "__main__":
    main()
