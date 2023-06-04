from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """ This Function reads the data file and returns the
            contents of the file"""
        pass

    @abstractmethod
    def add_movie(self, title):
        """ This function adds a movie to our data file """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """ This function deletes a movie found in the data file """
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        """ This function changes/updates the rating of a movie in our data file """
        pass
