import streamlit as st
from data_handler import load_workouts
from logger import workout_logger
from tracker import volume_overview
from history import display_workout_history
from nutrition import nutrition_strategy_tip
from progression import progression_engine
from volume_goals import volume_goal_ui
from exercise_manager import manage_saved_exercises


st.set_page_config(page_title="Hypertrophy App", layout="wide")

st.title("🏋️ Hypertrophy Tracker")

# Load data
workouts = load_workouts()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select a page:", [
    "Log Workout",
    "Volume Tracker",
    "Workout History",
    "Diet Tips",
    "Progression Suggestions",
    "Volume Overview",
    "Set Volume Goals",
    "Exercise Library",
    "Tonnage Tracker"  # ← new page option
])

# Main display logic
if page == "Set Volume Goals":
    volume_goal_ui()
if page == "Log Workout":
    exercise = workout_logger()
    if exercise:
        progression_engine(exercise)
elif page == "Volume Tracker":
    volume_overview(workouts)
elif page == "Workout History":
    display_workout_history()
elif page == "Diet Tips":
    user_data = {"mesocycle": {"phase": "Accumulation"}}
    nutrition_strategy_tip(user_data["mesocycle"]["phase"], goal="maintenance")
elif page == "Progression Suggestions":
    selected_exercise = st.text_input("Enter or select an exercise:")
    if selected_exercise:
        progression_engine(selected_exercise)
elif page == "Volume Overview":
    volume_overview(workouts)
elif page == "Exercise Library":
    manage_saved_exercises()
elif page == "Tonnage Tracker":
    from tonnage import tonnage_tracker
    tonnage_tracker()
