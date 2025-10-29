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
st.title("🎧 Listening & Mood Patterns by Age and Listening Time")

st.markdown("""
Explore how **listening time** and **favorite genres** relate to **mental health** across **different age groups**.
""")

# ---------------------------
# Data Cleaning
# ---------------------------
# Keep only necessary columns
columns_needed = [
    "Age",
    "Primary streaming service",
    "Hours per day",
    "Fav genre",
    "Anxiety",
    "Depression",
    "Insomnia",
    "OCD"
]

df = df[columns_needed].copy()

# Convert numeric columns
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Hours per day"] = pd.to_numeric(df["Hours per day"], errors="coerce")
df["Anxiety"] = pd.to_numeric(df["Anxiety"], errors="coerce")
df["Depression"] = pd.to_numeric(df["Depression"], errors="coerce")
df["Insomnia"] = pd.to_numeric(df["Insomnia"], errors="coerce")
df["OCD"] = pd.to_numeric(df["OCD"], errors="coerce")

# Drop rows with missing key data
df = df.dropna(subset=["Age", "Hours per day", "Fav genre"])

# Compute average mental health score
df["Mental_Health_Score"] = df[["Anxiety", "Depression", "Insomnia", "OCD"]].mean(axis=1)

# ---------------------------
# Age Group Binning
# ---------------------------
def categorize_age(age):
    if age < 20:
        return "Teen (13–19)"
    elif age < 30:
        return "Young Adult (20–29)"
    elif age < 45:
        return "Adult (30–44)"
    elif age < 60:
        return "Middle Age (45–59)"
    else:
        return "Senior (60+)"

df["Age_Group"] = df["Age"].apply(categorize_age)

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("🔧 Filters")

# Age group dropdown
age_group = st.sidebar.selectbox(
    "Select Age Group",
    options=sorted(df["Age_Group"].unique())
)

# Hours range slider
hours_range = st.sidebar.slider(
    "Select Listening Hours Range",
    float(df["Hours per day"].min()),
    float(df["Hours per day"].max()),
    (float(df["Hours per day"].min()), float(df["Hours per day"].max()))
)

# Genre multiselect
genres = st.sidebar.multiselect(
    "Select Favorite Genres",
    options=sorted(df["Fav genre"].dropna().unique()),
    default=list(df["Fav genre"].dropna().unique())[:5]
)

# ---------------------------
# Filter data
# ---------------------------
filtered = df[
    (df["Age_Group"] == age_group) &
    (df["Hours per day"].between(hours_range[0], hours_range[1])) &
    (df["Fav genre"].isin(genres))
].copy()

# Bin hours for clarity
filtered["Hours_bin"] = pd.cut(filtered["Hours per day"], bins=5, precision=0)
filtered["Hours_bin"] = filtered["Hours_bin"].astype(str)

# Group by and compute mean
grouped = (
    filtered.groupby(["Fav genre", "Hours_bin"])["Mental_Health_Score"]
    .mean()
    .reset_index()
)

# ---------------------------
# Plot heatmap
# ---------------------------
if not grouped.empty:
    fig = px.density_heatmap(
        grouped,
        x="Hours_bin",
        y="Fav genre",
        z="Mental_Health_Score",
        color_continuous_scale="RdYlBu_r",
        title=f"Average Mental Health by Genre and Listening Hours ({age_group})"
    )
    fig.update_layout(height=600, xaxis_title="Listening Hours (binned)", yaxis_title="Favorite Genre")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

# ---------------------------
# Research Question
# ---------------------------
st.markdown("---")
st.subheader("🧠 Research Question")
st.markdown("""
**How do different listening durations and favorite music genres relate to mental health across age groups?**
""")
