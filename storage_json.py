from istorage import IStorage
import json
import requests

API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=e9c4608d&t='


class StorageJson(IStorage):

    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        try:
            with open(self.file_path, 'r') as fileobj:
                data = fileobj.read()
                movies = json.loads(data)

        except FileNotFoundError:
            with open(self.file_path, 'w') as file: # Writes a new file if the file doesn't exist
                empty_file = {}
                json.dump(empty_file, file)

            with open(self.file_path, 'r') as fileobj:
                data = fileobj.read()
                movies = json.loads(data)
        return movies

    @staticmethod
    def api_get(title):
        space_replace_title = title.replace(' ', '+')
        response = requests.get(API_URL + space_replace_title)
        return response.json()

    def add_movie(self, title):
        data = self.api_get(title)
        new_dict = {
            data['Title']: {'Rating': float(data['imdbRating']), 'Year': int(data['Year']), 'Poster': data['Poster']}}
        all_data = self.list_movies()
        all_data.update(new_dict)
        with open(self.file_path, 'w') as fileobj:
            json.dump(all_data, fileobj)

    def delete_movie(self, title):
        movies = self.list_movies()
        del movies[title]

        with open(self.file_path, 'w') as fileobj:
            json.dump(movies, fileobj)

    def update_movie(self, title, notes):
        data = self.list_movies()
        data[title]['Notes'] = notes

        with open(self.file_path, 'w') as fileobj:
            json.dump(data, fileobj)
