import pytest
import pandas as pd
from Class_MovieData import MovieData


# Mock URL for testing
TEST_URL = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"

# Initialize the class once to use in multiple tests
@pytest.fixture
def movie_data_instance():
    return MovieData(url=TEST_URL)


# Test movie_type() method
def test_movie_type(movie_data_instance):
    df = movie_data_instance.movie_type(N=5)
    assert isinstance(df, pd.DataFrame), "Expected a DataFrame"
    assert "Movie_Type" in df.columns, "Expected column 'Movie_Type'"
    assert "Count" in df.columns, "Expected column 'Count'"
    assert len(df) <= 5, "DataFrame should have at most 5 rows"

# Test movie_type() invalid input
def test_movie_type_invalid(movie_data_instance):
    with pytest.raises(TypeError):
        movie_data_instance.movie_type(N="ten")


# Test actor_count() method
def test_actor_count(movie_data_instance):
    df = movie_data_instance.actor_count()
    assert isinstance(df, pd.DataFrame), "Expected a DataFrame"
    assert "Number_of_Actors" in df.columns, "Expected column 'Number_of_Actors'"
    assert "Movie_Count" in df.columns, "Expected column 'Movie_Count'"


# Test releases() method
def test_releases(movie_data_instance):
    df = movie_data_instance.releases()
    assert isinstance(df, pd.DataFrame), "Expected a DataFrame"
    assert "release_year" in df.columns or "Year" in df.columns, "Expected a 'Year' or 'release_year' column"
    assert "Movie_Count" in df.columns, "Expected column 'Movie_Count'"


# Test ages() method (Births per year)
def test_ages_year(movie_data_instance):
    df = movie_data_instance.ages(unit="Y")
    assert isinstance(df, pd.DataFrame), "Expected a DataFrame"
    assert "Year" in df.columns, "Expected column 'Year'"
    assert "Birth_Count" in df.columns, "Expected column 'Birth_Count'"


# Test ages() method (Births per month)
def test_ages_month(movie_data_instance):
    df = movie_data_instance.ages(unit="M")
    assert isinstance(df, pd.DataFrame), "Expected a DataFrame"
    assert "Month" in df.columns, "Expected column 'Month'"
    assert "Birth_Count" in df.columns, "Expected column 'Birth_Count'"


# Test invalid input for ages()
def test_ages_invalid(movie_data_instance):
    df = movie_data_instance.ages(unit="invalid")
    assert "Year" in df.columns, "Default should be 'Year' if an invalid unit is passed"
