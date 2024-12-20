import requests
import logging
from datetime import datetime
from src.config import WEBHOOK_URL, ROLE_ID, DROP_URL

def send_webhook_notification(round_number, event_title, round_status, start_date, end_date, image_url=None):
    """
    Sends an embedded notification to the configured Discord webhook.
    Optionally tags a role if the event status is "Event Live".
    """

    # Only mention the role if the event status is "Event Live"
    if round_status.lower() == "event live":
        content = f"<@&{ROLE_ID}> New Rust drop round is live! 🎉"
    else:
        content = f"New Rust drop round is on its way!"

    # Replace 'UTC' with ' +0000' for parsing and convert to ISO 8601 format
    start_date = start_date.replace(" UTC", " +0000")
    end_date = end_date.replace(" UTC", " +0000")

    try:
        # Parse the dates to datetime objects
        start_date_obj = datetime.strptime(start_date, "%B %d, %Y at %I:%M %p %z")
        end_date_obj = datetime.strptime(end_date, "%B %d, %Y at %I:%M %p %z")

        # Convert to Unix timestamp (seconds since the Unix epoch)
        start_timestamp = int(start_date_obj.timestamp())
        end_timestamp = int(end_date_obj.timestamp())

    except ValueError as e:
        logging.error(f"Error parsing date: {e}")
        return

    embed = {
        "title": f"{round_number} - {event_title}",
        "url": DROP_URL,
        "description": f"Status: {round_status}",
        "color": 65280,  # Green color
        "fields": [
            {"name": "Start Date", "value": f"<t:{start_timestamp}>", "inline": True},
            {"name": "End Date", "value": f"<t:{end_timestamp}>", "inline": True},
        ],
        "footer": {"text": "Rust Drop Notification"},
    }

    # Add the image to the embed if it's available
    if image_url:
        embed["image"] = {"url": image_url}

    data = {
        "content": content,  # This is where the role is mentioned if event is live
        "embeds": [embed],
    }

    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        logging.info("Notification sent successfully!")
    else:
        logging.error(f"Failed to send notification. Status: {response.status_code}")