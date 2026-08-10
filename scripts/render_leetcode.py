import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
INPUT_FILE = os.path.join(DATA_DIR, "leetcode_stats.json")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "leetcode-card.svg")

DEFAULT_STATS = {
    "username": "Ragunthan",
    "solvedTotal": 21,
    "easySolved": 8,
    "mediumSolved": 11,
    "hardSolved": 2,
    "totalQuestions": 3300,
    "easyTotal": 820,
    "mediumTotal": 1720,
    "hardTotal": 760,
    "acceptanceRate": 68.4,
    "ranking": 4270870,
    "contestRating": 1685,
    "topPercentage": 12.5
}

def generate_svg(stats):
    solved_total = stats.get("solvedTotal", 21)
    easy_solved = stats.get("easySolved", 8)
    medium_solved = stats.get("mediumSolved", 11)
    hard_solved = stats.get("hardSolved", 2)
    acceptance_rate = stats.get("acceptanceRate", 68.4)
    ranking = stats.get("ranking", 4270870)
    contest_rating = stats.get("contestRating", 1685)
    top_pct = stats.get("topPercentage", 12.5)

    easy_pct = min(100, max(5, int((easy_solved / 800) * 100))) if easy_solved > 0 else 5
    medium_pct = min(100, max(5, int((medium_solved / 1600) * 100))) if medium_solved > 0 else 5
    hard_pct = min(100, max(5, int((hard_solved / 700) * 100))) if hard_solved > 0 else 5

    # Calculate stroke-dasharray for donut chart
    r = 54
    circumference = 2 * 3.14159 * r # ~339.29
    # Progress ring ratio
    progress_ratio = max(0.05, min(1.0, solved_total / 100.0))
    dash_filled = circumference * progress_ratio
    dash_empty = circumference - dash_filled

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 220" width="100%" height="220" fill="none">
  <style>
    .bg {{ fill: #0d1117; rx: 12px; stroke: #30363d; stroke-width: 1.5; }}
    .card-panel {{ fill: #161b22; rx: 8px; stroke: #30363d; stroke-width: 1; }}
    .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 16px; font-weight: 700; fill: #f0f6fc; }}
    .subtitle {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; fill: #8b949e; }}
    .stat-number {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 28px; font-weight: 800; fill: #f0f6fc; }}
    .label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 600; fill: #8b949e; }}
    .value {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; font-weight: 700; fill: #f0f6fc; }}
    .easy-text {{ fill: #2cbb5d; font-weight: 700; font-family: sans-serif; font-size: 13px; }}
    .medium-text {{ fill: #ffb800; font-weight: 700; font-family: sans-serif; font-size: 13px; }}
    .hard-text {{ fill: #ef4743; font-weight: 700; font-family: sans-serif; font-size: 13px; }}
    .orange-text {{ fill: #ffa116; font-weight: 700; font-family: sans-serif; font-size: 13px; }}
    .accent-text {{ fill: #58a6ff; font-weight: 700; font-family: sans-serif; font-size: 13px; }}
    .bar-bg {{ fill: #21262d; rx: 4px; }}
  </style>

  <!-- Container Box -->
  <rect x="0" y="0" width="850" height="220" class="bg" />

  <!-- Header -->
  <g transform="translate(24, 28)">
    <!-- LeetCode Logo Icon -->
    <path d="M13.483 0a1.374 1.374 0 0 0-.961.438L7.17 5.79a1.374 1.374 0 0 0-.008 1.933l.008.008 3.518 3.55a1.374 1.374 0 0 0 1.94 0 1.374 1.374 0 0 0 0-1.94L9.89 6.58l4.553-4.606a1.374 1.374 0 0 0-.96-1.974zm5.553 4.148a1.374 1.374 0 0 0-.968.411l-9.845 9.94a1.374 1.374 0 0 0 0 1.94l3.52 3.55a1.374 1.374 0 0 0 1.94 0l9.844-9.94a1.374 1.374 0 0 0-.96-2.338z" fill="#ffa116" transform="translate(0, -2) scale(0.9)"/>
    <text x="24" y="14" class="title">LeetCode Performance Dashboard</text>
    <text x="610" y="14" class="subtitle">leetcode.com/u/Ragunthan</text>
  </g>

  <!-- Divider Line -->
  <line x1="24" y1="46" x2="826" y2="46" stroke="#30363d" stroke-width="1" />

  <!-- Column 1: Solved Donut Ring (Left) -->
  <g transform="translate(24, 60)">
    <rect x="0" y="0" width="240" height="140" class="card-panel" />
    
    <!-- Donut Chart -->
    <g transform="translate(70, 70)">
      <!-- Donut Track -->
      <circle cx="0" cy="0" r="{r}" stroke="#21262d" stroke-width="10" fill="none" />
      <!-- Progress Arc -->
      <circle cx="0" cy="0" r="{r}" stroke="#ffa116" stroke-width="10" stroke-linecap="round" fill="none"
              stroke-dasharray="{dash_filled:.1f} {dash_empty:.1f}" transform="rotate(-90)" />
      <!-- Central Text -->
      <text x="0" y="4" text-anchor="middle" class="stat-number">{solved_total}</text>
      <text x="0" y="20" text-anchor="middle" class="subtitle">Solved</text>
    </g>

    <!-- Stat Highlights on Right of Donut -->
    <g transform="translate(150, 35)">
      <text x="0" y="0" class="label">Acceptance</text>
      <text x="0" y="18" class="orange-text">{acceptance_rate}%</text>
      
      <text x="0" y="50" class="label">Global Rank</text>
      <text x="0" y="68" class="value">#{ranking:,}</text>
    </g>
  </g>

  <!-- Column 2: Difficulty Breakdown Bars (Center) -->
  <g transform="translate(280, 60)">
    <rect x="0" y="0" width="310" height="140" class="card-panel" />

    <!-- Easy Bar -->
    <g transform="translate(20, 24)">
      <text x="0" y="0" class="easy-text">Easy</text>
      <text x="270" y="0" text-anchor="end" class="value">{easy_solved}</text>
      <rect x="0" y="10" width="270" height="8" class="bar-bg" />
      <rect x="0" y="10" width="{int(270 * (easy_pct / 100.0))}" height="8" fill="#2cbb5d" rx="4" />
    </g>

    <!-- Medium Bar -->
    <g transform="translate(20, 64)">
      <text x="0" y="0" class="medium-text">Medium</text>
      <text x="270" y="0" text-anchor="end" class="value">{medium_solved}</text>
      <rect x="0" y="10" width="270" height="8" class="bar-bg" />
      <rect x="0" y="10" width="{int(270 * (medium_pct / 100.0))}" height="8" fill="#ffb800" rx="4" />
    </g>

    <!-- Hard Bar -->
    <g transform="translate(20, 104)">
      <text x="0" y="0" class="hard-text">Hard</text>
      <text x="270" y="0" text-anchor="end" class="value">{hard_solved}</text>
      <rect x="0" y="10" width="270" height="8" class="bar-bg" />
      <rect x="0" y="10" width="{int(270 * (hard_pct / 100.0))}" height="8" fill="#ef4743" rx="4" />
    </g>
  </g>

  <!-- Column 3: Contest Rating & Rank Summary (Right) -->
  <g transform="translate(606, 60)">
    <rect x="0" y="0" width="220" height="140" class="card-panel" />
    
    <g transform="translate(20, 25)">
      <text x="0" y="0" class="label">Contest Rating</text>
      <text x="0" y="24" class="stat-number" fill="#ffa116">{contest_rating}</text>
    </g>

    <line x1="20" y1="72" x2="200" y2="72" stroke="#30363d" stroke-width="1" />

    <g transform="translate(20, 95)">
      <text x="0" y="0" class="label">Top Percentile</text>
      <text x="0" y="20" class="accent-text">Top {top_pct}%</text>
      <text x="180" y="20" text-anchor="end" class="subtitle">🎯 Active</text>
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
