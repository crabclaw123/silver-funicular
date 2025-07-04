import streamlit as st
from data_handler import save_workout, load_in_progress_workout, save_in_progress_workout, clear_in_progress_workout
import datetime

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
    muscle_group = st.selectbox("Muscle Group", [
        "Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves"
    ])
    exercise_name = st.text_input("Exercise Name")
    equipment = st.selectbox("Equipment Used", ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Other"])
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

    # Only log once after rerun
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

