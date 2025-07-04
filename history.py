# --- history.py ---
import streamlit as st
import json
import os
from datetime import datetime
from data_handler import load_workouts, save_all_workouts  # UPDATED IMPORT

WORKOUT_LOG_FILE = "workout_log.json"
IN_PROGRESS_FILE = "in_progress_workout.json"

def display_workout_history():
    # Session state to manage deferred deletes
    if "delete_workout_idx" not in st.session_state:
        st.session_state.delete_workout_idx = None
    if "delete_exercise" not in st.session_state:
        st.session_state.delete_exercise = None
    if "safe_delete_ran" not in st.session_state:
        st.session_state.safe_delete_ran = False

    # Load saved workouts
    workouts = load_workouts()

    # Handle any deferred deletes first, *before UI renders*
    if not st.session_state.safe_delete_ran:
        if st.session_state.delete_exercise:
            i, j = st.session_state.delete_exercise
            try:
                workouts[i]["exercises"].pop(j)
                save_all_workouts(workouts)  # ✅ FIXED
            except IndexError:
                st.warning("Couldn't delete exercise. Index out of range.")
            st.session_state.delete_exercise = None
            st.session_state.safe_delete_ran = True
            st.rerun()

        if st.session_state.delete_workout_idx is not None:
            try:
                workouts.pop(st.session_state.delete_workout_idx)
                save_all_workouts(workouts)  # ✅ FIXED
            except IndexError:
                st.warning("Couldn't delete workout. Index out of range.")
            st.session_state.delete_workout_idx = None
            st.session_state.safe_delete_ran = True
            st.rerun()

    # Normal display logic
    st.subheader("📜 Workout History")
    if not workouts:
        st.info("No workouts logged yet.")
        return

    for i, entry in enumerate(workouts):
        if not isinstance(entry, dict):
            continue

        with st.expander(f"{entry['date']} — {entry.get('type', 'Unknown')}"):
            edited = False

            # Allow date editing
            new_date = st.date_input("Edit Date", value=datetime.strptime(entry['date'], "%Y-%m-%d").date(), key=f"edit_date_{i}")
            new_date_str = new_date.strftime("%Y-%m-%d")
            if new_date_str != entry["date"]:
                entry["date"] = new_date_str
                edited = True

            for j, exercise in enumerate(entry.get("exercises", [])):
                st.markdown(f"**{exercise['muscle_group']} - {exercise['exercise']}**")
                equipment = exercise.get("equipment", "")
                st.text(f"Equipment: {equipment}")

                for s_idx, s in enumerate(exercise.get("sets", [])):
                    cols = st.columns(2)
                    with cols[0]:
                        weight = st.number_input(
                            "Weight (lbs)", min_value=0.0, max_value=2000.0, step=0.5,
                            value=float(s["weight"]), format="%.1f",
                            key=f"edit_weight_{i}_{j}_{s_idx}"
                        )
                    with cols[1]:
                        reps = st.number_input(
                            "Reps", min_value=1, max_value=100, step=1,
                            value=int(s["reps"]),
                            key=f"edit_reps_{i}_{j}_{s_idx}"
                        )
                    s["weight"], s["reps"] = weight, reps

                new_equipment = st.selectbox(
                    "Edit Equipment",
                    ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"],
                    index=["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"].index(equipment)
                    if equipment in ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"] else 0,
                    key=f"edit_equipment_{i}_{j}"
                )

                if new_equipment != equipment:
                    exercise["equipment"] = new_equipment
                    edited = True

                if st.button(f"❌ Delete Exercise", key=f"delete_ex_{i}_{j}"):
                    st.session_state.delete_exercise = (i, j)
                    st.session_state.safe_delete_ran = False
                    st.rerun()

            if st.button(f"🗑️ Delete Entire Workout", key=f"delete_workout_{i}"):
                st.session_state.delete_workout_idx = i
                st.session_state.safe_delete_ran = False
                st.rerun()

            if edited:
                save_all_workouts(workouts)  # ✅ FIXED
                st.success("Edits saved!")

# --- In-Progress Management ---
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
