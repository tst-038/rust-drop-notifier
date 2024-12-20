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
    Reads the last round details (round number and status) from a file.
    """
    if os.path.exists(LAST_ROUND_FILE):
        with open(LAST_ROUND_FILE, "r") as file:
            return file.read().strip().split(",")
    return None, None

def write_last_round(round_number, round_status):
    """
    Writes the current round details (round number and status) to the file.
    """
    with open(LAST_ROUND_FILE, "w") as file:
        file.write(f"{round_number},{round_status}")

def main():
    logging.info("Starting Rust drop notifier...")

    while True:
        drop_data = get_latest_drop()
        if drop_data:
            last_round, last_status = read_last_round()

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
                write_last_round(drop_data["round_number"], drop_data["round_status"])

            elif drop_data["round_status"] != last_status:
                logging.info(f"Round status updated to: {drop_data['round_status']}")
                send_webhook_notification(
                    drop_data["round_number"],
                    drop_data["event_title"],
                    drop_data["round_status"],
                    drop_data["start_date"],
                    drop_data["end_date"],
                    drop_data.get("image_url")
                )
                write_last_round(drop_data["round_number"], drop_data["round_status"])

            else:
                logging.info(
                    f"No updates. Current round: {drop_data['round_number']}, status: {drop_data['round_status']}")
        else:
            logging.error("No drop data returned.")

        # Wait for 1 hour
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()