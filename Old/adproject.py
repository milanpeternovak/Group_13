import pandas as pd
from urllib.request import urlretrieve
import os
import tarfile


#link for the dataset
data_link = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"

class PEP8:
    def __init__(file_link: str, output_file: str='movie_data.tar.gz'):
        """
        First step: Downloads a file from an URL into your hard drive, if it doesn't exist already, if it does,
        then the user gets a warning saying: "File already exists!".
        
        Parameters
        ------------
        file_link: str
            A string containing the link to the file you wish to download.
        output_file: str
            A string containing the name of the output file. The default value is 'movie_data.tar.gz'
            at the location you are running the function.
            
        ------------
        ------------
        Second step: Opens the file, and unzips it, to the working directory, using the output_file variable.

        ------------
        ------------
        Third step: Reads in the tab separated files into pandas dataframes, while naming the columns appropriately. 
        After reading the files into dataframes, it merges the two in order to be able to analyze it simultaneously.

        Returns
        ---------
        .head() of the merged dataframe.
        """
        
        # If file doesn't exist, download it. Else, print a warning message.
        if not os.path.exists(output_file):
            urlretrieve(file_link, filename=output_file)
        else:
            print("File already exists!")
            # Open the tar.gz file
        with tarfile.open(output_file, 'r:gz') as tar:
            # Extract all contents to the current directory
            tar.extractall()
        column_names_for_movies = ['wikipedia_movie_id', 'freebase_movie_id', 'title', 'release_date', 'box_office_revenue', 'runtime_min', 'languages', 'countries', 'genres']
        dataframe_for_movies = pd.read_csv('/Users/novakmilanpeter/Desktop/nova_advanced_programming/MovieSummaries/movie.metadata.tsv',sep = '\t', names=column_names_for_movies, header=None)
        
        column_names_for_characters = ['wikipedia_movie_id', 'freebase_movie_id', 'movie_release_date', 'character_name', 'actor_date_of_birth', 'actor_gender', 'actor_height_in_meters', 'actor_ethnicity_freebase_id', 'actor_name', 'actor_age_at_movie_release', 'freebase_character_or_actor_map_id', 'freebase_character_id', 'freebase_actor_id']
        dataframe_for_characters = pd.read_csv('/Users/novakmilanpeter/Desktop/nova_advanced_programming/MovieSummaries/character.metadata.tsv',sep = '\t', names=column_names_for_characters, header=None)

        dataframe = pd.merge(dataframe_for_characters, dataframe_for_movies, on = ['freebase_movie_id', 'wikipedia_movie_id'], how = 'left')

        return dataframe_for_movies.head()
    def __movietype__(N: int=10):
        if type(N) != int:
            raise TypeError("Variable 'N' is not an integer. DO SOMETHING ABOUT IT!")
        #else:
            #we need to do this part!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __actor_count__():
        pass
    def __actor_distributions__(gender: str, max_height: float, min_height: float, plot: bool=False):
        if type(gender) != str:
            raise TypeError("Variable 'gender' is not a string. DO SOMETHING ABOUT IT!")
        elif type(max_height) !=float:
            raise TypeError("Variable 'max_height' is not a float. DO SOMETHING ABOUT IT!")
        elif type(min_height)!=float:
            raise TypeError("Variable 'min_height' is not a float. DO SOMETHING ABOUT IT!")
        
        

            
PEP8.__actor_distributions__("M", 1.8, 1.5, True)