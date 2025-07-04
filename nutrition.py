import streamlit as st

def nutrition_strategy_tip(phase, goal="maintenance"):
    st.subheader("🍽️ Nutrition Strategy Based on Mesocycle Phase")
    st.write(f"Current phase: **{phase}**")
    if phase == "Accumulation":
        st.info("Slight surplus may support recovery and higher training volume. Focus on carbs and overall calories.")
    elif phase == "Intensification":
        st.info("Slight maintenance or mild surplus. Prioritize protein to support repair and maintain strength.")
    elif phase == "Deload":
        st.info("Lower calories slightly to match reduced training. Keep protein high to preserve muscle.")
    elif phase == "Specialization":
        st.info("Adjust intake based on the focus muscle group's demand. Often higher carb and protein.")
    else:
        st.warning("Phase not recognized.")