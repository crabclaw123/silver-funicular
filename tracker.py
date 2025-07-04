# --- tracker.py ---
# Displays weekly volume per muscle group and overlays volume goal lines

import streamlit as st
import datetime
import matplotlib.pyplot as plt
import json
from pathlib import Path

GOAL_FILE = Path("volume_goals.json")

def load_volume_goals():
    if GOAL_FILE.exists():
        with open(GOAL_FILE, "r") as f:
            return json.load(f)
    return {}

def volume_overview(workouts):
    st.subheader("📊 Weekly Volume Tracker")

    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    volume_by_muscle = {}

    for w in workouts:
        w_date = datetime.datetime.strptime(w["date"], "%Y-%m-%d").date()
        if w_date >= seven_days_ago:
            for exercise in w.get("exercises", []):
                muscle = exercise.get("muscle_group")
                if muscle:
                    volume_by_muscle[muscle] = volume_by_muscle.get(muscle, 0) + len(exercise.get("sets", []))

    if volume_by_muscle:
        st.write("### Weekly Volume Summary")
        goals = load_volume_goals()
        cols = st.columns(len(volume_by_muscle))
        for idx, (muscle, sets) in enumerate(sorted(volume_by_muscle.items())):
            with cols[idx]:
                goal = goals.get(muscle, 0)
                st.metric(label=muscle, value=f"{sets}/{goal} sets")

        with st.expander("See compact bar chart"):
            fig, ax = plt.subplots(figsize=(4, 2))
            muscles = list(volume_by_muscle.keys())
            sets = list(volume_by_muscle.values())
            goal_lines = [goals.get(m, 0) for m in muscles]

            bars = ax.bar(muscles, sets, width=0.5, label="Actual Volume")

            # Overlay goal lines
            for i, goal in enumerate(goal_lines):
                ax.axhline(y=goal, color='red', linestyle='dashed', linewidth=1)

            ax.set_xlabel("Muscle", fontsize=8)
            ax.set_ylabel("Sets", fontsize=8)
            ax.set_title("7-Day Volume vs Goals", fontsize=10)
            ax.tick_params(axis='x', labelrotation=45, labelsize=7)
            ax.tick_params(axis='y', labelsize=7)
            plt.tight_layout(pad=0.5)
            st.pyplot(fig)
    else:
        st.write("No logged workouts in the last 7 days.")
