"""
make_tech_stack_svg.py

Generates a hacker/terminal-themed Technical Skills SVG card (assets/tech-stack.svg)
displaying categorized technical skills with pure CSS sequential animations.
"""

import os
import sys
import argparse
import html


class TechStackSvgGenerator:
    """Generates an animated terminal SVG showcasing technical skills."""

    def __init__(
        self,
        output_svg_path: str = "assets/tech-stack.svg",
        bg_color: str = "#0d1117",
        font_family: str = "'Fira Code', 'JetBrains Mono', Consolas, monospace",
    ):
        self.output_svg_path = output_svg_path
        self.bg_color = bg_color
        self.font_family = font_family

    def get_skills_data(self) -> list[tuple[str, str]]:
        """Return categorized technical skills."""
        return [
            ("Programming", "Java, Python, C, JavaScript, Dart, SQL"),
            ("Frontend", "HTML5, CSS3, React JS, Flutter, Tailwind CSS"),
            ("Backend", "Node.js, Express.js, REST API, JWT"),
            ("Database", "MySQL, MongoDB"),
            ("DevOps & Tools", "Git, GitHub, Jenkins, Docker, Linux, Postman"),
            ("Cloud", "AWS (Basic)"),
            ("CS Core", "DSA, OOP, DBMS, OS, Networks, Web Security"),
        ]

    def build_svg(self) -> str:
        """Build animated SVG card for technical skills."""
        width = 460
        header_height = 35
        row_height = 42
        padding_x = 22
        padding_y = 16

        skills = self.get_skills_data()
        total_rows = len(skills)
        height = int(header_height + padding_y * 2 + total_rows * row_height + 40)

        svg_elements = []
        delay_step = 0.08
        current_delay = 0.1

        # 1. Shell prompt header line
        start_y = header_height + padding_y + 14
        svg_elements.append(
            f'    <text x="{padding_x}" y="{start_y}" class="prompt-line" style="animation-delay: {current_delay:.2f}s;">'
            f'<tspan class="prompt-user">ragunthan@github</tspan><tspan class="prompt-sep">:$</tspan> cat skills.json</text>'
        )
        current_delay += delay_step

        # 2. Divider line
        sep_y = start_y + 14
        svg_elements.append(
            f'    <text x="{padding_x}" y="{sep_y}" class="prompt-sep" style="animation-delay: {current_delay:.2f}s;">'
            f'-------------------------------------------------</text>'
        )
        current_delay += delay_step

        # 3. Categorized skills rows
        content_start_y = sep_y + 24
        for idx, (category, items) in enumerate(skills):
            y_pos = content_start_y + idx * row_height
            escaped_cat = html.escape(f"[{category}]")
            escaped_items = html.escape(items)

            row_svg = (
                f'    <g class="skill-row" style="animation-delay: {current_delay:.2f}s;">\n'
                f'      <text x="{padding_x}" y="{y_pos}" class="cat-text">{escaped_cat}</text>\n'
                f'      <text x="{padding_x}" y="{y_pos + 16}" class="item-text">{escaped_items}</text>\n'
                f'    </g>'
            )
            svg_elements.append(row_svg)
            current_delay += delay_step

        # 4. Terminal Cursor prompt at end
        end_y = content_start_y + total_rows * row_height + 6
        svg_elements.append(
            f'    <text x="{padding_x}" y="{end_y}" class="prompt-line" style="animation-delay: {current_delay:.2f}s;">'
            f'<tspan class="prompt-user">ragunthan@github</tspan><tspan class="prompt-sep">:$</tspan> <tspan class="cursor">█</tspan></text>'
        )

        svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: {self.bg_color}; rx: 8px; }}
      .border {{ fill: none; stroke: #30363d; stroke-width: 1.5px; rx: 8px; }}
      .title-bar {{ fill: #161b22; }}
      .title-text {{ fill: #8b949e; font-family: {self.font_family}; font-size: 12px; font-weight: 600; }}
      .window-dot {{ r: 5px; }}

      .prompt-line {{
        font-family: {self.font_family};
        font-size: 12.5px;
        opacity: 0;
        animation: fadeIn 0.3s ease-out forwards;
      }}
      .prompt-user {{ fill: #58a6ff; font-weight: 700; }}
      .prompt-sep {{ fill: #30363d; }}

      .skill-row {{
        opacity: 0;
        animation: fadeIn 0.35s ease-out forwards;
      }}

      .cat-text {{
        font-family: {self.font_family};
        font-size: 12px;
        font-weight: 700;
        fill: #39d353;
      }}

      .item-text {{
        font-family: {self.font_family};
        font-size: 11.5px;
        font-weight: 400;
        fill: #e6e6e6;
      }}

      .cursor {{
        fill: #58a6ff;
        animation: cursorBlink 0.8s infinite step-end;
      }}

      @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(3px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      @keyframes cursorBlink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Terminal Window Base -->
  <rect width="{width}" height="{height}" class="bg" />
  
  <!-- Terminal Header Bar -->
  <path d="M 0,8 A 8,8 0 0 1 8,0 L {width-8},0 A 8,8 0 0 1 {width},8 L {width},{header_height} L 0,{header_height} Z" class="title-bar" />
  <circle cx="18" cy="18" class="window-dot" fill="#ff5f56" />
  <circle cx="34" cy="18" class="window-dot" fill="#ffbd2e" />
  <circle cx="50" cy="18" class="window-dot" fill="#27c93f" />
  <text x="{width // 2}" y="22" text-anchor="middle" class="title-text">ragunthan@github: ~/tech-stack</text>

  <!-- Outer Border -->
  <rect width="{width}" height="{height}" class="border" />

  <!-- Skills Card Content -->
  <g>
{"\n".join(svg_elements)}
  </g>
</svg>
"""
        return svg_code

    def render(self) -> str:
        """Render Tech Stack SVG card to output path."""
        print(f"[+] Generating Tech Stack SVG card...")
        svg_code = self.build_svg()

        output_dir = os.path.dirname(self.output_svg_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(self.output_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)

        print(f"[OK] Successfully rendered Tech Stack SVG -> {self.output_svg_path}")
        return self.output_svg_path


def main():
    parser = argparse.ArgumentParser(description="Generate Tech Stack SVG info card.")
    parser.add_argument("--output", default="assets/tech-stack.svg", help="Output SVG path")
    args = parser.parse_args()

    generator = TechStackSvgGenerator(args.output)
    generator.render()


if __name__ == "__main__":
    main()
