import streamlit as st

def progression_engine(exercise_name):
    st.subheader("📈 Progression Suggestions")
    st.write(f"Based on your last logged session for **{exercise_name}**, aim to:")
    st.write("- Increase weight by 2.5–5 lbs **OR**")
    st.write("- Add 1 rep to your final set **OR**")
    st.write("- Add 1 total set if recovery was good")