from datetime import datetime, timedelta, timezone
from pymisp import PyMISP
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Replace with your MISP instance URL and API key
MISP_URL = 
MISP_API_KEY = 
VERIFY_SSL = False  # Set to True if your MISP instance uses a valid SSL certificate

def pull_recent_feed_events(last_hours=24):
    try:
        # Initialize MISP client
        misp = PyMISP(MISP_URL, MISP_API_KEY, VERIFY_SSL)

        # Fetch all feeds
        feeds = misp.feeds()
        if not feeds:
            print("No feeds found in the MISP instance.")
            return

        print(f"Found {len(feeds)} feeds. Starting synchronization for the last {last_hours} hours...")

        for feed in feeds:
            if not feed['Feed']['enabled']:
                print(f"Skipping disabled feed: {feed['Feed']['name']}")
                continue

            # Trigger feed synchronization
            print(f"Synchronizing feed: {feed['Feed']['name']} (Last {last_hours} hours)")
            result = misp.fetch_feed(feed['Feed']['id'])
            if result:
                print(f"Feed {feed['Feed']['name']} synchronized successfully.")
            else:
                print(f"Failed to synchronize feed: {feed['Feed']['name']}")

    except Exception as e:
        print(f"Error while pulling events from feeds: {e}")

if __name__ == "__main__":
    pull_recent_feed_events(last_hours=24)
