from istorage import IStorage
import json
import requests

API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=e9c4608d&t='


class StorageJson(IStorage):
    """A class that implements the IStorage interface using JSON file storage."""

    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """Retrieve the list of movies from the JSON file."""
        try:
            with open(self.file_path, 'r') as fileobj:
                data = fileobj.read()
                movies = json.loads(data)

        except FileNotFoundError:
            with open(self.file_path, 'w') as file:
                empty_file = {}
                json.dump(empty_file, file)

            with open(self.file_path, 'r') as fileobj:
                data = fileobj.read()
                movies = json.loads(data)
        return movies

    @staticmethod
    def api_get(title):
        """Make an API request to retrieve movie information."""
        space_replace_title = title.replace(' ', '+')
        response = requests.get(API_URL + space_replace_title)
        return response.json()

    def add_movie(self, title):
        """Add a movie to the JSON file."""
        data = self.api_get(title)
        new_dict = {
            data['Title']: {'Rating': float(data['imdbRating']), 'Year': int(data['Year']), 'Poster': data['Poster']}}
        all_data = self.list_movies()
        all_data.update(new_dict)
        with open(self.file_path, 'w') as fileobj:
            json.dump(all_data, fileobj)

    def delete_movie(self, title):
        """Delete a movie from the JSON file."""
        movies = self.list_movies()
        del movies[title]

        with open(self.file_path, 'w') as fileobj:
            json.dump(movies, fileobj)

    def update_movie(self, title, notes):
        """Update the notes of a movie in the JSON file.    """
        data = self.list_movies()
        data[title]['Notes'] = notes

        with open(self.file_path, 'w') as fileobj:
            json.dump(data, fileobj)
