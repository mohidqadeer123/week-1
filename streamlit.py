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

# ---------------------------
# Clean and Prepare
# ---------------------------
df = df.rename(columns=lambda x: x.strip())

# Convert numeric columns
for col in ["Age", "Hours per day", "Anxiety", "Depression", "Insomnia", "OCD"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Age", "Hours per day", "Fav genre"])

# Define bins for Age
age_bins = [10, 20, 30, 40, 50, 60, 70]
df["Age_group"] = pd.cut(df["Age"], bins=age_bins, labels=[f"{age_bins[i]}–{age_bins[i+1]}" for i in range(len(age_bins)-1)], right=False)

# ---------------------------
# Streamlit Layout
# ---------------------------
st.title("🎧 3D Heatmap: Music Habits vs Mental Health")

st.markdown("""
Explore how **Age**, **Listening Hours**, and **Music Genre** relate to  
mental health conditions such as *Anxiety*, *Depression*, *Insomnia*, and *OCD*.
""")

# --- Controls ---
st.sidebar.header("🎛️ Filters")

# Age group dropdown
age_group = st.sidebar.selectbox("Select Age Group", options=df["Age_group"].unique())

# Hours slider
hours_range = st.sidebar.slider("Select Listening Hours per Day", 0.0, 6.0, (1.0, 4.0), step=0.5)

# Condition dropdown
condition = st.sidebar.selectbox("Select Condition", ["Anxiety", "Depression", "Insomnia", "OCD"])

# Genre multi-select
genres = st.sidebar.multiselect(
    "Select Favorite Genres",
    options=sorted(df["Fav genre"].dropna().unique()),
    default=["Pop", "Rock", "Hip hop"]
)

# ---------------------------
# Filter Data
# ---------------------------
filtered = df[
    (df["Age_group"] == age_group)
    & (df["Hours per day"].between(hours_range[0], hours_range[1]))
    & (df["Fav genre"].isin(genres))
]

if filtered.empty:
    st.warning("⚠️ No data matches the selected filters.")
    st.stop()

# ---------------------------
# Aggregate by Genre and Hours
# ---------------------------
grouped = (
    filtered.groupby(["Fav genre", "Hours per day"])[condition]
    .mean()
    .reset_index()
)

# ---------------------------
# 3D Heatmap (Surface Plot)
# ---------------------------
fig = px.scatter_3d(
    grouped,
    x="Fav genre",
    y="Hours per day",
    z=condition,
    color=condition,
    color_continuous_scale="RdYlBu_r",
    size_max=15,
    title=f"3D Visualization of {condition} Levels — Age Group {age_group}"
)

fig.update_layout(
    scene=dict(
        xaxis_title="Genre",
        yaxis_title="Listening Hours per Day",
        zaxis_title=f"{condition} Level"
    ),
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Research Question
# ---------------------------
st.markdown("---")
st.subheader("🧠 Research Question")
st.markdown(f"""
**How does the number of listening hours and music genre preference  
relate to {condition.lower()} levels for individuals aged {age_group}?**
""")
