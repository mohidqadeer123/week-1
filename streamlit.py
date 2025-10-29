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
Explore how **listening time and music genres** relate to **mental health scores**,  
grouped by **age categories**.
""")

# Expected columns check
expected_cols = ["Age", "Genre", "Hours_per_day", "Mental_health_score"]
missing_cols = [col for col in expected_cols if col not in df.columns]

if missing_cols:
    st.error(f"❌ Missing expected columns in dataset: {', '.join(missing_cols)}")
    st.stop()

# Convert types
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Hours_per_day"] = pd.to_numeric(df["Hours_per_day"], errors="coerce")
df["Mental_health_score"] = pd.to_numeric(df["Mental_health_score"], errors="coerce")
df = df.dropna(subset=["Age", "Hours_per_day", "Genre", "Mental_health_score"])

# Define Age Groups
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

# Sidebar filters
st.sidebar.header("Filters")
# Age group dropdown
age_group = st.sidebar.selectbox(
    "Select Age Group",
    options=df["Age_Group"].unique()
)
# Hours range slider
hours_range = st.sidebar.slider(
    "Select Listening Hours Range",
    float(df["Hours_per_day"].min()),
    float(df["Hours_per_day"].max()),
    (float(df["Hours_per_day"].min()), float(df["Hours_per_day"].max()))
)

# Genre multiselect
genres = st.sidebar.multiselect(
    "Select Genres",
    options=df["Genre"].unique(),
    default=list(df["Genre"].unique())
)
# Filter data
filtered = df[
    (df["Age_Group"] == age_group) &
    (df["Hours_per_day"].between(hours_range[0], hours_range[1])) &
    (df["Genre"].isin(genres))
].copy()

# Bin hours for x-axis clarity
filtered["Hours_bin"] = pd.cut(filtered["Hours_per_day"], bins=5, precision=0)
filtered["Hours_bin"] = filtered["Hours_bin"].astype(str)

# Group and average
grouped = (
    filtered.groupby(["Genre", "Hours_bin"])["Mental_health_score"]
    .mean()
    .reset_index()
)


# Plot heatmap
if not grouped.empty:
    fig = px.density_heatmap(
        grouped,
        x="Hours_bin",
        y="Genre",
        z="Mental_health_score",
        color_continuous_scale="Viridis",
        title=f"Average Mental Health by Genre and Listening Hours ({age_group})"
    )
    fig.update_layout(height=600, xaxis_title="Listening Hours (binned)", yaxis_title="Genre")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")


# Research Question

st.markdown("---")
st.subheader("🧠 Research Question")
st.markdown("""
**How does listening time and genre preference differ across age groups,  
and how might these factors relate to mental health?**
""")
