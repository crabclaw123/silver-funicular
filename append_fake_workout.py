import json
from pathlib import Path
from datetime import date

LOG_FILE = Path("workout_log.json")

# ✅ Step 1: Load existing workouts
if LOG_FILE.exists():
    with open(LOG_FILE, "r") as f:
        workouts = json.load(f)
else:
    workouts = []

# ✅ Step 2: Define the new workout entry
new_workout = {
    "date": str(date.today()),
    "type": "Volume",
    "exercises": [
        {
            "muscle_group": "Chest",
            "exercise": "Incline Dumbbell Press",
            "equipment": "Dumbbell",
            "sets": [
                {"reps": 10, "weight": 45},
                {"reps": 8, "weight": 50},
                {"reps": 6, "weight": 55}
            ]
        },
        {
            "muscle_group": "Shoulders",
            "exercise": "Lateral Raises",
            "equipment": "Cable",
            "sets": [
                {"reps": 12, "weight": 15},
                {"reps": 12, "weight": 15}
            ]
        }
    ]
}

# ✅ Step 3: Append and save
workouts.append(new_workout)

with open(LOG_FILE, "w") as f:
    json.dump(workouts, f, indent=4)

print("✅ Fake workout successfully appended.")