import os
import subprocess
from datetime import datetime

# Name of the file to back up
LOG_FILE = "workout_log.json"

# Optional: customize commit message with a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_msg = f"Backup workout log – {timestamp}"

def backup_log():
    if not os.path.exists(LOG_FILE):
        print(f"❌ {LOG_FILE} not found.")
        return

    try:
        subprocess.run(["git", "add", LOG_FILE], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Workout log successfully backed up to GitHub!")
    except subprocess.CalledProcessError as e:
        print("❌ Git command failed:", e)

if __name__ == "__main__":
    backup_log()