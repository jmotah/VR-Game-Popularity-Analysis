import requests
from bs4 import BeautifulSoup
import pandas as pd
from DrissionPage._pages.chromium_page import ChromiumPage
import time

''' 
Make sure pip install drissionpage
Make sure to manually start Chrome with the --remote-debugging-port=9222 option enabled.
'''

def fetch_popular_vr_games(limit=100):
    """
    Fetches popular VR games from Steam, including their app IDs, prices, number of reviews, positive review percentages, 
    and supported operating systems (Windows, macOS, Linux), and VR support.

    Args:
        limit (int): Number of games to retrieve.

    Returns:
        pd.DataFrame: DataFrame containing popular VR games and information.
    """
    url = "https://store.steampowered.com/search/?sort_by=_ASC&ignore_preferences=1&tags=21978&category1=998&vrsupport=101&os=win&supportedlang=english"
    dp = ChromiumPage()
    dp.get(url)

    games = []

    while len(games) < limit:
        # Scroll to the bottom of the page using DrissionPage
        dp.scroll.to_bottom()
        time.sleep(2)
        
        soup = BeautifulSoup(dp.html, "html.parser")
        # Find game details, limited to 5.
        game_rows = soup.find_all("a", {"class": "search_result_row"})[:limit]
        for game in game_rows:
            game_title = game.find("span", class_="title").text.strip()
            app_id = game["data-ds-appid"]
            price_tag = game.find("div", {"class": "discount_final_price"})
            price = price_tag.text.strip() if price_tag else "Free"

            # Extract the review data.
            reviews_summary = game.find("span", {"class": "search_review_summary"})
            if reviews_summary:
                reviews_tooltip = reviews_summary.get("data-tooltip-html")
                if reviews_tooltip:
                    parts = reviews_tooltip.split("<br>")
                    positive_percentage = parts[0].strip()
                    review_part = parts[1]
                    reviews_count = review_part.split("of")[-1].split("user")[0].replace("the", "").strip().replace(",", "")

                    # Extracts supported platforms
            os_supported = []
            if game.find("span", class_="platform_img win"):
                os_supported.append("Windows")
            if game.find("span", class_="platform_img mac"):
                os_supported.append("macOS")
            if game.find("span", class_="platform_img linux"):
                os_supported.append("Linux")

            # Appends game data to list.
            games.append({
                "Name": game_title,
                "Steam_ID": app_id,
                "Average_Review": positive_percentage,
                "Operating_Systems": ", ".join(os_supported)
            })

            # Stop if we've reached the limit
            if len(games) >= limit:
                break

    return pd.DataFrame(games)

# Fetches and displays the popular VR games.
vr_games_df = fetch_popular_vr_games()
vr_games_df.head()
