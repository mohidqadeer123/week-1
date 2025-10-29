import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Music Genre and Mental Health Analysis")

file_path = r"https://raw.githubusercontent.com/mohidqadeer123/week-1/refs/heads/main/Data_Science_Survey.csv"
df = pd.read_csv(file_path)

cols = ["Fav genre", "Anxiety", "Depression", "Insomnia"]
subset = df[cols].dropna()

# Compute mean values per genre
genre_means = subset.groupby("Fav genre")[["Anxiety", "Depression", "Insomnia"]].mean()

# Also compute a combined score
genre_means["avg_score"] = genre_means.mean(axis=1)

# Reset index for plotting
genre_means = genre_means.reset_index()

# Sort by avg_score
genre_means = genre_means.sort_values("avg_score")

st.subheader("Average Mental Health Scores by Music Genre")
st.dataframe(genre_means)

fig = px.bar(
    genre_means,
    x="Fav genre",
    y=["Anxiety", "Depression", "Insomnia"],
    barmode="group",
    title="Average Mental Health Scores by Music Genre",
    labels={"value": "Average Score", "Fav genre": "Music Genre"}
)

fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)


# Heatmap
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Load Data
# ---------------------------
file_path = r"https://raw.githubusercontent.com/mohidqadeer123/week-1/refs/heads/main/Data_Science_Survey.csv"
df = pd.read_csv(file_path)

st.title("🎧 Mental Health Patterns by Age and Listening Habits")

st.markdown("""
Visualize how **Age** and **Listening Hours per Day** relate to **mental health conditions**  
(such as Anxiety, Depression, Insomnia, or OCD).
""")

# ---------------------------
# Data Cleaning
# ---------------------------
df = df.rename(columns=lambda x: x.strip())

# Convert numeric columns safely
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Hours per day"] = pd.to_numeric(df["Hours per day"], errors="coerce")
for col in ["Anxiety", "Depression", "Insomnia", "OCD"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Age", "Hours per day"])

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("🎛️ Controls")

genre = st.sidebar.selectbox(
    "Select Favorite Genre",
    options=sorted(df["Fav genre"].dropna().unique())
)

metric = st.sidebar.selectbox(
    "Select Mental Health Condition",
    ["Anxiety", "Depression", "Insomnia", "OCD"]
)

# Bin Age and Hours for heatmap
age_bins = [10, 20, 30, 40, 50, 60, 70]
hour_bins = [0, 1, 2, 3, 4, 5, 6]

df_filtered = df[df["Fav genre"] == genre].copy()
df_filtered["Age_bin"] = pd.cut(df_filtered["Age"], bins=age_bins, right=False)
df_filtered["Hours_bin"] = pd.cut(df_filtered["Hours per day"], bins=hour_bins, right=False)

# Group and calculate average condition score
grouped = (
    df_filtered.groupby(["Age_bin", "Hours_bin"])[metric]
    .mean()
    .reset_index()
)

# Convert bins to readable string ranges
grouped["Age_bin"] = grouped["Age_bin"].astype(str)
grouped["Hours_bin"] = grouped["Hours_bin"].astype(str)

# ---------------------------
# Heatmap Plot
# ---------------------------
if not grouped.empty:
    fig = px.density_heatmap(
        grouped,
        x="Hours_bin",
        y="Age_bin",
        z=metric,
        color_continuous_scale="RdYlBu_r",
        title=f"{metric} Levels by Age and Listening Hours ({genre})"
    )
    fig.update_layout(
        height=600,
        xaxis_title="Listening Hours (binned)",
        yaxis_title="Age (binned)",
        coloraxis_colorbar_title=f"{metric} Level"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data available for the selected genre or bins.")

# ---------------------------
# Research Question
# ---------------------------
st.markdown("---")
st.subheader("🧠 Research Question")
st.markdown(f"""
**How does the number of hours spent listening to {genre} music relate  
to {metric.lower()} levels across different age groups?**
""")
