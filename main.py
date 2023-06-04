from storage_json import StorageJson
from movie_app import MovieApp


def main():
    ahmed = StorageJson('ahmed_movies.json')
    movies = MovieApp(ahmed)
    ahmed.add_movie('Interstellar')
    ahmed.delete_movie('Interstellar')
    movies.run()



if __name__ == '__main__':
    main()
