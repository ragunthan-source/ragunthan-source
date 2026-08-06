"""
fetch_contributions.py

Fetches GitHub contribution graph HTML directly from:
https://github.com/users/<username>/contributions

Parses daily contribution counts using BeautifulSoup and calculates statistics:
- Yearly total contributions
- Current streak
- Longest streak
- Best day (maximum commits on a single day)
- Monthly totals

Saves structured data into data/contributions.json.
Includes robust error handling and realistic fallback data generator for offline/CI use.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta, date
import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup


class ContributionFetcher:
    """Fetches and parses GitHub user contribution data without third-party services."""

    def __init__(self, username: str = "ragunthan-source", output_json: str = "data/contributions.json"):
        self.username = username
        self.output_json = output_json
        self.url = f"https://github.com/users/{username}/contributions"

    def fetch_raw_html(self) -> str:
        """Download raw contribution HTML snippet from GitHub."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        try:
            print(f"[+] Fetching GitHub contributions for user: {self.username}...")
            response = requests.get(self.url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.text
            else:
                print(f"[!] GitHub API returned status code {response.status_code}. Using fallback data.")
                return ""
        except Exception as e:
            print(f"[!] Failed to connect to GitHub ({e}). Using fallback data generator.")
            return ""

    def parse_contributions(self, html_content: str) -> list[dict]:
        """Parse BeautifulSoup HTML for contribution cells (td or rect)."""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        days_data = []

        # GitHub uses <td class="ContributionCalendar-day" data-date="..." data-level="...">
        # or <rect class="ContributionCalendar-day" ...>
        cells = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)

        for cell in cells:
            date_str = cell.get("data-date")
            if not date_str:
                continue

            level = int(cell.get("data-level", "0"))
            
            # Count extraction: tooltips or text content or aria-label
            count = 0
            aria_label = cell.get("aria-label", "")
            id_val = cell.get("id")
            
            # Check associated tooltip element if present
            tooltip_count = None
            if id_val:
                tooltip = soup.find("tool-tip", attrs={"for": id_val})
                if tooltip:
                    aria_label = tooltip.text.strip()

            if aria_label:
                # Format e.g. "No contributions on January 1, 2024" or "5 contributions on Feb 3, 2024"
                parts = aria_label.split()
                if parts and parts[0].isdigit():
                    count = int(parts[0])
                elif "No" in parts[0]:
                    count = 0
            else:
                # Estimate count from level if exact text is missing
                level_estimates = {0: 0, 1: 2, 2: 5, 3: 9, 4: 14}
                count = level_estimates.get(level, 0)

            days_data.append({"date": date_str, "count": count, "level": level})

        # Sort chronologically
        days_data.sort(key=lambda x: x["date"])
        return days_data

    def generate_fallback_data(self) -> list[dict]:
        """Generates 53 weeks (371 days) of realistic hacker contribution data."""
        print("[+] Generating high-activity terminal contribution dataset...")
        today = date.today()
        start_date = today - timedelta(days=370)

        import random
        random.seed(42)  # Deterministic seed for consistency

        days_data = []
        curr = start_date
        while curr <= today:
            d_str = curr.strftime("%Y-%m-%d")
            # Weekend vs weekday weighting
            is_weekend = curr.weekday() in (5, 6)
            prob_active = 0.65 if is_weekend else 0.85

            if random.random() < prob_active:
                count = random.randint(1, 16)
                if count <= 2:
                    level = 1
                elif count <= 5:
                    level = 2
                elif count <= 9:
                    level = 3
                else:
                    level = 4
            else:
                count = 0
                level = 0

            days_data.append({"date": d_str, "count": count, "level": level})
            curr += timedelta(days=1)

        return days_data

    def compute_statistics(self, days_data: list[dict]) -> dict:
        """Calculate total, current streak, longest streak, best day, and monthly totals."""
        if not days_data:
            return {}

        total_contributions = sum(d["count"] for d in days_data)
        
        # Streak calculations
        current_streak = 0
        longest_streak = 0
        temp_streak = 0
        
        # Best day
        best_day = max(days_data, key=lambda x: x["count"]) if days_data else {"date": "N/A", "count": 0}

        # Monthly totals
        monthly_totals = {}
        for d in days_data:
            month_key = d["date"][:7]  # YYYY-MM
            monthly_totals[month_key] = monthly_totals.get(month_key, 0) + d["count"]

        # Longest streak calculation
        for d in days_data:
            if d["count"] > 0:
                temp_streak += 1
                if temp_streak > longest_streak:
                    longest_streak = temp_streak
            else:
                temp_streak = 0

        # Current streak calculation (backwards from most recent day)
        for d in reversed(days_data):
            if d["count"] > 0:
                current_streak += 1
            else:
                # If today has 0 commits so far, allow 1 day grace for yesterday
                if current_streak == 0 and d["date"] == date.today().strftime("%Y-%m-%d"):
                    continue
                break

        return {
            "total_contributions": total_contributions,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": {"date": best_day["date"], "count": best_day["count"]},
            "monthly_totals": monthly_totals,
        }

    def run(self) -> dict:
        """Execute fetching, parsing, analysis, and JSON writing."""
        html_content = self.fetch_raw_html()
        days_data = self.parse_contributions(html_content)

        if not days_data:
            days_data = self.generate_fallback_data()

        stats = self.compute_statistics(days_data)

        payload = {
            "username": self.username,
            "generated_at": datetime.now().isoformat(),
            "stats": stats,
            "days": days_data,
        }

        output_dir = os.path.dirname(self.output_json)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        print(f"[OK] Saved contribution stats to {self.output_json}")
        print(f"     Total Contributions: {stats['total_contributions']}")
        print(f"     Current Streak: {stats['current_streak']} days")
        print(f"     Longest Streak: {stats['longest_streak']} days")
        print(f"     Best Day: {stats['best_day']['date']} ({stats['best_day']['count']} commits)")
        return payload


def main():
    parser = argparse.ArgumentParser(description="Fetch and parse GitHub contributions.")
    parser.add_argument("--username", default="ragunthan-source", help="GitHub username")
    parser.add_argument("--output", default="data/contributions.json", help="Output JSON path")
    args = parser.parse_args()

    fetcher = ContributionFetcher(args.username, args.output)
    fetcher.run()


if __name__ == "__main__":
    main()
