import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta
from data_handler import load_workouts


def tonnage_comparison():
    st.subheader("📈 Tonnage Comparison")

    workouts = load_workouts()
    if not workouts:
        st.info("No workouts logged yet.")
        return

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
                "tonnage": total_tonnage,
                "sets": sets
            })

    df = pd.DataFrame(tonnage_data)
    if df.empty:
        st.info("No tonnage data available.")
        return

    df["date"] = pd.to_datetime(df["date"])

    exercise_list = sorted(df["exercise"].unique())
    selected_exercise = st.selectbox("Select Exercise to Compare", exercise_list)
    time_range = st.selectbox("Time Range", ["Past 30 Days", "Past 3 Months", "Past Year", "All Time"])

    today = datetime.today()
    if time_range == "Past 30 Days":
        date_cutoff = today - timedelta(days=30)
    elif time_range == "Past 3 Months":
        date_cutoff = today - timedelta(days=90)
    elif time_range == "Past Year":
        date_cutoff = today - timedelta(days=365)
    else:
        date_cutoff = datetime.strptime("1900-01-01", "%Y-%m-%d")

    df_ex = df[df["exercise"] == selected_exercise].copy()
    df_ex = df_ex[df_ex["date"] >= date_cutoff]

    if df_ex.empty:
        st.warning("No workouts for this exercise in the selected time range.")
        return

    df_ex = df_ex.sort_values("date")
    df_ex["Week"] = df_ex["date"].dt.to_period("W").apply(lambda r: r.start_time)

    st.line_chart(df_ex.set_index("date")["tonnage"], use_container_width=True)
    st.markdown(f"### 📊 Tonnage Data for `{selected_exercise}`")
    st.dataframe(df_ex[["date", "tonnage"]].rename(columns={"date": "Date", "tonnage": "Tonnage"}), use_container_width=True)

    if len(df_ex) >= 2:
        latest = df_ex.iloc[-1]
        latest_tonnage = latest["tonnage"]
        previous_tonnage = df_ex.iloc[-2]["tonnage"]
        change = latest_tonnage - previous_tonnage
        percent = (change / previous_tonnage) * 100 if previous_tonnage else 0
        delta = f"(+{percent:.1f}% increase)" if change > 0 else f"({percent:.1f}% decrease)"
        st.success(f"Latest tonnage: `{latest_tonnage}` lbs — {delta}")

        st.markdown("### 💡 Increase Tonnage Next Time")
        method = st.radio("Select progression method:", ["Increase Reps", "Increase Weight"])

        sets = latest["sets"]
        target_increase = max(1.0, 0.03 * latest_tonnage)  # Default 3% increase

        suggested_sets = []
        total_new_tonnage = 0

        if method == "Increase Reps":
            for s in sets:
                reps = s["reps"]
                weight = s["weight"]
                current_tonnage = reps * weight
                needed = target_increase / len(sets)
                new_reps = math.ceil((current_tonnage + needed) / weight)
                suggested_sets.append(f"{weight:.1f} lbs × {new_reps} reps")
                total_new_tonnage += new_reps * weight

        else:  # Increase Weight
            for s in sets:
                reps = s["reps"]
                weight = s["weight"]
                current_tonnage = reps * weight
                needed = target_increase / len(sets)
                new_weight = weight + (needed / reps)
                new_weight = round(new_weight, 1)
                suggested_sets.append(f"{new_weight:.1f} lbs × {reps} reps")
                total_new_tonnage += new_weight * reps

        st.markdown("#### ✅ Suggested Set Plan:")
        for i, plan in enumerate(suggested_sets):
            st.write(f"Set {i+1}: {plan}")
        st.markdown(f"**Total Tonnage (Projected):** `{total_new_tonnage:.1f}` lbs")
