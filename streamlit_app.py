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

# Code for the LLM Part: 
import random
from ollama import chat, ChatResponse

# Create an instance of MovieDataset
test_instance = MovieData(url=url)

# Set page configuration
st.set_page_config(page_title="Random Movie Information", page_icon="🎬", layout="wide")

# Streamlit page title
st.title("Random Movie Information")

# Filter movies with existing summaries and genres
valid_movies = test_instance.movie_metadata[
    (test_instance.movie_metadata["wiki_movie_id"].isin(test_instance.plot_summaries["wiki_movie_id"])) &
    (test_instance.movie_metadata["genres"].notna())
]

# Shuffle button
if st.button("Shuffle"):
    # Ensure there are valid movies to choose from
    if valid_movies.empty:
        st.error("No movies with summaries and genres available.")
    else:
        # Select a random movie from the filtered list
        random_index = random.randint(0, len(valid_movies) - 1)
        movie = valid_movies.iloc[random_index]
        movie_id = movie["wiki_movie_id"]
        
        # Get the movie title and summary
        movie_title = movie["movie_name"]
        plot_summary_row = test_instance.plot_summaries[test_instance.plot_summaries["wiki_movie_id"] == movie_id]
        
        if not plot_summary_row.empty:
            movie_summary = plot_summary_row["plot_summary"].values[0]
        else:
            movie_summary = "Summary not available."
        
        # Get the movie genres
        movie_genres = eval(movie["genres"]).values()
        
        # Display the information in text boxes
        st.markdown(f"### {movie_title}\n\n{movie_summary}")
        st.text_area("Genres", ", ".join(movie_genres))
        
        # Use local LLM to classify the genre
        response: ChatResponse = chat(model='mistral', messages=[
            {
                'role': 'user',
                'content': f'Classify the following movie summary into genres: {movie_summary}. Only list the genres, separated by commas. Do not include any additional information or brackets.',
            },
        ])
        
        # Extract and display the genre classification
        llm_genres = response.message.content.strip()
        st.text_area("Genre by LLM", llm_genres)
        
        # Normalize and compare genres
        identified_genres = set([genre.strip().lower() for genre in llm_genres.split(",")])
        database_genres = set([genre.strip().lower() for genre in movie_genres])
        
        matching_genres = identified_genres.intersection(database_genres)
        
        if matching_genres:
            st.markdown("### Successfully Detected Genres")
            st.markdown(", ".join(matching_genres))
        
        if identified_genres.issubset(database_genres):
            st.success("The genres identified by the LLM are contained in the database genres.")
        else:
            st.warning("The genres identified by the LLM are not fully contained in the database genres.")
        
        # Visualization of the score
        genre_counts = {
            "Database Genres": len(database_genres),
            "LLM Genres": len(identified_genres),
            "Matching Genres": len(matching_genres)
        }
        
        fig, ax = plt.subplots()
        ax.bar(genre_counts.keys(), genre_counts.values(), color=["skyblue", "lightcoral", "lightgreen"])
        ax.set_ylabel("Count")
        ax.set_title("Genre Detection Score")
        st.pyplot(fig)
