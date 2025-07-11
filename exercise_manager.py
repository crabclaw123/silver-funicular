# --- exercise_manager.py ---
import streamlit as st
import json
import os

EXERCISE_FILE = "saved_exercises.json"

def load_saved_exercises():
    if not os.path.exists(EXERCISE_FILE):
        return []
    with open(EXERCISE_FILE, "r") as f:
        return json.load(f)

def save_saved_exercises(data):
    with open(EXERCISE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def manage_saved_exercises():
    st.subheader("📘 Saved Exercise Manager")

    saved_exercises = load_saved_exercises()

    # Show all saved exercises with edit/delete options
    for i, ex in enumerate(saved_exercises):
        with st.expander(f"{ex['name']} ({ex['muscle_group']})"):
            cols = st.columns([2, 2, 1, 1])
            name = cols[0].text_input("Exercise Name", ex["name"], key=f"name_{i}")
            muscle = cols[1].selectbox("Muscle Group", [
                "Chest", "Back", "Shoulders", "Arms", "Biceps", "Triceps", "Quads",
                "Hamstrings", "Glutes", "Calves", "Forearms", "Core", "Full Body", "Other"
            ], index=[
                "Chest", "Back", "Shoulders", "Arms", "Biceps", "Triceps", "Quads",
                "Hamstrings", "Glutes", "Calves", "Forearms", "Core", "Full Body", "Other"
            ].index(ex["muscle_group"]), key=f"muscle_{i}")

            equipment = cols[2].selectbox("Equipment", [
                "Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Smith Machine", "Other"
            ], index=[
                "Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Smith Machine", "Other"
            ].index(ex["equipment"]), key=f"equipment_{i}")

            favorite = cols[3].checkbox("⭐ Favorite", value=ex.get("favorite", False), key=f"fav_{i}")

            tags = st.text_input("Tags (comma separated)", ", ".join(ex.get("tags", [])), key=f"tags_{i}")

            if st.button("💾 Save Changes", key=f"save_{i}"):
                saved_exercises[i] = {
                    "name": name,
                    "muscle_group": muscle,
                    "equipment": equipment,
                    "tags": [t.strip() for t in tags.split(",") if t.strip()],
                    "favorite": favorite
                }
                save_saved_exercises(saved_exercises)
                st.success("Exercise updated!")
                st.rerun()

            if st.button("🗑️ Delete", key=f"delete_{i}"):
                saved_exercises.pop(i)
                save_saved_exercises(saved_exercises)
                st.warning("Exercise deleted")
                st.rerun()

    st.divider()
    st.subheader("➕ Add New Exercise")

    new_name = st.text_input("New Exercise Name")
    new_muscle = st.selectbox("Muscle Group", [
        "Chest", "Back", "Shoulders", "Arms", "Biceps", "Triceps", "Quads",
        "Hamstrings", "Glutes", "Calves", "Forearms", "Core", "Full Body", "Other"
    ])
    new_equipment = st.selectbox("Equipment", ["Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Smith Machine", "Other"])
    new_tags = st.text_input("Tags (comma separated)")
    new_favorite = st.checkbox("⭐ Mark as Favorite")

    if st.button("➕ Add Exercise"):
        saved_exercises.append({
            "name": new_name,
            "muscle_group": new_muscle,
            "equipment": new_equipment,
            "tags": [t.strip() for t in new_tags.split(",") if t.strip()],
            "favorite": new_favorite
        })
        save_saved_exercises(saved_exercises)
        st.success(f"Added {new_name} to library!")
        st.rerun()
