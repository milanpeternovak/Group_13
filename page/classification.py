import streamlit as st
import random
import matplotlib.pyplot as plt
from ollama import chat, ChatResponse

def classification(movie_data):
    st.title("🤖 Movie Genre Classification with DeepSeek")

    valid_movies = movie_data.movie_df.dropna(subset=["genres", "title"])
    
    if "random_movie" not in st.session_state or st.button("Shuffle"):
        st.session_state.random_movie = valid_movies.sample(1).iloc[0]

    movie = st.session_state.random_movie
    movie_title = movie["title"]
    movie_summary = movie_data.plot_summaries[movie_data.plot_summaries["wikipedia_movie_id"] == movie["wikipedia_movie_id"]]["plot_summary"].values[0]

    st.markdown(f"### 🎬 {movie_title}\n\n📖 {movie_summary}")

    database_genres = eval(movie["genres"]).values()

    # Use DeepSeek for classification
    response: ChatResponse = chat(model="deepseek-r1:1.5b", messages=[{
        "role": "user",
        "content": f"Classify this movie summary into genres: {movie_summary}. Only list the genres, separated by commas."
    }])

    llm_genres = response.message.content.strip()

    # Display results
    st.text_area("Database Genres", ", ".join(database_genres))
    st.text_area("DeepSeek Genres", llm_genres)

    # Compare genres
    identified_genres = set(genre.strip().lower() for genre in llm_genres.split(","))
    database_genres = set(genre.strip().lower() for genre in database_genres)

    matching_genres = identified_genres.intersection(database_genres)

    if matching_genres:
        st.success(f"Matching Genres: {', '.join(matching_genres)}")
    else:
        st.warning("No genres matched between DeepSeek and database genres.")

    # Visualization
    genre_counts = {"Database Genres": len(database_genres), "DeepSeek Genres": len(identified_genres), "Matching Genres": len(matching_genres)}

    fig, ax = plt.subplots()
    ax.bar(genre_counts.keys(), genre_counts.values(), color=["skyblue", "lightcoral", "lightgreen"])
    ax.set_ylabel("Count")
    ax.set_title("Genre Classification Accuracy")
    st.pyplot(fig)
