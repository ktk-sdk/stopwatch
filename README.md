# Stopwatch

<img width="682" height="447" alt="Screenshot 2025-10-21 at 4 14 12 PM" src="https://github.com/user-attachments/assets/6f2d4e13-5ff0-46bb-85f2-179f821bd6dd" />

Stopwatch is a simple command-line stopwatch to track time spent on activities~

## Features

* Start, stop, and track multiple activities
* View status of running timers
* View history of all sessions
  * Data stored in `data/YYYY-MM-DD/<activity>.json` next to the script
* Global command works from any directory

## Installation

1. Download this folder, place it wherever you like, then copy the absolute path of `stopwatch.py`, for example:

```
Users/Kiki/Stopwatch/stopwatch.py
```

2. Make it executable:

```bash
chmod +x Users/Kiki/Stopwatch/stopwatch.py
```

3. Create a global symlink:

### macOS / Linux
```python3 setup_stopwatch.py```

You can test if this worked with ```which stopwatch```

### Windows
```python .\setup_stopwatch.py```

then add the location of the installation to your PATH variables

You can test if this worked with ```where stopwatch```



## Usage

```bash
# Start a timer for an activity
stopwatch start reading

# Stop the timer
stopwatch stop reading

# Check current status of all activities today
stopwatch status

# Show history for a specific activity
stopwatch history reading

# Show history for all activities today
stopwatch history
```


## Data Storage

* Data folder is **next to the script**:

```
~/Stopwatch/data/YYYY-MM-DD/<activity>.json
```

* Example:

```
~/Stopwatch/data/2025-10-21/reading.json
~/Stopwatch/data/2025-10-21/coding.json
```

* Each JSON contains:

```json
{
  "total": 1800,
  "sessions": [
    {
      "start": "2025-10-21 09:00:00",
      "end": "2025-10-21 09:30:00",
      "duration_sec": 1800
    }
  ]
}
```

* New sessions are **appended**, so previous sessions are preserved.

---

## Notes

* The stopwatch supports **multiple activities at the same time**. Each activity has its own JSON file.
* Data is **centralized**, so you can use the global `stopwatch` command from any directory.
* Daily folders keep data organized and prevent JSON files from growing too large.

