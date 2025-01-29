import requests
from bs4 import BeautifulSoup
from src.config import DROP_URL

def get_latest_drop():
    """
    Scrapes the Rust drops website and returns details about the latest drop round.
    """
    response = requests.get(DROP_URL)
    if response.status_code != 200:
        print(f"Failed to fetch drops. Status: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the round info
    round_info_element = soup.find("div", class_="round-info")
    if not round_info_element:
        print("No round info found on the page.")
        return None

    # Extract the round number
    round_number = round_info_element.find("span", class_="round-info-number").text.strip()

    # Extract the event title
    event_title = round_info_element.find("span", class_="round-info-title").text.strip()

    # Extract the round status
    if not round_info_element.find("span", class_="round-info-live"):
        round_status = "Announced"
    else:
        round_status = round_info_element.find("span", class_="round-info-live").text.strip()

    # Find the event dates
    event_date_element = soup.find("div", class_="event-date")
    if event_date_element:
        start_date = event_date_element.find_all("span", class_="date")[0].text.strip()
        end_date = event_date_element.find_all("span", class_="date")[1].text.strip()
    else:
        start_date = end_date = "Dates not found."

    # Extract the main image URL
    image_tag = soup.find("div", class_="hero-image").find("img")
    if image_tag:
        image_url = image_tag["src"]
    else:
        image_url = None

    return {
        "round_number": round_number,
        "event_title": event_title,
        "round_status": round_status,
        "start_date": start_date,
        "end_date": end_date,
        "image_url": image_url
    }