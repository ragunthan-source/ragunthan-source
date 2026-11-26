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

    easy_pct = min(100, max(6, int((easy_solved / 800) * 100))) if easy_solved > 0 else 6
    medium_pct = min(100, max(6, int((medium_solved / 1600) * 100))) if medium_solved > 0 else 6
    hard_pct = min(100, max(6, int((hard_solved / 700) * 100))) if hard_solved > 0 else 6

    # Donut chart calculations
    r = 27
    circumference = 2 * 3.14159265 * r # ~169.64
    progress_ratio = max(0.05, min(1.0, solved_total / 100.0))
    dash_filled = circumference * progress_ratio
    dash_empty = circumference - dash_filled

    bar_w = 260
    easy_w = max(6, int(bar_w * (easy_pct / 100.0)))
    med_w = max(6, int(bar_w * (medium_pct / 100.0)))
    hard_w = max(6, int(bar_w * (hard_pct / 100.0)))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 135" width="100%" height="135" fill="none">
  <defs>
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0d14"/>
      <stop offset="100%" stop-color="#141923"/>
    </linearGradient>
  </defs>

  <style>
    .bg {{ fill: url(#card-bg); rx: 12px; stroke: #262f3f; stroke-width: 1.2; }}
    .panel {{ fill: #0f172a; rx: 8px; stroke: #1e293b; stroke-width: 1; }}
    .head-title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; fill: #cbd5e1; letter-spacing: 1.2px; text-transform: uppercase; }}
    .head-sub {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 10px; fill: #64748b; }}
    .stat-num {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 18px; font-weight: 800; fill: #f8fafc; }}
    .sub-num {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 9px; font-weight: 600; fill: #94a3b8; }}
    .meta-lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 600; fill: #64748b; }}
    .meta-val {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; fill: #f8fafc; }}
    .easy-clr {{ fill: #2cbb5d; font-family: sans-serif; font-size: 10px; font-weight: 700; }}
    .med-clr {{ fill: #ffb800; font-family: sans-serif; font-size: 10px; font-weight: 700; }}
    .hard-clr {{ fill: #ef4743; font-family: sans-serif; font-size: 10px; font-weight: 700; }}
    .orange-val {{ fill: #ffa116; font-family: sans-serif; font-size: 11px; font-weight: 700; }}
    .bar-track {{ fill: #1e293b; rx: 3px; }}
  </style>

  <!-- Container Box -->
  <rect x="0" y="0" width="850" height="135" class="bg" />

  <!-- Header Strip -->
  <g transform="translate(24, 18)">
    <path d="M11.235 0a1.145 1.145 0 0 0-.8.365L5.975 4.825a1.145 1.145 0 0 0-.007 1.61l.007.007 2.932 2.958a1.145 1.145 0 0 0 1.616 0 1.145 1.145 0 0 0 0-1.616L8.242 5.483l3.794-3.838a1.145 1.145 0 0 0-.8-1.645zm4.628 3.457a1.145 1.145 0 0 0-.807.342L6.85 12.08a1.145 1.145 0 0 0 0 1.617l2.933 2.958a1.145 1.145 0 0 0 1.617 0l8.203-8.283a1.145 1.145 0 0 0-.8-1.948z" fill="#ffa116" transform="translate(0, -2) scale(0.75)"/>
    <text x="20" y="10" class="head-title">PROBLEM SOLVING &amp; ALGORITHMIC METRICS</text>
    <text x="802" y="10" text-anchor="end" class="head-sub">LEETCODE VERIFIED STATS</text>
  </g>

  <line x1="24" y1="28" x2="826" y2="28" stroke="#1e293b" stroke-width="1" />

  <!-- Column 1: Solved Count & Circular Gauge -->
  <g transform="translate(24, 38)">
    <rect x="0" y="0" width="220" height="84" class="panel" />
    
    <!-- Mini Donut -->
    <g transform="translate(48, 42)">
      <circle cx="0" cy="0" r="{r}" stroke="#1e293b" stroke-width="6" fill="none" />
      <circle cx="0" cy="0" r="{r}" stroke="#ffa116" stroke-width="6" stroke-linecap="round" fill="none"
              stroke-dasharray="{dash_filled:.1f} {dash_empty:.1f}" transform="rotate(-90)" />
      <text x="0" y="4" text-anchor="middle" class="stat-num">{solved_total}</text>
      <text x="0" y="15" text-anchor="middle" class="sub-num">SOLVED</text>
    </g>

    <g transform="translate(106, 26)">
      <text x="0" y="0" class="meta-lbl">Acceptance</text>
      <text x="0" y="14" class="orange-val">{acceptance_rate}%</text>

      <text x="0" y="34" class="meta-lbl">Global Rank</text>
      <text x="0" y="48" class="meta-val">#{ranking:,}</text>
    </g>
  </g>

  <!-- Column 2: Difficulty Breakdown Bars -->
  <g transform="translate(256, 38)">
    <rect x="0" y="0" width="370" height="84" class="panel" />

    <!-- Easy Bar -->
    <g transform="translate(18, 16)">
      <text x="0" y="0" class="easy-clr">EASY</text>
      <text x="334" y="0" text-anchor="end" class="meta-val">{easy_solved} <tspan fill="#64748b" font-weight="500">/ 820</tspan></text>
      <rect x="0" y="6" width="334" height="6" class="bar-track" />
      <rect x="0" y="6" width="{easy_w * 334 // bar_w}" height="6" fill="#2cbb5d" rx="3" />
    </g>

    <!-- Medium Bar -->
    <g transform="translate(18, 38)">
      <text x="0" y="0" class="med-clr">MEDIUM</text>
      <text x="334" y="0" text-anchor="end" class="meta-val">{medium_solved} <tspan fill="#64748b" font-weight="500">/ 1720</tspan></text>
      <rect x="0" y="6" width="334" height="6" class="bar-track" />
      <rect x="0" y="6" width="{med_w * 334 // bar_w}" height="6" fill="#ffb800" rx="3" />
    </g>

    <!-- Hard Bar -->
    <g transform="translate(18, 60)">
      <text x="0" y="0" class="hard-clr">HARD</text>
      <text x="334" y="0" text-anchor="end" class="meta-val">{hard_solved} <tspan fill="#64748b" font-weight="500">/ 760</tspan></text>
      <rect x="0" y="6" width="334" height="6" class="bar-track" />
      <rect x="0" y="6" width="{hard_w * 334 // bar_w}" height="6" fill="#ef4743" rx="3" />
    </g>
  </g>

  <!-- Column 3: Contest Rating & Percentile -->
  <g transform="translate(638, 38)">
    <rect x="0" y="0" width="188" height="84" class="panel" />

    <g transform="translate(16, 20)">
      <text x="0" y="0" class="meta-lbl">CONTEST RATING</text>
      <text x="0" y="20" class="stat-num" fill="#ffa116">{contest_rating}</text>
    </g>

    <line x1="16" y1="48" x2="172" y2="48" stroke="#1e293b" stroke-width="1" />

    <g transform="translate(16, 64)">
      <text x="0" y="0" class="meta-lbl">PERCENTILE</text>
      <text x="75" y="0" class="meta-val" fill="#38bdf8">Top {top_pct}%</text>
      <circle cx="145" cy="-3" r="3" fill="#34d399" />
      <text x="153" y="0" class="sub-num" fill="#34d399">ACTIVE</text>
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
    
    print(f"LeetCode SVG card generated successfully at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
