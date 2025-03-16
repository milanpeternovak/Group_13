import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from movie_data_v2 import MovieData  # Ensure the class is in the same directory

# Initialize MovieData instance
url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
movie_data = MovieData(url=url)

# Streamlit Page Title
st.title("📅 Chronological Movie Releases")

# Sidebar Section for User Inputs
st.sidebar.header("User Inputs")

# Select Genre (Limited to 10 genres for efficiency)
common_genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Fantasy", "Adventure", "Animation"]
selected_genre = st.sidebar.selectbox("Select Genre:", ["All"] + common_genres)

# Fetch data from releases method
if selected_genre == "All":
    release_df = movie_data.releases()
else:
    try:
        release_df = movie_data.releases(genre=selected_genre)
    except ValueError as e:
        st.sidebar.error(str(e))
        release_df = pd.DataFrame()

# Plot movie releases per year
if not release_df.empty:
    st.subheader(f"📊 Number of Movies Released Per Year ({selected_genre})")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(release_df["release_year"], release_df["Movie_Count"], color="dodgerblue")
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Movies")
    ax.set_title(f"Movies Released Per Year - {selected_genre}")
    st.pyplot(fig)
else:
    st.warning("No data available for the selected genre.")

# ---- Actor Birth Distribution ----
st.subheader("🎂 Actor Birth Distribution")
unit_options = {"Year": "Y", "Month": "M"}
selected_unit = st.sidebar.selectbox("Select Birth Distribution Unit:", list(unit_options.keys()))

# Fetch birth data
birth_df = movie_data.ages(unit=unit_options[selected_unit])

if not birth_df.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(birth_df.iloc[:, 0], birth_df["Birth_Count"], color="seagreen")
    ax2.set_xlabel(selected_unit)
    ax2.set_ylabel("Number of Births")
    ax2.set_title(f"Actor Births Per {selected_unit}")
    st.pyplot(fig2)
else:
    st.warning("No data available for the selected unit.")