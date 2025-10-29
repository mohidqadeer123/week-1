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


# 3D map
file_path = "https://raw.githubusercontent.com/mohidqadeer123/week-1/refs/heads/main/Data_Science_Survey.csv"
df = pd.read_csv(file_path)

# Clean and convert
df = df.rename(columns=lambda x: x.strip())
df_clean = df.dropna(subset=['Age', 'Hours per day', 'Fav genre', 'Anxiety', 'Depression', 'Insomnia'])

for col in ['Age', 'Hours per day', 'Anxiety', 'Depression', 'Insomnia']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🎧 3D Music & Mental Health Explorer")
st.markdown("""
Explore how **Age**, **Listening Hours**, and **Music Genre** relate to  
different **mental health conditions** such as *Anxiety*, *Depression*, and *Insomnia*.
""")

# Sidebar controls
st.sidebar.header("🎛️ Filters")

# Age range slider
age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=10,
    max_value=70,
    value=(15, 40),
    step=5
)

# Hours per day slider
hours_range = st.sidebar.slider(
    "Listening Hours per Day",
    min_value=0.0,
    max_value=10.0,
    value=(1.0, 5.0),
    step=0.5
)

# Genre dropdown
genre_options = ['All'] + sorted(df_clean['Fav genre'].dropna().unique().tolist())
genre = st.sidebar.selectbox("Select Genre", genre_options)

# Metric dropdown
metric_options = ['Anxiety', 'Depression', 'Insomnia']
metric = st.sidebar.selectbox("Select Mental Health Metric", metric_options)

# ---------------------------
# Filter Data
# ---------------------------
filtered = df_clean[
    (df_clean['Age'].between(age_range[0], age_range[1])) &
    (df_clean['Hours per day'].between(hours_range[0], hours_range[1]))
]

if genre != 'All':
    filtered = filtered[filtered['Fav genre'] == genre]

# ---------------------------
# Plot
# ---------------------------
if filtered.empty:
    st.warning("⚠️ No data matches the selected filters.")
else:
    fig = px.scatter_3d(
        filtered,
        x='Age',
        y='Hours per day',
        z=metric,
        color='Fav genre',
        size='Depression',  # example secondary variable
        hover_data=['Primary streaming service', 'Music effects'],
        title=f"{metric} Levels by Age, Genre, and Listening Hours",
        opacity=0.7,
        color_continuous_scale="RdYlBu"
    )
    fig.update_traces(marker=dict(symbol='circle', line=dict(width=0)))
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Research Question
# ---------------------------
st.markdown("---")
st.subheader("🧠 Research Question")
st.markdown(f"""
**How do Age, Listening Hours, and Music Genre relate to {metric.lower()} levels?**  
Use the sidebar filters to explore different trends interactively.
""")
