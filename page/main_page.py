import streamlit as st
import matplotlib.pyplot as plt

def main_page(movie_data):
    st.title("🎬 Movie Data Analysis")

    # User inputs
    col1, col2 = st.columns(2)

    with col1:
        N = st.number_input("Select number of top genres (N):", min_value=1, max_value=50, value=10, step=1)
        movie_genres_df = movie_data.movie_type(N=N)

        st.subheader("📊 Top Movie Genres")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(movie_genres_df["Movie_Type"], movie_genres_df["Count"], color="skyblue")
        ax.set_xlabel("Count")
        ax.set_ylabel("Movie Genre")
        ax.set_title(f"Top {N} Most Common Movie Genres")
        st.pyplot(fig)

    with col2:
        st.subheader("🎭 Actor Count Per Movie")
        actor_count_df = movie_data.actor_count()
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(actor_count_df["Number_of_Actors"], actor_count_df["Movie_Count"], color="salmon")
        ax2.set_xlabel("Number of Actors")
        ax2.set_ylabel("Movie Count")
        ax2.set_title("Distribution of Number of Actors Per Movie")
        st.pyplot(fig2)

    # Actor height distribution
    st.subheader("📈 Actor Height Distribution")
    gender = st.selectbox("Select Gender:", ["All"] + movie_data.character_df["actor_gender"].dropna().unique().tolist())
    min_height = st.number_input("Minimum Height (m):", min_value=0.5, max_value=3.0, value=1.5, step=0.1)
    max_height = st.number_input("Maximum Height (m):", min_value=0.5, max_value=3.0, value=2.0, step=0.1)

    if min_height > max_height:
        st.error("⚠️ Minimum height must be less than maximum height.")

    actor_height_df = movie_data.actor_distributions(gender=gender, min_height=min_height, max_height=max_height)
    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.hist(actor_height_df["actor_height_in_meters"].dropna(), bins=30, color="green", edgecolor="black")
    ax3.set_xlabel("Height (meters)")
    ax3.set_ylabel("Frequency")
    ax3.set_title(f"Height Distribution for {gender}")
    st.pyplot(fig3)
