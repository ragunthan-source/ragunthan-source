import json
import os
import sys
import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "leetcode_stats.json")

DEFAULT_STATS = {
    "username": "Ragunthan",
    "solvedTotal": 250,
    "easySolved": 110,
    "mediumSolved": 115,
    "hardSolved": 25,
    "totalQuestions": 3300,
    "easyTotal": 820,
    "mediumTotal": 1720,
    "hardTotal": 760,
    "acceptanceRate": 68.4,
    "ranking": 125430,
    "contestRating": 1685,
    "topPercentage": 12.5
}

def fetch_leetcode_stats(username="Ragunthan"):
    url = "https://leetcode.com/graphql"
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
        profile {
          ranking
        }
      }
      userContestRanking(username: $username) {
        rating
        globalRanking
        topPercentage
      }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://leetcode.com"
    }

    try:
        response = requests.post(url, json={"query": query, "variables": {"username": username}}, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user = data.get("data", {}).get("matchedUser")
            if user:
                stats = dict(DEFAULT_STATS)
                stats["username"] = username
                ac_submissions = user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
                
                total_solved = 0
                for item in ac_submissions:
                    diff = item.get("difficulty")
                    cnt = item.get("count", 0)
                    if diff == "All":
                        stats["solvedTotal"] = cnt
                        total_solved = cnt
                    elif diff == "Easy":
                        stats["easySolved"] = cnt
                    elif diff == "Medium":
                        stats["mediumSolved"] = cnt
                    elif diff == "Hard":
                        stats["hardSolved"] = cnt
                
                profile = user.get("profile", {})
                if profile and profile.get("ranking"):
                    stats["ranking"] = profile.get("ranking")
                
                contest = data.get("data", {}).get("userContestRanking")
                if contest:
                    if contest.get("rating"):
                        stats["contestRating"] = round(contest.get("rating"))
                    if contest.get("topPercentage"):
                        stats["topPercentage"] = round(contest.get("topPercentage"), 1)
                
                return stats
    except Exception as e:
        print(f"Warning: Failed to fetch online LeetCode stats for '{username}': {e}. Using cached/default values.")
    
    return DEFAULT_STATS

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "Ragunthan"
    os.makedirs(DATA_DIR, exist_ok=True)
    
    stats = fetch_leetcode_stats(username)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    print(f"LeetCode statistics saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
