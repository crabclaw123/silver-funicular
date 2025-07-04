import streamlit as st
from data_handler import load_workouts
import json
from pathlib import Path

WORKOUT_FILE = Path("workout_log.json")

def save_all_workouts(data):
    with open(WORKOUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def display_workout_history():
    st.subheader("📜 Workout History")

    workouts = load_workouts()

    if not workouts:
        st.info("No workouts logged yet.")
        return

    for i in reversed(range(len(workouts))):
        entry = workouts[i]
        workout_type = entry.get("type", "Not Tagged")
        st.write(f"### {entry['date']} — *{workout_type} Focus*")

        for j, exercise in enumerate(entry.get("exercises", [])):
            st.markdown(f"**{exercise['muscle_group']} - {exercise['exercise']}**")
            for k, s in enumerate(exercise["sets"]):
                st.write(f"Set {k + 1}: {s['reps']} reps @ {s['weight']} lbs")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🗑️ Remove This Exercise", key=f"remove_ex_{i}_{j}"):
                    workouts[i]["exercises"].pop(j)
                    if len(workouts[i]["exercises"]) == 0:
                        workouts.pop(i)
                    save_all_workouts(workouts)
                    st.rerun()

            with col2:
                if st.button(f"✏️ Edit", key=f"edit_ex_{i}_{j}"):
                    st.session_state[f"editing_{i}_{j}"] = True

            if st.session_state.get(f"editing_{i}_{j}", False):
                with st.form(f"edit_form_{i}_{j}"):
                    st.write("**Edit Exercise**")

                    new_muscle = st.selectbox("Muscle Group", [
                        "Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves"
                    ], index=["Chest", "Back", "Legs", "Shoulders", "Arms", "Glutes", "Core", "Forearms", "Calves"].index(exercise["muscle_group"]))

                    new_name = st.text_input("Exercise Name", value=exercise["exercise"])

                    new_sets = []
                    for s_idx, s in enumerate(exercise["sets"]):
                        cols = st.columns(2)
                        with cols[0]:
                            weight = st.number_input("Weight (lbs)", min_value=0.0, max_value=2000.0, step=0.5,
                         value=float(s["weight"]), format="%.1f", key=f"edit_weight_{i}_{j}_{s_idx}")

                        with cols[1]:
                            reps = st.number_input("Reps", min_value=1, max_value=100, step=1,
                                                   value=s["reps"], key=f"edit_reps_{i}_{j}_{s_idx}")
                        new_sets.append({"reps": reps, "weight": weight})

                    submit = st.form_submit_button("✅ Save Changes")
                    if submit:
                        workouts[i]["exercises"][j] = {
                            "muscle_group": new_muscle,
                            "exercise": new_name,
                            "sets": new_sets
                        }
                        save_all_workouts(workouts)
                        st.success("Exercise updated successfully.")
                        del st.session_state[f"editing_{i}_{j}"]
                        st.rerun()