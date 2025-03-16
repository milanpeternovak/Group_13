import streamlit as st
import matplotlib.pyplot as plt
import ast

def chronology(movie_data):
    st.title("📆 Movie Release Timeline")

    # Extract valid genres for dropdown
    def extract_genres(genre_str):
        try:
            return list(ast.literal_eval(genre_str).values())
        except (ValueError, SyntaxError):
            return []

    all_genres = movie_data.movie_df["genres"].dropna().map(extract_genres).explode().unique()

    genre = st.selectbox("Select Genre (Optional):", ["All"] + list(all_genres))

    if genre == "All":
        release_df = movie_data.releases()
    else:
        release_df = movie_data.releases(genre=genre)

    st.subheader(f"🎬 Movies Released Over Time ({genre})")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(release_df["Year"], release_df["Movie_Count"], color="blue")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    ax.set_title("Movies Released Per Year")
    st.pyplot(fig)

    # Actor birth distribution
    unit = st.selectbox("Group actor births by:", ["Year", "Month"])
    unit = "Y" if unit == "Year" else "M"

    birth_df = movie_data.ages(unit=unit)
    st.subheader(f"🎭 Actor Births by {unit}")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    column_name = "Year" if unit == "Y" else "Month"
    ax2.bar(birth_df[column_name], birth_df["Birth_Count"], color="purple")
    ax2.set_xlabel(unit)
    ax2.set_ylabel("Number of Births")
    ax2.set_title(f"Actor Births Per {unit}")
    st.pyplot(fig2)
