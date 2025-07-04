# --- data_handler.py ---
# Handles saving and loading workout data.

import json
from pathlib import Path
import os
import json

IN_PROGRESS_FILE = "in_progress_workout.json"

def save_all_workouts(workouts):
    with open(WORKOUT_LOG_FILE, "w") as f:
        json.dump(workouts, f, indent=2)

def load_in_progress_workout():
    if os.path.exists(IN_PROGRESS_FILE):
        with open(IN_PROGRESS_FILE, "r") as f:
            return json.load(f)
    return []

def save_in_progress_workout(data):
    with open(IN_PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def clear_in_progress_workout():
    if os.path.exists(IN_PROGRESS_FILE):
        os.remove(IN_PROGRESS_FILE)


WORKOUT_LOG_FILE = Path("workout_log.json")

def load_workouts():
    if WORKOUT_LOG_FILE.exists():
        with open(WORKOUT_LOG_FILE, "r") as f:
            try:
                data = json.load(f)

                # Defensive fix: flatten nested lists
                flat_workouts = []
                for entry in data:
                    if isinstance(entry, list):
                        flat_workouts.extend(entry)
                    else:
                        flat_workouts.append(entry)

                return flat_workouts
            except json.JSONDecodeError:
                return []
    return []

def save_workout(entry):
    workouts = load_workouts()
    workouts.append(entry)
    with open(WORKOUT_LOG_FILE, "w") as f:
        json.dump(workouts, f, indent=2)
