import streamlit as st
import json
from pathlib import Path

GOAL_FILE = Path("volume_goals.json")

def save_volume_goals(goals):
    with open(GOAL_FILE, "w") as f:
        json.dump(goals, f, indent=4)

def load_volume_goals():
    if GOAL_FILE.exists():
        with open(GOAL_FILE, "r") as f:
            return json.load(f)
    return {}

def volume_goal_ui():
    st.sidebar.markdown("🎯 **Set Weekly Volume Goals**")
    goals = load_volume_goals()

    for muscle in [
        "Chest", "Back", "Legs", "Shoulders", "Arms",
        "Glutes", "Core", "Forearms", "Calves"
    ]:
        val = st.sidebar.number_input(
            f"{muscle} sets/week",
            min_value=0,
            max_value=30,
            step=1,
            value=goals.get(muscle, 10)
        )
        goals[muscle] = val

    if st.sidebar.button("💾 Save Volume Goals"):
        save_volume_goals(goals)
        st.sidebar.success("Goals saved!")

    return goals