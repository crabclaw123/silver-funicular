import json
from pathlib import Path

WORKOUT_FILE = Path("workout_log.json")

def load_workouts():
    if WORKOUT_FILE.exists():
        with open(WORKOUT_FILE, "r") as f:
            return json.load(f)
    return []

def save_workout(new_entry):
    data = load_workouts()
    data.append(new_entry)
    with open(WORKOUT_FILE, "w") as f:
        json.dump(data, f, indent=4)