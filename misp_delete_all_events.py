#### run script with argument of how many days (example: python3.exe ./DeleteMispEvents.py 0    # where "0" is the number of days to keep. (past 24 hours)
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import argparse
import sys

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Delete MISP events older than specified days')
    parser.add_argument('days', type=int, help='Delete events older than this many days')
    return parser.parse_args()

misp_url = 
api_key = ""
headers = {
    "Authorization": api_key,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def delete_event(event_id):
    delete_response = requests.delete(f"{misp_url}/events/{event_id}", headers=headers, verify=False)
    if delete_response.status_code == 200:
        print(f"Deleted event ID: {event_id}")
    else:
        print(f"Failed to delete event ID: {event_id} - {delete_response.text}")

def main():
    # Parse command line arguments
    args = parse_arguments()
    days = args.days

    # Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(days=days)

    # Get all events
    response = requests.get(f"{misp_url}/events/index", headers=headers, verify=False)
    if response.status_code == 200:
        events = response.json()
        
        # Filter events older than the specified days
        events_to_delete = []
        for event in events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            if event_date < cutoff_date:
                events_to_delete.append(event['id'])

        if not events_to_delete:
            print(f"No events found older than {days} days.")
            return

        ##print(f"Found {len(events_to_delete)} events older than {days} days to delete.")
        ##user_input = input("Do you want to proceed with deletion? (y/n): ")
        
        ##if user_input.lower() != 'y':
        ##    print("Operation cancelled.")
        ##    return

        # Delete events concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(delete_event, event_id): event_id for event_id in events_to_delete}
            for future in as_completed(futures):
                event_id = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"Event ID {event_id} generated an exception: {exc}")
    else:
        print(f"Failed to fetch events: {response.text}")

if __name__ == "__main__":
    main()
