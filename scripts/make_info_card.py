"""
make_info_card.py

Generates a Neofetch-style Information Card SVG with a modern hacker terminal theme.
Features sequential fade-in animations for each system info row.
"""

import os
import sys
import argparse
import html


class InfoCardSvgGenerator:
    """Generates an animated Neofetch-style terminal SVG card."""

    def __init__(
        self,
        output_svg_path: str = "assets/info-card.svg",
        bg_color: str = "#0d1117",
        font_family: str = "'Fira Code', 'JetBrains Mono', Consolas, monospace",
    ):
        self.output_svg_path = output_svg_path
        self.bg_color = bg_color
        self.font_family = font_family

    def get_info_data(self) -> list[tuple[str, str]]:
        """Return the Neofetch metadata rows."""
        return [
            ("Name", "Ragunthan P R"),
            ("Role", "Computer Science Engineering Student"),
            ("Focus", "AI, Cloud, DevOps, Full Stack, Cyber Security"),
            ("Languages", "Python, Java, C, JavaScript, SQL"),
            ("Frameworks", "React, Node.js, Express, Tailwind CSS"),
            ("Tools", "Git, GitHub, Docker, Linux, VS Code"),
            ("Current Project", "AI Powered GitHub Automation"),
            ("Learning", "AWS, Kubernetes, CI/CD, Machine Learning"),
        ]

    def build_svg(self) -> str:
        """Build the animated SVG content."""
        width = 460
        header_height = 35
        row_height = 24
        padding_x = 24
        padding_y = 20

        info_rows = self.get_info_data()
        
        # ASCII Logo for Neofetch left side
        os_logo = [
            "       .-.      ",
            "      (   )     ",
            "       '-'      ",
            "   /\\       /\\  ",
            "  /  \\     /  \\ ",
            " / /\\ \\   / /\\ \\",
            " \\/  \\/   \\/  \\/",
        ]

        total_content_rows = max(len(os_logo) + 4, len(info_rows) + 3)
        height = int(header_height + padding_y * 2 + total_content_rows * row_height)

        # Generate SVG Elements with CSS Sequential Animations
        svg_elements = []
        delay_step = 0.1
        current_delay = 0.1

        # 1. OS Header / User Host line
        start_y = header_height + padding_y + 15
        svg_elements.append(
            f'    <text x="{padding_x}" y="{start_y}" class="prompt-user" style="animation-delay: {current_delay:.2f}s;">'
            f'ragunthan<tspan class="prompt-at">@</tspan>github</text>'
        )
        current_delay += delay_step

        # 2. Separator line
        sep_y = start_y + 16
        svg_elements.append(
            f'    <text x="{padding_x}" y="{sep_y}" class="prompt-sep" style="animation-delay: {current_delay:.2f}s;">'
            f'-------------------------------------------------</text>'
        )
        current_delay += delay_step

        # 3. Key-Value Rows
        content_start_y = sep_y + 26
        for idx, (key, value) in enumerate(info_rows):
            y_pos = content_start_y + idx * row_height
            escaped_key = html.escape(key)
            escaped_val = html.escape(value)

            row_svg = (
                f'    <g class="info-row" style="animation-delay: {current_delay:.2f}s;">\n'
                f'      <text x="{padding_x}" y="{y_pos}" class="key-text">{escaped_key}:</text>\n'
                f'      <text x="{padding_x + 130}" y="{y_pos}" class="val-text">{escaped_val}</text>\n'
                f'    </g>'
            )
            svg_elements.append(row_svg)
            current_delay += delay_step

        # 4. Terminal Color Blocks (Classic Neofetch palette bar)
        palette_y = content_start_y + len(info_rows) * row_height + 12
        palette_colors = ["#161b22", "#30363d", "#6e7681", "#8b949e", "#c9d1d9", "#f0f6fc", "#58a6ff", "#39d353"]
        palette_rects = []
        for i, color in enumerate(palette_colors):
            x_pos = padding_x + i * 22
            palette_rects.append(f'<rect x="{x_pos}" y="{palette_y}" width="18" height="12" rx="2" fill="{color}" />')

        svg_elements.append(
            f'    <g class="info-row" style="animation-delay: {current_delay:.2f}s;">\n'
            f'      {" ".join(palette_rects)}\n'
            f'    </g>'
        )

        svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: {self.bg_color}; rx: 8px; }}
      .border {{ fill: none; stroke: #30363d; stroke-width: 1.5px; rx: 8px; }}
      .title-bar {{ fill: #161b22; }}
      .title-text {{ fill: #8b949e; font-family: {self.font_family}; font-size: 12px; font-weight: 600; }}
      .window-dot {{ r: 5px; }}

      .prompt-user {{
        font-family: {self.font_family};
        font-size: 14px;
        font-weight: 700;
        fill: #58a6ff;
        opacity: 0;
        animation: fadeIn 0.3s ease-out forwards;
      }}
      .prompt-at {{ fill: #8b949e; }}
      .prompt-sep {{
        font-family: {self.font_family};
        font-size: 12px;
        fill: #30363d;
        opacity: 0;
        animation: fadeIn 0.3s ease-out forwards;
      }}
      
      .info-row {{
        opacity: 0;
        animation: fadeIn 0.35s ease-out forwards;
      }}

      .key-text {{
        font-family: {self.font_family};
        font-size: 12.5px;
        font-weight: 600;
        fill: #8b949e;
      }}

      .val-text {{
        font-family: {self.font_family};
        font-size: 12.5px;
        font-weight: 400;
        fill: #e6e6e6;
      }}

      @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(3px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
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
  <text x="{width // 2}" y="22" text-anchor="middle" class="title-text">ragunthan@github: ~/neofetch</text>

  <!-- Terminal Border -->
  <rect width="{width}" height="{height}" class="border" />

  <!-- Info Card Content -->
  <g>
{"\n".join(svg_elements)}
  </g>
</svg>
"""
        return svg_code

    def render(self) -> str:
        """Render Neofetch SVG card to output path."""
        print(f"[+] Generating Neofetch SVG card...")
        svg_code = self.build_svg()

        output_dir = os.path.dirname(self.output_svg_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(self.output_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)

        print(f"[OK] Successfully rendered Info Card SVG -> {self.output_svg_path}")
        return self.output_svg_path


def main():
    parser = argparse.ArgumentParser(description="Generate Neofetch SVG info card.")
    parser.add_argument("--output", default="assets/info-card.svg", help="Output SVG path")
    args = parser.parse_args()

    generator = InfoCardSvgGenerator(args.output)
    generator.render()


if __name__ == "__main__":
    main()
