import streamlit as st
import pandas as pd
from data_handler import load_workouts
from collections import defaultdict
from datetime import datetime, timedelta
from exercise_manager import load_saved_exercises


def tonnage_tracker():
    st.subheader("📊 Tonnage Tracker")

    workouts = load_workouts()
    if not workouts:
        st.info("No workouts logged yet.")
        return

    # Flatten all sets with metadata for tags and exercises
    tonnage_data = []
    for entry in workouts:
        date = entry.get("date")
        for ex in entry.get("exercises", []):
            sets = ex.get("sets", [])
            tags = ex.get("tags", []) or ["Untagged"]
            exercise_name = ex.get("exercise", "Unknown")
            for s in sets:
                tonnage = s["weight"] * s["reps"]
                tonnage_data.append({
                    "date": date,
                    "exercise": exercise_name,
                    "tonnage": tonnage,
                    "tags": tags
                })

    df = pd.DataFrame(tonnage_data)
    if df.empty:
        st.info("No set data found in logged workouts.")
        return

    df["date"] = pd.to_datetime(df["date"])

    view_mode = st.radio("View Tonnage By:", ["Exercise", "Muscle Tag"])

    if view_mode == "Exercise":
        exercise_list = sorted(df["exercise"].unique())
        selected_exercise = st.selectbox("Select Exercise", exercise_list)
        df_filtered = df[df["exercise"] == selected_exercise].copy()

        st.markdown(f"### Tonnage History for: `{selected_exercise}`")
        summary = df_filtered.groupby("date")["tonnage"].sum().reset_index()
        st.dataframe(summary.rename(columns={"date": "Date", "tonnage": "Total Tonnage"}), use_container_width=True)
        st.line_chart(summary.set_index("date")["tonnage"], use_container_width=True)

        if len(summary) >= 2:
            latest = summary.iloc[-1]["tonnage"]
            previous = summary.iloc[-2]["tonnage"]
            change = latest - previous
            percent = (change / previous) * 100 if previous else 0
            delta = f"(+{percent:.1f}% increase)" if change > 0 else f"({percent:.1f}% decrease)"
            st.success(f"Latest tonnage: `{latest}` lbs — {delta}")

    elif view_mode == "Muscle Tag":
        tag_counts = defaultdict(float)
        for _, row in df.iterrows():
            for tag in row["tags"]:
                tag_counts[tag] += row["tonnage"]

        tag_df = pd.DataFrame(sorted(tag_counts.items(), key=lambda x: -x[1]), columns=["Tag", "Total Tonnage"])
        st.markdown("### 📌 Total Volume by Muscle Tag")
        st.dataframe(tag_df, use_container_width=True)
        st.bar_chart(tag_df.set_index("Tag"), use_container_width=True)

    # Optional breakdown for the current calendar week (Monday to Sunday)
    if st.checkbox("🔍 Show Muscle Tag Breakdown for This Week"):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)
        recent_df = df[(df["date"] >= start_of_week) & (df["date"] <= end_of_week)]

        weekly_breakdown = defaultdict(float)
        for _, row in recent_df.iterrows():
            for tag in row["tags"]:
                weekly_breakdown[tag] += row["tonnage"]

        st.markdown(f"### 🧠 Tag Breakdown — This Week (Mon to Sun)")
        breakdown_df = pd.DataFrame(sorted(weekly_breakdown.items(), key=lambda x: -x[1]), columns=["Tag", "Tonnage"])
        st.dataframe(breakdown_df, use_container_width=True)
        st.bar_chart(breakdown_df.set_index("Tag"), use_container_width=True)
