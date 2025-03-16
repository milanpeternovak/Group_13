import os
import tarfile
import requests
import pandas as pd
import ast  # Required for safely converting string dictionaries to Python dictionaries
from collections import Counter  # Required for counting occurrences in a list
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field, model_validator


class MovieData(BaseModel):
    """
    A class to handle the automated downloading, extraction,
    and loading of movie-related datasets.

    Attributes
    ----------
    url : str
        URL to download the dataset.
    download_path : str
        Directory where the downloaded file will be stored.
    extract_path : str
        Directory where extracted files will be placed.
    movie_df : pd.DataFrame or None
        DataFrame containing movie metadata.
    character_df : pd.DataFrame or None
        DataFrame containing character metadata.
    """

    url: str = Field(..., description="URL of the dataset")
    download_path: str = Field(
        default="downloads/", description="Directory for the downloaded file"
    )
    extract_path: str = Field(
        default="downloads/MovieSummaries/", description="Directory for extracted files"
    )
    movie_df: pd.DataFrame = None
    character_df: pd.DataFrame = None
    plot_summaries: pd.DataFrame = None

    model_config = {
        "arbitrary_types_allowed": True  # Allows Pandas DataFrames within Pydantic models
    }

    @model_validator(mode="after")
    def setup(self) -> "MovieData":
        """
        Handles the downloading, extraction, and loading of datasets.

        This method checks if the dataset is already downloaded, extracts it if necessary,
        and then loads the relevant files into Pandas DataFrames.

        Returns
        -------
        MovieData
            The instance of the MovieData class with the datasets loaded.

        Raises
        ------
        FileNotFoundError
            If the expected dataset files are missing after extraction.
        """
        os.makedirs(self.download_path, exist_ok=True)
        filename = os.path.join(self.download_path, "MovieSummaries.tar.gz")

        # Download the dataset if it does not exist locally
        if not os.path.exists(filename):
            self._download_file(self.url, filename)
        else:
            print("Dataset already downloaded.")

        # Extract the dataset if it has not been extracted yet
        if not os.path.exists(self.extract_path):
            self._extract_file(filename, self.download_path)
        else:
            print("Dataset already extracted.")

        # Load the datasets into Pandas DataFrames
        self._load_dataframes()

        return self

    def _download_file(self, url: str, filename: str) -> None:
        """
        Downloads a file from the given URL and saves it locally.

        Parameters
        ----------
        url : str
            The URL from which to download the dataset.
        filename : str
            The local path where the downloaded file will be stored.
        """
        print(f"Downloading dataset from {url}...")
        response = requests.get(url, stream=True)
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("Download complete.")

    def _extract_file(self, filepath: str, extract_to: str) -> None:
        """
        Extracts a compressed tar.gz file to a specified directory.

        Parameters
        ----------
        filepath : str
            The path to the compressed file.
        extract_to : str
            The directory where the extracted files will be placed.
        """
        print("Extracting dataset...")
        with tarfile.open(filepath, "r:gz") as tar:
            tar.extractall(extract_to)
        print("Extraction complete.")

    def _load_dataframes(self) -> None:
        """
        Loads the extracted TSV dataset files into Pandas DataFrames.

        Raises
        ------
        FileNotFoundError
            If any of the required dataset files are missing.
        """
        movie_file = os.path.join(self.extract_path, "movie.metadata.tsv")
        character_file = os.path.join(self.extract_path, "character.metadata.tsv")
        plot_file = os.path.join(self.extract_path, "plot_summaries.txt")

        if os.path.exists(movie_file) and os.path.exists(character_file):
            self.movie_df = pd.read_csv(
                movie_file,
                sep="\t",
                names=[
                    "wikipedia_movie_id",
                    "freebase_movie_id",
                    "title",
                    "release_date",
                    "box_office_revenue",
                    "runtime_min",
                    "languages",
                    "countries",
                    "genres",
                ],
                header=None,
            )

            self.character_df = pd.read_csv(
                character_file,
                sep="\t",
                names=[
                    "wikipedia_movie_id",
                    "freebase_movie_id",
                    "movie_release_date",
                    "character_name",
                    "actor_date_of_birth",
                    "actor_gender",
                    "actor_height_in_meters",
                    "actor_ethnicity_freebase_id",
                    "actor_name",
                    "actor_age_at_movie_release",
                    "freebase_character_or_actor_map_id",
                    "freebase_character_id",
                    "freebase_actor_id",
                ],
                header=None,
            )
            self.plot_summaries = pd.read_csv(
                plot_file,
                sep="\t",
                names=[
                    "wikipedia_movie_id",
                    "plot_summary"
                ],
                header=None,
            )

            print("Datasets loaded successfully.")
        else:
            raise FileNotFoundError(
                "One or more dataset files are missing. Check extraction."
            )

    def movie_type(self, N: int = 10) -> pd.DataFrame:
        """
        Identifies the top N most common movie genres.

        Parameters:
        ----------
        N : int, optional
            The number of most common movie genres to return (default is 10).

        Returns:
        -------
        pd.DataFrame
            A DataFrame with two columns:
            - 'Movie_Type': Genre name.
            - 'Count': Number of occurrences of each genre.

        Raises:
        ------
        TypeError: If N is not an integer.
        ValueError: If the dataset is not loaded.
        """

        # Ensure that N is an integer
        if not isinstance(N, int):
            raise TypeError("N must be an integer.")

        # Ensure that the dataset has been loaded
        if self.movie_df is None:
            raise ValueError("Dataset not loaded.")

        # Convert genre column from string format to dictionary format
        self.movie_df["genres"] = self.movie_df["genres"].apply(ast.literal_eval)

        # Extract all genres from the dictionary and flatten into a single list
        all_genres = [
            genre
            for sublist in self.movie_df["genres"].apply(lambda x: list(x.values()))
            for genre in sublist
        ]

        # Count the occurrences of each genre
        genre_counts = Counter(all_genres)

        # Get the N most common genres
        most_common_genres = genre_counts.most_common(N)

        # Return the results as a Pandas DataFrame
        return pd.DataFrame(most_common_genres, columns=["Movie_Type", "Count"])

    def actor_count(self) -> pd.DataFrame:
        """
        Computes a histogram showing the number of actors per movie.

        Returns:
        -------
        pd.DataFrame
            A DataFrame with two columns:
            - 'Number_of_Actors': Number of actors in a movie.
            - 'Movie_Count': Number of movies that have that many actors.

        Raises:
        ------
        ValueError: If the dataset is not loaded.
        """

        # Ensure that the dataset has been loaded
        if self.character_df is None:
            raise ValueError("Dataset not loaded.")

        # Group by 'wikipedia_movie_id' to count the number of unique actors per movie
        movie_actor_counts = (
            self.character_df.groupby("wikipedia_movie_id")["actor_name"]
            .nunique()
            .reset_index()
        )

        # Rename columns for clarity
        movie_actor_counts.columns = ["wikipedia_movie_id", "Number_of_Actors"]

        # Count how many movies have the same number of actors
        actor_count_histogram = (
            movie_actor_counts["Number_of_Actors"].value_counts().reset_index()
        )

        # Rename columns for clarity
        actor_count_histogram.columns = ["Number_of_Actors", "Movie_Count"]

        # Sort values by the number of actors for better readability
        actor_count_histogram = actor_count_histogram.sort_values(
            by="Number_of_Actors"
        ).reset_index(drop=True)

        return actor_count_histogram

    def actor_distributions(
        self, gender: str, min_height: float, max_height: float, plot: bool = False
    ) -> pd.DataFrame:
        """
        Filters actors based on gender and height and optionally plots the height distribution.

        Parameters:
        ----------
        gender : str
            The gender to filter by. Accepts "All" or specific values from the dataset.
        min_height : float
            The minimum height (in meters) to include in the filtered dataset.
        max_height : float
            The maximum height (in meters) to include in the filtered dataset.
        plot : bool, optional
            If True, displays a histogram of actor heights (default is False).

        Returns:
        -------
        pd.DataFrame
            A filtered DataFrame with actor names, genders, and heights.

        Raises:
        ------
        TypeError: If gender is not a string or if height values are not numerical.
        ValueError: If min_height is greater than max_height.
        ValueError: If the dataset is not loaded.
        """

        # Ensure that gender is a string
        if not isinstance(gender, str):
            raise TypeError("Gender must be a string.")

        # Ensure that height values are numerical
        if not isinstance(min_height, (int, float)) or not isinstance(
            max_height, (int, float)
        ):
            raise TypeError("Height values must be numerical.")

        # Ensure that min_height is not greater than max_height
        if min_height > max_height:
            raise ValueError("min_height must be less than max_height.")

        # Ensure that the dataset has been loaded
        if self.character_df is None:
            raise ValueError("Dataset not loaded.")

        # Get the list of valid genders from the dataset
        valid_genders = ["All"] + self.character_df[
            "actor_gender"
        ].dropna().unique().tolist()

        # Validate the provided gender input
        if gender not in valid_genders:
            raise ValueError(f"Invalid gender. Accepted values: {valid_genders}")

        # Filter dataset by gender (or keep all genders if "All" is selected)
        filtered_data = (
            self.character_df
            if gender == "All"
            else self.character_df[self.character_df["actor_gender"] == gender]
        )

        # Filter dataset by height range
        filtered_data = filtered_data[
            (filtered_data["actor_height_in_meters"] >= min_height)
            & (filtered_data["actor_height_in_meters"] <= max_height)
        ]

        # If the plot parameter is True, generate a histogram of actor heights
        if plot:
            plt.figure(figsize=(10, 6))
            plt.hist(
                filtered_data["actor_height_in_meters"].dropna(),
                bins=30,
                color="blue",
                edgecolor="black",
            )
            plt.title(f"Height Distribution for Gender: {gender}")
            plt.xlabel("Height (meters)")
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.show()

        return filtered_data
