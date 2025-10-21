import os
import sys
import shutil
import stat
import platform

# path to your stopwatch script
STOPWATCH_PATH = os.path.abspath("stopwatch.py")

if not os.path.exists(STOPWATCH_PATH):
    print(f"Error: {STOPWATCH_PATH} does not exist.")
    sys.exit(1)

system = platform.system()

if system in ("Darwin", "Linux"):
    # macOS / Linux
    target = "/usr/local/bin/stopwatch"
    try:
        # create symlink
        if os.path.islink(target) or os.path.exists(target):
            os.remove(target)
        os.symlink(STOPWATCH_PATH, target)
        # make executable
        st = os.stat(STOPWATCH_PATH)
        os.chmod(target, st.st_mode | stat.S_IEXEC)
        print(f"Symlink created: {target}")
        print("Test it with: stopwatch")
    except PermissionError:
        print("Permission denied. Try running with sudo.")
elif system == "Windows":
    # Windows
    bat_path = os.path.join(os.getenv("USERPROFILE"), "stopwatch.bat")
    with open(bat_path, "w") as f:
        f.write(f'@echo off\npy "{STOPWATCH_PATH}" %*\n')
    print(f"Batch file created: {bat_path}")
    print("Make sure the folder is in your PATH.")
    print("Test it with: stopwatch")
else:
    print(f"Unsupported OS: {system}")
