import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
INPUT_FILE = os.path.join(DATA_DIR, "leetcode_stats.json")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "leetcode-card.svg")

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
    "acceptanceRate": 68.4,
    "ranking": 2980549,
    "contestRating": 1685,
    "topPercentage": 12.5
}

def generate_svg(stats):
    solved_total = stats.get("solvedTotal", 47)
    easy_solved = stats.get("easySolved", 15)
    medium_solved = stats.get("mediumSolved", 28)
    hard_solved = stats.get("hardSolved", 4)
    acceptance_rate = stats.get("acceptanceRate", 68.4)
    ranking = stats.get("ranking", 2980549)
    contest_rating = stats.get("contestRating", 1685)
    top_pct = stats.get("topPercentage", 12.5)

    easy_pct = min(100, max(5, int((easy_solved / 800) * 100))) if easy_solved > 0 else 5
    medium_pct = min(100, max(5, int((medium_solved / 1600) * 100))) if medium_solved > 0 else 5
    hard_pct = min(100, max(5, int((hard_solved / 700) * 100))) if hard_solved > 0 else 5

    # Donut chart calculations
    r = 25
    circumference = 2 * 3.14159265 * r # ~157.08
    progress_ratio = max(0.05, min(1.0, solved_total / 100.0))
    dash_filled = circumference * progress_ratio
    dash_empty = circumference - dash_filled

    bar_w = 260
    easy_w = max(6, int(bar_w * (easy_pct / 100.0)))
    med_w = max(6, int(bar_w * (medium_pct / 100.0)))
    hard_w = max(6, int(bar_w * (hard_pct / 100.0)))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 128" width="100%" height="128" fill="none">
  <defs>
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060913"/>
      <stop offset="50%" stop-color="#0b1120"/>
      <stop offset="100%" stop-color="#060913"/>
    </linearGradient>
  </defs>

  <style>
    .card-border {{ fill: url(#card-bg); stroke: #1e293b; stroke-width: 1.2; rx: 14px; }}
    .head-lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 700; fill: #64748b; letter-spacing: 1.5px; text-transform: uppercase; }}
    .head-link {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 10px; fill: #38bdf8; }}
    .big-stat {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 20px; font-weight: 800; fill: #f8fafc; }}
    .sub-stat {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 8px; font-weight: 700; fill: #64748b; letter-spacing: 1px; }}
    .meta-key {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 500; fill: #64748b; }}
    .meta-val {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; fill: #f8fafc; }}
    .diff-lbl {{ font-family: sans-serif; font-size: 10px; font-weight: 700; }}
    .bar-bg {{ fill: #1e293b; rx: 2px; }}
  </style>

  <!-- Card Canvas -->
  <rect x="0" y="0" width="800" height="128" class="card-border" />

  <!-- Header Strip -->
  <g transform="translate(24, 18)">
    <path d="M10 0a1 1 0 0 0-.7.3L5.3 4.2a1 1 0 0 0 0 1.4l2.6 2.6a1 1 0 0 0 1.4 0 1 1 0 0 0 0-1.4L7.3 4.8l3.4-3.4a1 1 0 0 0-.7-1.4zm4.1 3a1 1 0 0 0-.7.3L6.1 10.6a1 1 0 0 0 0 1.4l2.6 2.6a1 1 0 0 0 1.4 0l7.3-7.3a1 1 0 0 0-.7-1.7z" fill="#ffa116" transform="translate(0, -2) scale(0.8)"/>
    <text x="18" y="8" class="head-lbl">PROBLEM SOLVING &amp; ALGORITHMIC METRICS</text>
    <text x="752" y="8" text-anchor="end" class="head-link">leetcode.com/u/Ragunthan</text>
  </g>

  <line x1="24" y1="26" x2="776" y2="26" stroke="#1e293b" stroke-width="1" />

  <!-- Section 1: Total Solved Gauge -->
  <g transform="translate(30, 36)">
    <!-- Donut Ring -->
    <g transform="translate(42, 38)">
      <circle cx="0" cy="0" r="{r}" stroke="#1e293b" stroke-width="5" fill="none" />
      <circle cx="0" cy="0" r="{r}" stroke="#ffa116" stroke-width="5" stroke-linecap="round" fill="none"
              stroke-dasharray="{dash_filled:.1f} {dash_empty:.1f}" transform="rotate(-90)" />
      <text x="0" y="4" text-anchor="middle" class="big-stat">{solved_total}</text>
      <text x="0" y="14" text-anchor="middle" class="sub-stat">SOLVED</text>
    </g>

    <!-- Acceptance & Rank -->
    <g transform="translate(98, 22)">
      <text x="0" y="0" class="meta-key">Acceptance</text>
      <text x="0" y="14" class="meta-val" fill="#ffa116">{acceptance_rate}%</text>

      <text x="0" y="32" class="meta-key">Global Rank</text>
      <text x="0" y="46" class="meta-val">#{ranking:,}</text>
    </g>
  </g>

  <!-- Section 2: Difficulty Bars -->
  <g transform="translate(250, 42)">
    <!-- Easy -->
    <g transform="translate(0, 8)">
      <text x="0" y="0" class="diff-lbl" fill="#2cbb5d">Easy</text>
      <text x="290" y="0" text-anchor="end" class="meta-val">{easy_solved} <tspan fill="#64748b" font-weight="500">/ 820</tspan></text>
      <rect x="0" y="5" width="290" height="4" class="bar-bg" />
      <rect x="0" y="5" width="{easy_w * 290 // bar_w}" height="4" fill="#2cbb5d" rx="2" />
    </g>

    <!-- Medium -->
    <g transform="translate(0, 28)">
      <text x="0" y="0" class="diff-lbl" fill="#ffb800">Medium</text>
      <text x="290" y="0" text-anchor="end" class="meta-val">{medium_solved} <tspan fill="#64748b" font-weight="500">/ 1720</tspan></text>
      <rect x="0" y="5" width="290" height="4" class="bar-bg" />
      <rect x="0" y="5" width="{med_w * 290 // bar_w}" height="4" fill="#ffb800" rx="2" />
    </g>

    <!-- Hard -->
    <g transform="translate(0, 48)">
      <text x="0" y="0" class="diff-lbl" fill="#ef4743">Hard</text>
      <text x="290" y="0" text-anchor="end" class="meta-val">{hard_solved} <tspan fill="#64748b" font-weight="500">/ 760</tspan></text>
      <rect x="0" y="5" width="290" height="4" class="bar-bg" />
      <rect x="0" y="5" width="{hard_w * 290 // bar_w}" height="4" fill="#ef4743" rx="2" />
    </g>
  </g>

  <!-- Section 3: Contest Rating & Standing -->
  <g transform="translate(600, 48)">
    <g transform="translate(0, 0)">
      <text x="0" y="0" class="meta-key">CONTEST RATING</text>
      <text x="0" y="20" class="big-stat" fill="#ffa116">{contest_rating}</text>
    </g>

    <line x1="0" y1="36" x2="160" y2="36" stroke="#1e293b" stroke-width="1" />

    <g transform="translate(0, 52)">
      <text x="0" y="0" class="meta-key">PERCENTILE</text>
      <text x="75" y="0" class="meta-val" fill="#38bdf8">Top {top_pct}%</text>
      <circle cx="140" cy="-3" r="3" fill="#34d399" />
      <text x="148" y="0" font-family="sans-serif" font-size="9" font-weight="700" fill="#34d399">ACTIVE</text>
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

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    svg_content = generate_svg(stats)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    # Also write to leetcode.svg for cache busting
    alt_output = os.path.join(os.path.dirname(OUTPUT_FILE), "leetcode.svg")
    with open(alt_output, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"LeetCode SVG cards generated successfully at {OUTPUT_FILE} and {alt_output}")

if __name__ == "__main__":
    main()
