import streamlit as st
from data_handler import save_workout, load_in_progress_workout, save_in_progress_workout, clear_in_progress_workout
import datetime
from exercise_manager import load_saved_exercises, save_saved_exercises

def workout_logger():
    st.subheader("📋 Log Your Workout (Multiple Exercises)")

    if "today_workout" not in st.session_state:
        st.session_state.today_workout = load_in_progress_workout()

    if "workout_logged" not in st.session_state:
        st.session_state.workout_logged = False

    if "log_triggered" not in st.session_state:
        st.session_state.log_triggered = False

    date = st.date_input("Workout Date", value=datetime.date.today())
    workout_type = st.selectbox("Workout Focus", ["Volume", "Intensity", "Mixed"])

    st.markdown("### ➕ Add an Exercise")

    saved_exercises = load_saved_exercises()
    exercise_options = [ex["name"] for ex in saved_exercises]
    selected_name = st.selectbox("Select Exercise", exercise_options + ["➕ Create New"], key="exercise_select")

    # Default fallbacks
    exercise_name = ""
    muscle_group = "Other"
    equipment = "Other"

    if selected_name == "➕ Create New":
        exercise_name = st.text_input("New Exercise Name", key="new_ex_name")
        muscle_group = st.selectbox("Muscle Group", [
            "Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves", "Other"
        ], key="new_muscle")
        equipment = st.selectbox("Equipment Used", [
            "Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"
        ], key="new_equipment")

        if st.button("💾 Save Exercise for Later (Don't Log)"):
            new_ex = {
                "name": exercise_name.strip(),
                "muscle_group": muscle_group,
                "equipment": equipment,
                "tags": [],
                "favorite": False
            }
            if new_ex["name"] and new_ex["name"] not in exercise_options:
                saved_exercises.append(new_ex)
                save_saved_exercises(saved_exercises)
                st.success(f"Saved '{exercise_name}' to your exercise library!")
                st.rerun()
            else:
                st.error("Please enter a unique and valid exercise name.")

    else:
        selected_ex = next((ex for ex in saved_exercises if ex["name"] == selected_name), None)
        if selected_ex:
            exercise_name = selected_ex["name"]
            muscle_group = selected_ex.get("muscle_group", "Other")
            equipment = selected_ex.get("equipment", "Other")

    num_sets = st.number_input("Number of Sets", min_value=1, max_value=10, step=1, key="num_sets")
    temp_sets = []
    st.markdown("### 🏋️ Log Sets")
    for i in range(num_sets):
        st.markdown(f"**Set {i + 1}**")
        cols = st.columns(2)
        with cols[0]:
            weight = st.number_input("Weight (lbs)", min_value=0.0, max_value=2000.0, step=0.5, key=f"weight_{i}", format="%.1f")
        with cols[1]:
            reps = st.number_input("Reps", min_value=1, max_value=100, step=1, key=f"reps_{i}")
        temp_sets.append({"reps": reps, "weight": weight})

    if st.button("➕ Add Exercise to Workout"):
        if exercise_name.strip():
            new_ex = {
                "muscle_group": muscle_group,
                "exercise": exercise_name.strip(),
                "equipment": equipment,
                "sets": temp_sets
            }
            st.session_state.today_workout.append(new_ex)
            save_in_progress_workout(st.session_state.today_workout)
            st.success(f"Added: {exercise_name} with {len(temp_sets)} sets.")
            st.session_state.workout_logged = False
        else:
            st.error("Please enter a valid exercise name.")

    if st.session_state.today_workout:
        st.markdown("### ✅ Current Workout Summary")
        for idx, ex in enumerate(st.session_state.today_workout):
            st.markdown(f"**{idx + 1}. {ex['muscle_group']} • {ex['exercise']} • {len(ex['sets'])} sets**")
            if st.button(f"🗑️ Remove Exercise {idx + 1}", key=f"delete_{idx}"):
                st.session_state.today_workout.pop(idx)
                save_in_progress_workout(st.session_state.today_workout)
                st.rerun()

        if st.button("💾 Log Entire Workout") and not st.session_state.workout_logged:
            st.session_state.log_triggered = True
            st.rerun()

    if st.session_state.log_triggered and not st.session_state.workout_logged:
        workout_entry = {
            "date": str(date),
            "type": workout_type,
            "exercises": st.session_state.today_workout
        }
        save_workout(workout_entry)
        clear_in_progress_workout()
        st.session_state.today_workout = []
        st.session_state.workout_logged = True
        st.session_state.log_triggered = False
        st.success("Workout successfully logged!")
