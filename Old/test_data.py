from movie_data_v2 import MovieData

# Initialize the class
url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
movie_data = MovieData(url=url)

# Check if movie metadata is loaded
print("\n🔍 Checking movie dataset:")
print(movie_data.movie_df.head())

# Check if character metadata is loaded
print("\n🔍 Checking character dataset:")
print(movie_data.character_df.head())

# Test releases() method
print("\n🎥 Testing releases() method:")
try:
    df_releases = movie_data.releases()
    print(df_releases.head())
except Exception as e:
    print(f"⚠️ releases() error: {e}")

# Test ages() method
print("\n👶 Testing ages() method:")
try:
    df_ages = movie_data.ages(unit="Y")
    print(df_ages.head())
except Exception as e:
    print(f"⚠️ ages() error: {e}")
