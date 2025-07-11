import streamlit as st
import json
import os
from datetime import datetime
from data_handler import load_workouts, save_all_workouts
from exercise_manager import load_saved_exercises

WORKOUT_LOG_FILE = "workout_log.json"
IN_PROGRESS_FILE = "in_progress_workout.json"


def display_workout_history():
    if "delete_workout_idx" not in st.session_state:
        st.session_state.delete_workout_idx = None
    if "delete_exercise" not in st.session_state:
        st.session_state.delete_exercise = None
    if "safe_delete_ran" not in st.session_state:
        st.session_state.safe_delete_ran = False

    workouts = load_workouts()

    if not st.session_state.safe_delete_ran:
        if st.session_state.delete_exercise:
            i, j = st.session_state.delete_exercise
            try:
                workouts[i]["exercises"].pop(j)
                save_all_workouts(workouts)
            except IndexError:
                st.warning("Couldn't delete exercise. Index out of range.")
            st.session_state.delete_exercise = None
            st.session_state.safe_delete_ran = True
            st.rerun()

        if st.session_state.delete_workout_idx is not None:
            try:
                workouts.pop(st.session_state.delete_workout_idx)
                save_all_workouts(workouts)
            except IndexError:
                st.warning("Couldn't delete workout. Index out of range.")
            st.session_state.delete_workout_idx = None
            st.session_state.safe_delete_ran = True
            st.rerun()

    st.subheader("📜 Workout History")
    if not workouts:
        st.info("No workouts logged yet.")
        return

    saved_exercises = load_saved_exercises()
    muscle_tag_options = sorted(set(tag for ex in saved_exercises for tag in ex.get("tags", [])))
    if not muscle_tag_options:
        muscle_tag_options = [
            "Lateral Head", "Long Head", "Medial Head",
            "Upper Chest", "Lower Chest",
            "Anterior Delts", "Lateral Delts", "Rear Delts", "Brachioradialis",
            "Vastus Lateralis", "Vastus Medialis", "Glute Med", "Glute Max",
            "Biceps Long Head", "Biceps Short Head", "Latissimus Dorsi",
            "Hamstrings", "Quads", "Calves", "Core"
    ]


    for i, entry in enumerate(workouts):
        if not isinstance(entry, dict):
            continue

        with st.expander(f"{entry['date']} — {entry.get('type', 'Unknown')}"):
            edited = False

            new_date = st.date_input("Edit Date", value=datetime.strptime(entry['date'], "%Y-%m-%d").date(), key=f"edit_date_{i}")
            new_date_str = new_date.strftime("%Y-%m-%d")
            if new_date_str != entry["date"]:
                entry["date"] = new_date_str
                edited = True

            for j, exercise in enumerate(entry.get("exercises", [])):
                st.markdown(f"### 🏋️ Exercise {j+1}")

                ex_name = st.text_input("Exercise Name", value=exercise["exercise"], key=f"ex_name_{i}_{j}")
                muscle_group = st.selectbox("Muscle Group", ["Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves", "Other"], index=0 if exercise.get("muscle_group") not in ["Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves"] else ["Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves"].index(exercise["muscle_group"]), key=f"muscle_{i}_{j}")
                equipment = st.selectbox("Equipment", ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Smith Machine", "Other"], index=0 if exercise.get("equipment") not in ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"] else ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"].index(exercise["equipment"]), key=f"equip_{i}_{j}")
                default_tags = [t for t in exercise.get("tags", []) if t in muscle_tag_options]
                tags = st.multiselect("Tags", muscle_tag_options, default=default_tags, key=f"tags_{i}_{j}")

                sets = []
                for s_idx, s in enumerate(exercise.get("sets", [])):
                    cols = st.columns(2)
                    with cols[0]:
                        weight = st.number_input("Weight (lbs)", min_value=0.0, max_value=2000.0, step=0.5, value=s["weight"], format="%.1f", key=f"weight_{i}_{j}_{s_idx}")
                    with cols[1]:
                        reps = st.number_input("Reps", min_value=1, max_value=100, step=1, value=s["reps"], key=f"reps_{i}_{j}_{s_idx}")
                    sets.append({"weight": weight, "reps": reps})

                exercise.update({
                    "exercise": ex_name,
                    "muscle_group": muscle_group,
                    "equipment": equipment,
                    "tags": tags,
                    "sets": sets
                })
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
                save_all_workouts(workouts)
                st.success("Changes saved!")
