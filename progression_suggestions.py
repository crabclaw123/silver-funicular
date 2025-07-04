# progression.py
import streamlit as st

def progression_engine(exercise_name):
    st.subheader("📈 Progression Suggestions")

    # Basic muscle group logic for overload recommendation
    if any(leg in exercise_name.lower() for leg in ["squat", "leg", "deadlift", "rdl", "lunge"]):
        st.markdown("- 🔼 **Lower body movement** detected. Aim to increase weight by **5–10%** if all sets were completed.")
    else:
        st.markdown("- 🔼 **Upper body movement** detected. Aim to increase weight by **2.5–5%** if all sets were completed.")

    # Set and rep guidance
    st.markdown("- ✅ If you hit all sets and reps with clean form: **add 1 set** or slightly increase weight.")
    st.markdown("- ⚠️ If you struggled or failed a set: consider **maintaining or slightly reducing** volume next session.")

    # Recovery consideration
    st.markdown("- 💤 If you're feeling unusually fatigued: take a lighter session or deload after **4–6 weeks** of progressive overload.")

    # Visual suggestion (optional colors / emojis)
    st.markdown("\n**Progression Readiness:** 🟢 Optimal | 🟠 Moderate | 🔴 Needs Recovery")