"""
    def releases(self, genre: str = None) -> pd.DataFrame:
        """
        Computes the number of movies released per year, optionally filtered by genre.
        """
        if self.movie_df is None:
            raise ValueError("Dataset not loaded.")

        self.movie_df = self.movie_df.dropna(subset=["release_date"])
        self.movie_df["release_year"] = (
            self.movie_df["release_date"].astype(str).str[:4]
        )

        if genre:
            self.movie_df["genres"] = self.movie_df["genres"].apply(ast.literal_eval)

            all_genres = set(
                genre
                for sublist in self.movie_df["genres"].apply(lambda x: list(x.values()))
                for genre in sublist
            )
            if genre not in all_genres:
                raise ValueError(f"Invalid genre. Choose from: {sorted(all_genres)}")

            self.movie_df["is_genre_match"] = self.movie_df["genres"].apply(
                lambda x: genre in x.values()
            )
            filtered_df = self.movie_df[self.movie_df["is_genre_match"]]
        else:
            filtered_df = self.movie_df

        release_counts = (
            filtered_df.groupby("release_year").size().reset_index(name="Movie_Count")
        )
        release_counts["release_year"] = release_counts["release_year"].astype(int)
        release_counts = release_counts.sort_values(by="release_year").reset_index(
            drop=True
        )

        return release_counts
    """

    def releases(self, genre: str = None) -> pd.DataFrame:
        """
        Computes the number of movies released per year, optionally filtered by genre.
    
        Args:
            genre (str, optional): A specific genre to filter movies by. Defaults to None.
    
        Returns:
            pd.DataFrame: A DataFrame containing the number of movies released per year.
    
        Raises:
            ValueError: If the dataset is not loaded or if an invalid genre is provided.
        """
    
        # Ensure the dataset is loaded
        if self.movie_df is None:
            raise ValueError("Dataset not loaded.")
    
        # Remove rows with missing release dates
        self.movie_df = self.movie_df.dropna(subset=["release_date"])
    
        # Extract the release year as a string and take only the first 4 characters
        self.movie_df["release_year"] = self.movie_df["release_date"].astype(str).str[:4]
    
        # Process genre filtering if a genre is provided
        if genre:
            # Convert genre strings into actual Python lists (from string representations)
            self.movie_df["genres"] = self.movie_df["genres"].apply(ast.literal_eval)
    
            # Extract all unique genre names from the dataset
            all_genres = set(
                genre_name
                for genre_list in self.movie_df["genres"].apply(lambda x: [d["name"] for d in x])
                for genre_name in genre_list
            )
    
            # Validate that the given genre exists in the dataset
            if genre not in all_genres:
                raise ValueError(f"Invalid genre. Choose from: {sorted(all_genres)}")
    
            # Create a boolean column to filter movies containing the specified genre
            self.movie_df["is_genre_match"] = self.movie_df["genres"].apply(
                lambda x: any(d["name"] == genre for d in x)
            )
    
            # Filter dataset to only include movies that match the specified genre
            filtered_df = self.movie_df[self.movie_df["is_genre_match"]]
        else:
            filtered_df = self.movie_df
    
        # Count the number of movies released per year
        release_counts = (
            filtered_df.groupby("release_year")
            .size()
            .reset_index(name="Movie_Count")
        )
    
        # Ensure the release_year column is an integer for sorting purposes
        release_counts["release_year"] = release_counts["release_year"].astype(int)
    
        # Sort by release year and reset index
        release_counts = release_counts.sort_values(by="release_year").reset_index(drop=True)

    return release_counts

    def ages(self, unit: str = "Y") -> pd.DataFrame:
        """
        Computes the number of actor births per year or month.

        Parameters:
        ----------
        unit : str, optional
            'Y' (default) computes births per year.
            'M' computes births per month.
            If any other value is given, defaults to 'Y'.

        Returns:
        -------
        pd.DataFrame
            A DataFrame with two columns:
            - 'Year' / 'Month': The birth year or birth month.
            - 'Birth_Count': Number of actors born in that year or month.
        """

        if self.character_df is None:
            raise ValueError("Dataset not loaded.")

        # Drop rows where the birth date is missing
        self.character_df = self.character_df.dropna(subset=["actor_date_of_birth"])

        # Extract Year and Month
        self.character_df["birth_year"] = (
            self.character_df["actor_date_of_birth"].astype(str).str[:4]
        )
        self.character_df["birth_month"] = (
            self.character_df["actor_date_of_birth"].astype(str).str[5:7]
        )

        # Ensure unit is valid
        if unit not in ["Y", "M"]:
            unit = "Y"

        if unit == "Y":
            birth_counts = (
                self.character_df.groupby("birth_year")
                .size()
                .reset_index(name="Birth_Count")
            )
            birth_counts = birth_counts[
                birth_counts["birth_year"].str.isnumeric()
            ]  # Remove non-numeric years
            birth_counts["birth_year"] = birth_counts["birth_year"].astype(int)
            birth_counts = birth_counts.sort_values(by="birth_year").reset_index(
                drop=True
            )
            birth_counts.rename(columns={"birth_year": "Year"}, inplace=True)
        else:
            # Remove empty birth months before conversion
            self.character_df = self.character_df[
                self.character_df["birth_month"].str.strip() != ""
            ]

            # Convert birth_month to int and group by month
            birth_counts = (
                self.character_df.groupby("birth_month")
                .size()
                .reset_index(name="Birth_Count")
            )
            birth_counts["birth_month"] = birth_counts["birth_month"].astype(int)
            birth_counts = birth_counts.sort_values(by="birth_month").reset_index(
                drop=True
            )
            birth_counts.rename(columns={"birth_month": "Month"}, inplace=True)

        return birth_counts


# Example usage
url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
movie_data = MovieData(url=url)
