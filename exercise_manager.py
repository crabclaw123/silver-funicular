# --- exercise_manager.py ---
import streamlit as st
import json
import os

EXERCISE_FILE = "saved_exercises.json"

MUSCLE_GROUPS = [
    "Chest", "Back", "Shoulders", "Arms", "Biceps", "Triceps", "Quads",
    "Hamstrings", "Glutes", "Calves", "Forearms", "Core", "Full Body", "Other"
]

EQUIPMENT_TYPES = [
    "Dumbbell", "Barbell", "Cable", "Machine", "Bodyweight", "Smith Machine", "Other"
]

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

    for i, ex in enumerate(saved_exercises):
        with st.expander(f"{ex['name']} ({ex['muscle_group']})"):
            cols = st.columns([2, 2, 1, 1])
            name = cols[0].text_input("Exercise Name", ex["name"], key=f"name_{i}")

            muscle_index = MUSCLE_GROUPS.index(ex["muscle_group"]) if ex["muscle_group"] in MUSCLE_GROUPS else 0
            muscle = cols[1].selectbox("Muscle Group", MUSCLE_GROUPS, index=muscle_index, key=f"muscle_{i}")

            equipment_index = EQUIPMENT_TYPES.index(ex["equipment"]) if ex["equipment"] in EQUIPMENT_TYPES else 0
            equipment = cols[2].selectbox("Equipment", EQUIPMENT_TYPES, index=equipment_index, key=f"equipment_{i}")

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
    new_muscle = st.selectbox("Muscle Group", MUSCLE_GROUPS)
    new_equipment = st.selectbox("Equipment", EQUIPMENT_TYPES)
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
