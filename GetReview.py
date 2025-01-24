import requests
from bs4 import BeautifulSoup
import pandas as pd
from FetchPopularGames import vr_games_df
import time

# Steam App IDs for the selected VR apps
# app_info = {
#     "War Thunder": "236390",
#     "No Man's Sky": "275850",
#     "Phasmophobia": "739630",
#     "HITMAN World of Assassination": "1659040",
#     "VRChat": "438100"
# }
app_info = vr_games_df.set_index('Name')['Steam_ID'].to_dict()

def get_review_summary_and_total(app_id):
    """
    Scrapes the review summary and total reviews for the given Steam app.

    Args:
    - app_id (str): The Steam App ID.

    Returns:
    - dict: A dictionary with 'review_summary' and 'total_reviews'.
    """
    url = f"https://store.steampowered.com/app/{app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            review_summary = soup.find_all("span", {"class": "game_review_summary"})[1].text.strip()
        except:
            review_summary = 'N/A'
        try:
            total_reviews = soup.find("meta", {"itemprop": "reviewCount"})["content"]
        except:
            total_reviews = 'N/A'
        return {"review_summary": review_summary, "total_reviews": total_reviews}
    return {"review_summary": "N/A", "total_reviews": "N/A"}

def collect_vr_app_data(app_info):
    """
    Collects VR app data by fetching Steam API and scraping the review information.

    Args:
    - app_info (dict): A dictionary mapping app names to their Steam App IDs.

    Returns:
    - list: A list of dictionaries containing app data.
    """
    app_data = []
    for app_name, app_id in app_info.items():
        # Fetch API details for the app
        api_url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
        api_response = requests.get(api_url).json()[app_id]["data"]
        
        # Scrape review summary and total reviews
        review_data = get_review_summary_and_total(app_id)
        
        # Check if the app supports VR based on its categories
        vr_supported = any("VR" in category.get("description", "") for category in api_response.get("categories", []))
        
        # Format the price correctly as currency
        price = api_response.get("price_overview", {}).get("final", "N/A")
        price_formatted = f"${price / 100:.2f}" if price != "N/A" else "N/A"
        
        # Append collected data to the list
        app_data.append({
            "Name": api_response.get("name", app_name),
            "Price": price_formatted,
            "Review_Summary": review_data["review_summary"],
            "Number_of_Reviews": review_data["total_reviews"],
            "Release_Date": api_response.get("release_date", {}).get("date", "N/A"),
            "Developers": api_response.get("developers", ["N/A"]),
            "Genres": [genre["description"] for genre in api_response.get("genres", [])] if api_response.get("genres") else "N/A",
            "Supported_VR": vr_supported
        })
        time.sleep(1)
    return app_data

# Fetch VR app data and convert it to a DataFrame
df_vr_apps = pd.DataFrame(collect_vr_app_data(app_info))

# Display the styled DataFrame
df_vr_apps.head()
