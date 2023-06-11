from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():

    james = StorageCsv('james.csv')
    movies = MovieApp(james)
    james.add_movie('Home Alone')
    movies.run()


if __name__ == '__main__':
    main()
