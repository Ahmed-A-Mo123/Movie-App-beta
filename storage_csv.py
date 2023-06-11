from istorage import IStorage
import csv
import requests

API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=e9c4608d&t='


class StorageCsv(IStorage):
    """A class that implements the IStorage interface using CSV file storage."""
    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def read_csv_file(self):
        """Reads the file and turns the csv file into a dictionary by going row by row and creating a dictionary out of
        it"""
        movies_dict = {}
        with open(self.file_path, 'r') as fileobj:
            csv_reader = csv.DictReader(fileobj)
            for row in csv_reader:
                key = row[csv_reader.fieldnames[0]]
                movies_dict[key] = row
        return movies_dict

    def save_csv_file(self, movies):
        """Saves the movies dict into a csv file by creating headers (which are hard coded), then taking the contents
        of dict and placing it row by row for each movie."""
        with open(self.file_path, 'w', newline='') as fileobj:
            headers_list = ['title', 'Rating', 'Year', 'Poster', 'Notes']
            w = csv.DictWriter(fileobj, fieldnames=headers_list)
            w.writeheader()
            for key, val in movies.items():
                row = {'title': key, **val}
                w.writerow(row)

    def list_movies(self):
        """This method returns the dictionary of the movies and handles if a new file has been created"""
        try:
            movies = self.read_csv_file  # Reads the Csv File and determines if it exists
        except FileNotFoundError:
            with open(self.file_path, 'w') as fileobj:
                empty_file = {}
                self.save_csv_file(empty_file)
                movies = self.read_csv_file
        return movies

    @staticmethod
    def api_get(title):
        """Sends a requests to the API for the movie details"""
        space_replace_title = title.replace(' ', '+')
        response = requests.get(API_URL + space_replace_title)
        return response.json()

    def add_movie(self, title):
        """ Gets the information from the API and turns it into a new dictionary which then gets saved to file"""
        data = self.api_get(title)
        new_dict = {
            data['Title']: {'Rating': float(data['imdbRating']), 'Year': int(data['Year']), 'Poster': data['Poster']}}
        movies = self.list_movies()
        movies.update(new_dict)
        self.save_csv_file(movies)

    def delete_movie(self, title):
        """ Removes the movie the user specifies from the CSV file """
        movies = self.list_movies()
        del movies[title]
        self.save_csv_file(movies)

    def update_movie(self, title, notes):
        """Updates the movie notes"""
        movies = self.list_movies()
        movies[title]['Notes'] = notes
        self.save_csv_file(movies)


