import streamlit as st
from Class_MovieData import MovieData
from pages.main_page import main_page
from pages.chronology import chronology
from pages.classification import classification

# Load the dataset
@st.cache_resource
def load_data():
    url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
    return MovieData(url=url)

st.session_state.movie_data = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Chronology", "Classification"])

if page == "Main":
    main_page(st.session_state.movie_data)
elif page == "Chronology":
    chronology(st.session_state.movie_data)
elif page == "Classification":
    classification(st.session_state.movie_data)
