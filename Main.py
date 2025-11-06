import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO

# -----------------------------------
#  Genetic Algorithm Simulation
# -----------------------------------
def run_genetic_algorithm_with_data(co_r, mut_r, data, program_col):
    """
    Simulate a GA that selects the best program for each hour
    based on modified ratings and random variation.
    """
    hour_cols = [col for col in data.columns if "Modified Hour" in col or "Hour" in col]
    schedule = []

    for hour in hour_cols:
        # Add random variation based on mutation rate
        data["Score"] = data[hour] + np.random.uniform(-mut_r, mut_r, len(data))
        best_row = data.loc[data["Score"].idxmax()]

        schedule.append({
            "Hour": hour.replace("Modified ", ""),
            "Program": best_row[program_col],
            "Fitness Score": round(best_row[hour], 2)
        })

    return pd.DataFrame(schedule)


# -----------------------------------
#  Load Dataset
# -----------------------------------
st.title("🎬 Genetic Algorithm Scheduler – Multiple Trials (GitHub Data)")

file_path = "program_ratings.csv"
data = pd.read_csv(file_path)
st.success(f"✅ Dataset loaded successfully from: {file_path}")

# -----------------------------------
#  Detect Program Column Automatically
# -----------------------------------
possible_cols = [col for col in data.columns if "program" in col.lower()]
if possible_cols:
    program_col = possible_cols[0]
    st.info(f"✅ Automatically detected Program column: *{program_col}*")
else:
    st.error("❌ Could not detect a 'Program' column in the dataset.")
    st.stop()


# -----------------------------------
#  Parameter Settings for 3 Trials (Improved Layout)
# -----------------------------------
st.subheader("⚙️ Set Parameters for Each Trial")

# Tabs for 3 trials
tab1, tab2, tab3 = st.tabs(["🧪 Trial 1", "🧩 Trial 2", "🔥 Trial 3"])

with tab1:
    st.markdown(
        """
        <h4 style="color:#0d47a1;">Trial 1 Parameters</h4>
        <p style="color:gray;">Default settings emphasize exploration with a higher crossover rate.</p>
        """,
        unsafe_allow_html=True,
    )
    co_r1 = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8, 0.01, key="co_r1")
    mut_r1 = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, 0.01, key="mut_r1")
    st.markdown("<hr>", unsafe_allow_html=True)

with tab2:
    st.markdown(
        """
        <h4 style="color:#1b5e20;">Trial 2 Parameters</h4>
        <p style="color:gray;">Balanced configuration for crossover and mutation dynamics.</p>
        """,
        unsafe_allow_html=True,
    )
    co_r2 = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.6, 0.01, key="co_r2")
    mut_r2 = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.03, 0.01, key="mut_r2")
    st.markdown("<hr>", unsafe_allow_html=True)

with tab3:
    st.markdown(
        """
        <h4 style="color:#e65100;">Trial 3 Parameters</h4>
        <p style="color:gray;">Focused on mutation diversity with lower crossover emphasis.</p>
        """,
        unsafe_allow_html=True,
    )
    co_r3 = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.4, 0.01, key="co_r3")
    mut_r3 = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.04, 0.01, key="mut_r3")
    st.markdown("<hr>", unsafe_allow_html=True)


# -----------------------------------
#  Run All Trials
# -----------------------------------
if st.button("🚀 Run All Trials"):
    st.info("Running all 3 genetic algorithm trials...")

    trials = [
        ("Trial 1", co_r1, mut_r1, "#e3f2fd"),
        ("Trial 2", co_r2, mut_r2, "#e8f5e9"),
        ("Trial 3", co_r3, mut_r3, "#fff3e0"),
    ]

    for name, co_r, mut_r, color in trials:
        with st.container():
            st.markdown(
                f"""
                <div style="background-color:{color}; padding:15px; border-radius:10px;">
                    <h3 style="color:#424242;">{name}</h3>
                    <p><b>Crossover Rate (CO_R):</b> {co_r} &nbsp;&nbsp; | &nbsp;&nbsp;
                       <b>Mutation Rate (MUT_R):</b> {mut_r}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Run the GA
            schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data.copy(), program_col)

            # Show table
            st.dataframe(schedule_df, use_container_width=True)

            # Summary
            total_fitness = schedule_df["Fitness Score"].sum()
            st.success(f"🎯 Total Fitness Score: **{total_fitness:.2f}**")
            st.markdown("---")
