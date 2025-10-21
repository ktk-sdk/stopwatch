#!/usr/bin/env python3
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# store history in subfolder
BASE_DIR = Path(__file__).resolve().parent / "History"  # always store JSON files next to the script's real location
BASE_DIR.mkdir(parents=True, exist_ok=True)             # make directory if it doesn't exist already

# UTILITY FUNCTIONS

# Return the JSON file path for a given activity and today's date
def get_activity_file(activity):
    today_folder = BASE_DIR / datetime.now().strftime("%Y-%m-%d")
    today_folder.mkdir(parents=True, exist_ok=True)
    return today_folder / f"{activity}.json"

# Load activity data from JSON if it exists
def load_data(activity):
    file = get_activity_file(activity)
    if file.exists():
        with open(file, "r") as f:
            return json.load(f)
    return {}

# Save activity data to JSON
def save_data(activity, data):
    file = get_activity_file(activity)
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Format seconds into HH:MM:SS
def format_duration(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02}"


# COMMANDS
def start(activity):
    data = load_data(activity)
    if "start" in data:
        print(f"'{activity}' is already running.")
        return
    data["start"] = time.time()
    data["start_time_str"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.setdefault("sessions", [])
    data.setdefault("total", 0)
    save_data(activity, data)
    print(f"Started '{activity}' at {data['start_time_str']}")

def stop(activity):
    data = load_data(activity)
    if "start" not in data:
        print(f"'{activity}' is not running.")
        return

    start_time = data["start"]
    end_time = time.time()
    duration = end_time - start_time

    session = {
        "start": data["start_time_str"],
        "end": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_sec": round(duration, 2)
    }

    # append session and update total
    data.setdefault("sessions", []).append(session)
    data["total"] = data.get("total", 0) + duration

    # remove temporary keys
    data.pop("start", None)
    data.pop("start_time_str", None)

    save_data(activity, data)
    print(f"Stopped '{activity}' — {format_duration(duration)} (total {format_duration(data['total'])})")

def status():
    today_folder = BASE_DIR / datetime.now().strftime("%Y-%m-%d")
    if not today_folder.exists():
        print("No activities recorded today.")
        return
    for file in today_folder.glob("*.json"):
        activity = file.stem
        data = load_data(activity)
        if "start" in data:
            running_for = time.time() - data["start"]
            print(f"{activity} running for {format_duration(running_for)} (started {data['start_time_str']})")
        else:
            print(f"{activity} total {format_duration(data.get('total',0))}, {len(data.get('sessions',[]))} sessions")

def history(activity=None):
    if activity:
        data = load_data(activity)
        if not data.get("sessions"):
            print(f"No history for '{activity}'.")
            return
        print(f"History for '{activity}':")
        for s in data["sessions"]:
            print(f"  {s['start']} → {s['end']} ({format_duration(s['duration_sec'])})")
    else:
        today_folder = BASE_DIR / datetime.now().strftime("%Y-%m-%d")
        if not today_folder.exists():
            print("No activities recorded today.")
            return
        print("All activities today:")
        for file in today_folder.glob("*.json"):
            act = file.stem
            d = load_data(act)
            print(f"  {act}: {len(d.get('sessions',[]))} sessions, total {format_duration(d.get('total',0))}")

def main():
    error_msg = "Usage: stopwatch [start|stop|status|history] <activity>"

    if len(sys.argv) < 2:
        print(error_msg)
        return

    cmd = sys.argv[1]

    if cmd == "start" and len(sys.argv) == 3:
        start(sys.argv[2])
    elif cmd == "stop" and len(sys.argv) == 3:
        stop(sys.argv[2])
        
    elif cmd == "status":
        status()
    elif cmd == "history":
        if len(sys.argv) == 3:
            history(sys.argv[2])
        else:
            history()
    else:
        print(error_msg)

if __name__ == "__main__":
    main()
