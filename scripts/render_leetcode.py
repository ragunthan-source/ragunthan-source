import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
INPUT_FILE = os.path.join(DATA_DIR, "leetcode_stats.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
PRIMARY_OUTPUT = os.path.join(OUTPUT_DIR, "leetcode-dashboard.svg")

DEFAULT_STATS = {
    "username": "Ragunthan",
    "solvedTotal": 47,
    "easySolved": 15,
    "mediumSolved": 28,
    "hardSolved": 4,
    "totalQuestions": 3300,
    "easyTotal": 820,
    "mediumTotal": 1720,
    "hardTotal": 760,
    "acceptanceRate": 74.3,
    "ranking": 2980549,
    "contestRating": 1685,
    "topPercentage": 12.5
}

def generate_svg(stats):
    solved_total = stats.get("solvedTotal", 47)
    easy_solved = stats.get("easySolved", 15)
    medium_solved = stats.get("mediumSolved", 28)
    hard_solved = stats.get("hardSolved", 4)
    acceptance_rate = stats.get("acceptanceRate", 74.3)
    ranking = stats.get("ranking", 2980549)
    contest_rating = stats.get("contestRating", 1685)
    top_pct = stats.get("topPercentage", 12.5)

    easy_pct = min(100, max(5, int((easy_solved / 800) * 100))) if easy_solved > 0 else 5
    medium_pct = min(100, max(5, int((medium_solved / 1600) * 100))) if medium_solved > 0 else 5
    hard_pct = min(100, max(5, int((hard_solved / 700) * 100))) if hard_solved > 0 else 5

    # Donut chart calculations (Large & Clear)
    r = 46
    circumference = 2 * 3.14159265 * r  # ~289.03
    progress_ratio = max(0.05, min(1.0, solved_total / 100.0))
    dash_filled = circumference * progress_ratio
    dash_empty = circumference - dash_filled

    bar_w = 310
    easy_w = max(10, int(bar_w * (easy_pct / 100.0)))
    med_w = max(10, int(bar_w * (medium_pct / 100.0)))
    hard_w = max(10, int(bar_w * (hard_pct / 100.0)))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 205" width="100%" height="205" fill="none">
  <style>
    .panel-box {{ fill: #161b22; rx: 12px; stroke: #30363d; stroke-width: 1; }}
    .head-lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 700; fill: #8b949e; letter-spacing: 1.5px; text-transform: uppercase; }}
    .head-link {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 12px; fill: #38bdf8; }}
    .big-stat {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 36px; font-weight: 800; fill: #f0f6fc; }}
    .sub-stat {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; fill: #8b949e; letter-spacing: 1px; }}
    .meta-key {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 600; fill: #8b949e; }}
    .meta-val {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 17px; font-weight: 700; fill: #f0f6fc; }}
    .orange-val {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 18px; font-weight: 700; fill: #ffa116; }}
    .diff-lbl {{ font-family: sans-serif; font-size: 14px; font-weight: 700; }}
    .bar-bg {{ fill: #21262d; rx: 4px; }}
    .rating-num {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 38px; font-weight: 800; fill: #ffa116; }}
    .standing-val {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; font-weight: 700; fill: #38bdf8; }}
    .active-badge {{ font-family: sans-serif; font-size: 11px; font-weight: 600; fill: #3fb950; }}
  </style>

  <!-- Transparent Background Canvas (Blends seamlessly with GitHub) -->
  <rect x="0" y="0" width="850" height="205" fill="none" />

  <!-- Header Strip -->
  <g transform="translate(0, 20)">
    <path d="M11.235 0a1.145 1.145 0 0 0-.8.365L5.975 4.825a1.145 1.145 0 0 0-.007 1.61l.007.007 2.932 2.958a1.145 1.145 0 0 0 1.616 0 1.145 1.145 0 0 0 0-1.616L8.242 5.483l3.794-3.838a1.145 1.145 0 0 0-.8-1.645zm4.628 3.457a1.145 1.145 0 0 0-.807.342L6.85 12.08a1.145 1.145 0 0 0 0 1.617l2.933 2.958a1.145 1.145 0 0 0 1.617 0l8.203-8.283a1.145 1.145 0 0 0-.8-1.948z" fill="#ffa116" transform="translate(0, -3) scale(0.95)"/>
    <text x="24" y="10" class="head-lbl">PROBLEM SOLVING &amp; ALGORITHMIC PERFORMANCE</text>
    <text x="850" y="10" text-anchor="end" class="head-link">leetcode.com/u/Ragunthan →</text>
  </g>

  <line x1="0" y1="36" x2="850" y2="36" stroke="#21262d" stroke-width="1" />

  <!-- Panel 1: Donut Gauge & Solved Total -->
  <g transform="translate(0, 48)">
    <rect x="0" y="0" width="250" height="145" class="panel-box" />

    <!-- Donut Ring -->
    <g transform="translate(70, 72)">
      <circle cx="0" cy="0" r="{r}" stroke="#21262d" stroke-width="9" fill="none" />
      <circle cx="0" cy="0" r="{r}" stroke="#ffa116" stroke-width="9" stroke-linecap="round" fill="none"
              stroke-dasharray="{dash_filled:.1f} {dash_empty:.1f}" transform="rotate(-90)" />
      <text x="0" y="8" text-anchor="middle" class="big-stat">{solved_total}</text>
      <text x="0" y="26" text-anchor="middle" class="sub-stat">SOLVED</text>
    </g>

    <!-- Stat Highlights on Right -->
    <g transform="translate(148, 34)">
      <text x="0" y="0" class="meta-key">Acceptance</text>
      <text x="0" y="22" class="orange-val">{acceptance_rate}%</text>

      <text x="0" y="52" class="meta-key">Global Rank</text>
      <text x="0" y="74" class="meta-val">#{ranking:,}</text>
    </g>
  </g>

  <!-- Panel 2: Difficulty Breakdown -->
  <g transform="translate(265, 48)">
    <rect x="0" y="0" width="365" height="145" class="panel-box" />

    <!-- Easy Bar -->
    <g transform="translate(25, 28)">
      <text x="0" y="0" class="diff-lbl" fill="#2cbb5d">Easy</text>
      <text x="{bar_w}" y="0" text-anchor="end" class="meta-val">{easy_solved} <tspan fill="#8b949e" font-weight="500" font-size="12">/ 820</tspan></text>
      <rect x="0" y="8" width="{bar_w}" height="8" class="bar-bg" />
      <rect x="0" y="8" width="{easy_w}" height="8" fill="#2cbb5d" rx="4" />
    </g>

    <!-- Medium Bar -->
    <g transform="translate(25, 66)">
      <text x="0" y="0" class="diff-lbl" fill="#ffb800">Medium</text>
      <text x="{bar_w}" y="0" text-anchor="end" class="meta-val">{medium_solved} <tspan fill="#8b949e" font-weight="500" font-size="12">/ 1720</tspan></text>
      <rect x="0" y="8" width="{bar_w}" height="8" class="bar-bg" />
      <rect x="0" y="8" width="{med_w}" height="8" fill="#ffb800" rx="4" />
    </g>

    <!-- Hard Bar -->
    <g transform="translate(25, 104)">
      <text x="0" y="0" class="diff-lbl" fill="#ef4743">Hard</text>
      <text x="{bar_w}" y="0" text-anchor="end" class="meta-val">{hard_solved} <tspan fill="#8b949e" font-weight="500" font-size="12">/ 760</tspan></text>
      <rect x="0" y="8" width="{bar_w}" height="8" class="bar-bg" />
      <rect x="0" y="8" width="{hard_w}" height="8" fill="#ef4743" rx="4" />
    </g>
  </g>

  <!-- Panel 3: Contest Rating & Standing -->
  <g transform="translate(645, 48)">
    <rect x="0" y="0" width="205" height="145" class="panel-box" />

    <g transform="translate(22, 30)">
      <text x="0" y="0" class="meta-key">CONTEST RATING</text>
      <text x="0" y="34" class="rating-num">{contest_rating}</text>
    </g>

    <line x1="22" y1="78" x2="183" y2="78" stroke="#30363d" stroke-width="1" />

    <g transform="translate(22, 102)">
      <text x="0" y="0" class="meta-key">Standing:</text>
      <text x="56" y="0" class="standing-val">Top {top_pct}%</text>

      <circle cx="4" cy="20" r="3.5" fill="#3fb950" />
      <text x="14" y="24" class="active-badge">Active Contestant</text>
    </g>
  </g>
</svg>"""
    return svg

def main():
    if os.path.exists(INPUT_FILE):
        try:
            with open(INPUT_FILE, "r", encoding="utf-8") as f:
                stats = json.load(f)
        except Exception:
            stats = DEFAULT_STATS
    else:
        stats = DEFAULT_STATS

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    svg_content = generate_svg(stats)
    
    # Save to all target filenames for cache-busting & backward compatibility
    targets = [
        PRIMARY_OUTPUT,
        os.path.join(OUTPUT_DIR, "leetcode.svg"),
        os.path.join(OUTPUT_DIR, "leetcode-card.svg")
    ]
    
    for path in targets:
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
    
    print(f"LeetCode SVG cards generated successfully across {len(targets)} targets.")

if __name__ == "__main__":
    main()
