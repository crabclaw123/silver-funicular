import streamlit as st
import pandas as pd
from data_handler import load_workouts
from collections import defaultdict


def tonnage_tracker():
    st.subheader("📊 Tonnage Tracker")

    workouts = load_workouts()

    if not workouts:
        st.info("No workouts logged yet.")
        return

    # Step 1: Flatten workout data
    tonnage_data = []
    for entry in workouts:
        date = entry.get("date")
        for ex in entry.get("exercises", []):
            name = ex.get("exercise", "Unknown")
            sets = ex.get("sets", [])
            total_tonnage = sum(s["weight"] * s["reps"] for s in sets)
            tonnage_data.append({
                "date": date,
                "exercise": name,
                "tonnage": total_tonnage
            })

    # Step 2: Convert to DataFrame
    df = pd.DataFrame(tonnage_data)
    if df.empty:
        st.info("No set data found in logged workouts.")
        return

    # Step 3: Select exercise to view tonnage trend
    exercise_list = sorted(df["exercise"].unique())
    selected_exercise = st.selectbox("Select Exercise", exercise_list)

    df_filtered = df[df["exercise"] == selected_exercise].copy()
    df_filtered["date"] = pd.to_datetime(df_filtered["date"])
    df_filtered = df_filtered.sort_values("date")

    # Step 4: Show tonnage table and chart
    st.markdown(f"### Tonnage History for: `{selected_exercise}`")
    st.dataframe(df_filtered.rename(columns={"date": "Date", "tonnage": "Total Tonnage"}), use_container_width=True)

    st.line_chart(df_filtered.set_index("date")["tonnage"], use_container_width=True)

    # Step 5: Show % change
    if len(df_filtered) >= 2:
        latest = df_filtered.iloc[-1]["tonnage"]
        previous = df_filtered.iloc[-2]["tonnage"]
        change = latest - previous
        percent = (change / previous) * 100 if previous else 0
        delta = f"(+{percent:.1f}% increase)" if change > 0 else f"({percent:.1f}% decrease)"
        st.success(f"Latest tonnage: `{latest}` lbs — {delta}")
