import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from movie_data_v2 import MovieData  # Ensure movie_data.py is in the same directory

# Initialize MovieData instance
url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
movie_data = MovieData(url=url)

# Streamlit App Title
st.title("🎬 Movie Data Analysis App")

# Sidebar Section for User Inputs
st.sidebar.header("User Inputs")

# Input for `movie_type` method
N = st.sidebar.number_input("Select number of top genres (N):", min_value=1, max_value=50, value=10, step=1)

# Dropdown for `actor_distributions` gender selection
valid_genders = ["All"] + movie_data.character_df["actor_gender"].dropna().unique().tolist()
selected_gender = st.sidebar.selectbox("Select Gender:", valid_genders)

# Inputs for height range
min_height = st.sidebar.number_input("Minimum Height (meters):", min_value=0.5, max_value=3.0, value=1.5, step=0.1)
max_height = st.sidebar.number_input("Maximum Height (meters):", min_value=0.5, max_value=3.0, value=2.0, step=0.1)

# Ensure min_height is not greater than max_height
if min_height > max_height:
    st.sidebar.error("⚠️ Minimum height must be less than maximum height.")

# ---- PLOTS ----
st.subheader("📊 Movie Genre Distribution")
# Fetch data from movie_type method
movie_genres_df = movie_data.movie_type(N=N)

# Plot histogram of movie types
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(movie_genres_df["Movie_Type"], movie_genres_df["Count"], color="skyblue")
ax.set_xlabel("Count")
ax.set_ylabel("Movie Genre")
ax.set_title(f"Top {N} Most Common Movie Genres")
st.pyplot(fig)

# ---- Plot for `actor_count` method ----
st.subheader("🎭 Actor Count Per Movie")

actor_count_df = movie_data.actor_count()

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(actor_count_df["Number_of_Actors"], actor_count_df["Movie_Count"], color="salmon")
ax2.set_xlabel("Number of Actors")
ax2.set_ylabel("Movie Count")
ax2.set_title("Distribution of Number of Actors Per Movie")
st.pyplot(fig2)

# ---- Plot for `actor_distributions` method ----
st.subheader(f"📈 Actor Height Distribution for {selected_gender}")

actor_height_df = movie_data.actor_distributions(
    gender=selected_gender, min_height=min_height, max_height=max_height
)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.hist(actor_height_df["actor_height_in_meters"].dropna(), bins=30, color="green", edgecolor="black")
ax3.set_xlabel("Height (meters)")
ax3.set_ylabel("Frequency")
ax3.set_title(f"Height Distribution for {selected_gender}")
st.pyplot(fig3)
