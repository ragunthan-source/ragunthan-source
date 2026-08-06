"""
render_heatmap_svg.py

Renders a production-ready, animated GitHub contribution graph SVG from
data/contributions.json with a modern monochrome Linux terminal aesthetic.

Features:
- Width ~900px
- 53 weeks x 7 days grid layout with rounded squares (rx="2")
- Official GitHub Green Palette (#161b22, #0e4429, #006d32, #26a641, #39d353)
- Diagonal slide-in reveal animation per square (runs once, no infinite loop)
- Integrated stats bar: Total Contributions, Current Streak, Longest Streak, Best Day
- Month labels (Jan..Dec) & Day labels (Mon, Wed, Fri)
- Less -> More color legend
- Terminal window container styling
"""

import os
import sys
import json
import argparse
from datetime import datetime, date


class HeatmapSvgRenderer:
    """Renders animated GitHub contribution heatmap SVG graphics."""

    COLOR_MAP = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353",
    }

    MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(
        self,
        json_path: str = "data/contributions.json",
        output_svg_path: str = "assets/contribution-graph.svg",
        bg_color: str = "#0d1117",
        font_family: str = "'Fira Code', 'JetBrains Mono', Consolas, monospace",
    ):
        self.json_path = json_path
        self.output_svg_path = output_svg_path
        self.bg_color = bg_color
        self.font_family = font_family

    def load_data(self) -> dict:
        """Load contribution data from JSON file."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Contributions JSON not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def render(self) -> str:
        """Generate animated heatmap SVG."""
        data = self.load_data()
        stats = data.get("stats", {})
        days = data.get("days", [])

        width = 900
        header_height = 35
        stats_height = 45
        grid_top = header_height + stats_height + 25
        padding_left = 45
        padding_bottom = 40
        
        square_size = 11.5
        square_gap = 3.5
        col_width = square_size + square_gap
        row_height = square_size + square_gap

        grid_height = 7 * row_height
        total_height = grid_top + grid_height + padding_bottom

        # Organize days into 53 weeks x 7 days
        # Group days by week index
        weeks = []
        current_week = []
        for idx, d in enumerate(days):
            current_week.append(d)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        if current_week:
            weeks.append(current_week)
        
        # Limit to last 53 weeks
        weeks = weeks[-53:]

        # Build Month Labels
        month_labels_svg = []
        last_month = -1
        for col_idx, week in enumerate(weeks):
            if not week:
                continue
            first_day_date = datetime.strptime(week[0]["date"], "%Y-%m-%d")
            m = first_day_date.month
            if m != last_month:
                x_pos = padding_left + col_idx * col_width
                month_name = self.MONTH_NAMES[m - 1]
                month_labels_svg.append(
                    f'    <text x="{x_pos:.1f}" y="{grid_top - 8}" class="axis-label">{month_name}</text>'
                )
                last_month = m

        # Day Labels (Mon, Wed, Fri)
        day_labels_svg = [
            f'    <text x="{padding_left - 10}" y="{grid_top + 1 * row_height + 9}" text-anchor="end" class="axis-label">Mon</text>',
            f'    <text x="{padding_left - 10}" y="{grid_top + 3 * row_height + 9}" text-anchor="end" class="axis-label">Wed</text>',
            f'    <text x="{padding_left - 10}" y="{grid_top + 5 * row_height + 9}" text-anchor="end" class="axis-label">Fri</text>',
        ]

        # Build Squares SVG with diagonal slide animation keyframes
        squares_svg = []
        total_weeks = len(weeks)

        for col_idx, week in enumerate(weeks):
            for row_idx, day_data in enumerate(week):
                x_pos = padding_left + col_idx * col_width
                y_pos = grid_top + row_idx * row_height
                level = day_data.get("level", 0)
                color = self.COLOR_MAP.get(level, self.COLOR_MAP[0])
                date_str = day_data.get("date", "")
                count = day_data.get("count", 0)

                # Diagonal animation delay formula
                delay = round(0.1 + (col_idx * 0.015) + (row_idx * 0.02), 3)

                squares_svg.append(
                    f'    <rect x="{x_pos:.1f}" y="{y_pos:.1f}" width="{square_size}" height="{square_size}" rx="2" '
                    f'fill="{color}" class="sq" style="animation-delay: {delay}s;">'
                    f'<title>{count} contributions on {date_str}</title></rect>'
                )

        # Legend SVG
        legend_x = width - 180
        legend_y = grid_top + grid_height + 20
        legend_squares = []
        for lvl, clr in self.COLOR_MAP.items():
            lx = legend_x + 35 + lvl * (square_size + 3)
            legend_squares.append(
                f'<rect x="{lx:.1f}" y="{legend_y - 10}" width="{square_size}" height="{square_size}" rx="2" fill="{clr}" />'
            )

        legend_svg = (
            f'  <g class="legend">\n'
            f'    <text x="{legend_x}" y="{legend_y}" class="legend-text">Less</text>\n'
            f'    {" ".join(legend_squares)}\n'
            f'    <text x="{legend_x + 35 + 5 * (square_size + 3) + 4}" y="{legend_y}" class="legend-text">More</text>\n'
            f'  </g>'
        )

        # Top Stats Bar SVG
        total_contribs = stats.get("total_contributions", 0)
        curr_streak = stats.get("current_streak", 0)
        long_streak = stats.get("longest_streak", 0)
        best_day_info = stats.get("best_day", {})
        best_count = best_day_info.get("count", 0)

        stats_y = header_height + 26
        stat_item_w = (width - padding_left * 2) / 4

        stats_bar_svg = f"""  <!-- Stats Bar -->
  <g class="stats-group">
    <g class="stat-box" style="animation-delay: 0.1s;">
      <text x="{padding_left}" y="{stats_y}" class="stat-value">{total_contribs:,}</text>
      <text x="{padding_left}" y="{stats_y + 14}" class="stat-label">Yearly Contributions</text>
    </g>
    <g class="stat-box" style="animation-delay: 0.2s;">
      <text x="{padding_left + stat_item_w}" y="{stats_y}" class="stat-value">{curr_streak} Days</text>
      <text x="{padding_left + stat_item_w}" y="{stats_y + 14}" class="stat-label">Current Streak</text>
    </g>
    <g class="stat-box" style="animation-delay: 0.3s;">
      <text x="{padding_left + stat_item_w * 2}" y="{stats_y}" class="stat-value">{long_streak} Days</text>
      <text x="{padding_left + stat_item_w * 2}" y="{stats_y + 14}" class="stat-label">Longest Streak</text>
    </g>
    <g class="stat-box" style="animation-delay: 0.4s;">
      <text x="{padding_left + stat_item_w * 3}" y="{stats_y}" class="stat-value">{best_count} Commits</text>
      <text x="{padding_left + stat_item_w * 3}" y="{stats_y + 14}" class="stat-label">Best Day</text>
    </g>
  </g>"""

        # Construct complete SVG
        svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_height}" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: {self.bg_color}; rx: 8px; }}
      .border {{ fill: none; stroke: #30363d; stroke-width: 1.5px; rx: 8px; }}
      .title-bar {{ fill: #161b22; }}
      .title-text {{ fill: #8b949e; font-family: {self.font_family}; font-size: 12px; font-weight: 600; }}
      .window-dot {{ r: 5px; }}

      .stat-value {{
        font-family: {self.font_family};
        font-size: 16px;
        font-weight: 700;
        fill: #39d353;
      }}
      .stat-label {{
        font-family: {self.font_family};
        font-size: 10.5px;
        fill: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }}
      .stat-box {{
        opacity: 0;
        animation: fadeIn 0.4s ease-out forwards;
      }}

      .axis-label {{
        font-family: {self.font_family};
        font-size: 10px;
        fill: #8b949e;
      }}

      .sq {{
        opacity: 0;
        animation: revealSquare 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }}

      .legend-text {{
        font-family: {self.font_family};
        font-size: 10px;
        fill: #8b949e;
      }}

      @keyframes revealSquare {{
        0% {{
          opacity: 0;
          transform: translate(-4px, -4px) scale(0.8);
        }}
        100% {{
          opacity: 1;
          transform: translate(0, 0) scale(1);
        }}
      }}

      @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(3px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
    </style>
  </defs>

  <!-- Terminal Window Base -->
  <rect width="{width}" height="{total_height}" class="bg" />
  
  <!-- Terminal Header Bar -->
  <path d="M 0,8 A 8,8 0 0 1 8,0 L {width-8},0 A 8,8 0 0 1 {width},8 L {width},{header_height} L 0,{header_height} Z" class="title-bar" />
  <circle cx="18" cy="18" class="window-dot" fill="#ff5f56" />
  <circle cx="34" cy="18" class="window-dot" fill="#ffbd2e" />
  <circle cx="50" cy="18" class="window-dot" fill="#27c93f" />
  <text x="{width // 2}" y="22" text-anchor="middle" class="title-text">ragunthan@github: ~/contributions-heatmap</text>

  <!-- Outer Border -->
  <rect width="{width}" height="{total_height}" class="border" />

{stats_bar_svg}

  <!-- Axis Labels -->
  <g>
{"\n".join(month_labels_svg)}
{"\n".join(day_labels_svg)}
  </g>

  <!-- Heatmap Grid -->
  <g>
{"\n".join(squares_svg)}
  </g>

  <!-- Legend -->
{legend_svg}
</svg>
"""
        output_dir = os.path.dirname(self.output_svg_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(self.output_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)

        print(f"[OK] Successfully rendered Heatmap SVG -> {self.output_svg_path}")
        return self.output_svg_path


def main():
    parser = argparse.ArgumentParser(description="Render animated contribution heatmap SVG.")
    parser.add_argument("--json", default="data/contributions.json", help="Path to contributions JSON")
    parser.add_argument("--output", default="assets/contribution-graph.svg", help="Output SVG path")
    args = parser.parse_args()

    renderer = HeatmapSvgRenderer(args.json, args.output)
    renderer.render()


if __name__ == "__main__":
    main()
