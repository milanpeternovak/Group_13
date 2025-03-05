import os
import tarfile
import requests
import pandas as pd
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
    download_path: str = Field(default="downloads/", description="Directory for the downloaded file")
    extract_path: str = Field(default="downloads/MovieSummaries/", description="Directory for extracted files")
    movie_df: pd.DataFrame = None
    character_df: pd.DataFrame = None

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

        if os.path.exists(movie_file) and os.path.exists(character_file):
            self.movie_df = pd.read_csv(
                movie_file, sep="\t",
                names=["wikipedia_movie_id", "freebase_movie_id", "title", "release_date",
                       "box_office_revenue", "runtime_min", "languages", "countries", "genres"],
                header=None
            )

            self.character_df = pd.read_csv(
                character_file, sep="\t",
                names=["wikipedia_movie_id", "freebase_movie_id", "movie_release_date",
                       "character_name", "actor_date_of_birth", "actor_gender", "actor_height_in_meters",
                       "actor_ethnicity_freebase_id", "actor_name", "actor_age_at_movie_release",
                       "freebase_character_or_actor_map_id", "freebase_character_id", "freebase_actor_id"],
                header=None
            )

            print("Datasets loaded successfully.")
        else:
            raise FileNotFoundError("One or more dataset files are missing. Check extraction.")


# Usage example
if __name__ == "__main__":
    url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
    movie_data = MovieData(url=url)

    # Display first few rows of loaded datasets
    print(movie_data.movie_df.head())  # Movie metadata
    print(movie_data.character_df.head())  # Character metadata
