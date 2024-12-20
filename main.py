import logging
import os
import time
from src.scraper import get_latest_drop
from src.notifier import send_webhook_notification
from src.config import CHECK_INTERVAL

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# File to store the last round number
LAST_ROUND_FILE = "last_round.txt"

def read_last_round():
    """
    Reads the last round number from a file.
    """
    if os.path.exists(LAST_ROUND_FILE):
        with open(LAST_ROUND_FILE, "r") as file:
            return file.read().strip()
    return None

def write_last_round(round_number):
    """
    Writes the current round number to the file.
    """
    with open(LAST_ROUND_FILE, "w") as file:
        file.write(round_number)

def main():
    logging.info("Starting Rust drop notifier...")

    while True:
        drop_data = get_latest_drop()
        if drop_data:
            last_round = read_last_round()

            # Compare the current round with the last round
            if drop_data["round_number"] != last_round:
                logging.info(f"New round found: {drop_data['round_number']}")
                send_webhook_notification(
                    drop_data["round_number"],
                    drop_data["event_title"],
                    drop_data["round_status"],
                    drop_data["start_date"],
                    drop_data["end_date"],
                    drop_data.get("image_url")
                )
                # Update the last round
                write_last_round(drop_data["round_number"])
            else:
                logging.info(f"No new round. Current round: {drop_data['round_number']}")
        else:
            logging.error("No drop data returned.")

        # Wait for 1 hour
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()