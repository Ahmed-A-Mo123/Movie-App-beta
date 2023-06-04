import statistics
import random
import requests


MENU = """
'********** My Movies Database **********\n\nMenu:\n\n0. Exit
1. list movies \n2. Add movie\n3. Delete movie
4. Update movie\n5. Stats\n6. Random movie
7. Search movie\n8. Movies sorted by rating\n9. Generate Website
"""


class MovieApp:
    def __init__(self, storage):
        self.storage = storage

    def _command_list_movies(self):
        movies = self.storage.list_movies()
        print(f'{len(movies)} in total:\n')
        for movie_title, info in movies.items():
            rating = info['Rating']
            year = info['Year']
            print(f'{movie_title}:\n               Rating: {rating}  Year: {year}  ')

    def _command_add_movie(self):
        """Add movie function"""
        movies = self.storage.list_movies()
        title = input('Enter new movie name: ')

        if title in movies:
            print(f'Movie {title} already exists')
            return

        self.storage.add_movie(title)
        print(f"Movie '{title}' successfully added")

    def _command_del_movie(self):
        """Delete movies function."""
        movies = self.storage.list_movies()
        title = input('Enter movie to delete: ')
        if title in movies:
            self.storage.delete_movie(title)
            print(f'Movie {title} successfully deleted: ')
        else:
            print('Error movie not found! ')

    def _command_update_movie(self):
        movies = self.storage.list_movies()
        title = input('Enter movie name: ')
        if title in movies:
            rating = int(input('Enter new movie rating (0-10): '))
            self.storage.update_movie(title, rating)
            print(f'Movie {title} successfully updated')
        else:
            print('Error movie not found! ')

    def _command_movie_stats(self):
        """
        Provide statistics about the movie list.
        Includes Mean(Average), Median, Best Movie(s)
        Ratings And Worst Movies Ratings().
        """
        movies = self.storage.list_movies()
        list_of_ratings = [movie['Rating'] for movie in movies.values()]
        # -------------------------------------------------------------------
        print(f'Average rating: {round(statistics.mean(list_of_ratings), 2)}')
        # -------------------------------------------------------------------
        print(f'Median rating: {statistics.median(list_of_ratings)}')
        # -------------------------------------------------------------------
        highest_rating_counter = max(list_of_ratings)
        best_movie = ''
        for movie in movies:
            value = movies[movie]['Rating']
            if value == highest_rating_counter:
                best_movie += f' {movie},'
        print(f'Best movie(s): {best_movie}')
        # -------------------------------------------------------------------
        lowest_rating_counter = min(list_of_ratings)
        worst_movie = ''
        for movie in movies:
            value = movies[movie]['Rating']
            if value == lowest_rating_counter:
                worst_movie += f'{movie}, '
        print(f'Worst movie(s): {worst_movie}')

    def _command_random_movie(self):
        """
        Selects And Recommends A Random Movie
        For The User To Watch From Movie List.
        """
        movies = self.storage.list_movies()
        list_of_movies = list(movies.items())
        key, value = random.choice(list_of_movies)
        rating = value['Rating']
        print(f'Your Movie For Tonight: {key}, Its Rated {rating}')

    def _command_search_movie(self):
        """
        Allows User To Search For A Movie, Even Without
        The Full Title And In Any Case (Case Insensitive),
        In The Movie List.
        """
        movies = self.storage.list_movies()
        search_input = input('Enter Part Of A Movie Name: ')
        for key, value in movies.items():
            rating = value['Rating']
            year = value['Year']
            if search_input.lower() in key.lower():
                print(f'{key}, Rated: {rating}, Year Of Release: {year}')

    def _command_sorted_movies(self):
        """Sorts the Movie List In Descending Rating Order."""
        movies = self.storage.list_movies()
        new_dict = {movie: movies[movie]['Rating'] for movie in movies}
        sorted_movie_list = dict(sorted(new_dict.items(), key=lambda x: x[1], reverse=True))
        print()  # Line space
        for key, value in sorted_movie_list.items():
            print(f'{key}, {value}')

    @staticmethod
    def html_format(replace_obj, page_title):
        with open('index_template.html', 'r') as fileobj:
            html_content = fileobj.read()
            new_html_content = html_content.replace('__TEMPLATE_MOVIE_GRID__', replace_obj).replace(
                '__TEMPLATE_TITLE__',
                page_title)

        with open('movie_app.html', 'w') as newfile:
            newfile.write(new_html_content)

    def _command_generate_website(self):
        """This Function generates a html file which takes from our api data"""
        movies = self.storage.list_movies()
        html_title = "Ahmed's Movie App!"
        html_replace = ''
        for title, info in movies.items():
            year = info['Year']
            poster = info['Poster']
            img = f'<img class="movie-poster" src="{poster}"/>'
            movie_name = f'<div class="movie-title">{title}</div>'
            yr_html = f'<div class="movie-year">{year}</div>'
            html_each_movie = f'<li> <div class="movie">{img} {movie_name} {yr_html} </div> </li>'
            html_replace += html_each_movie
        self.html_format(html_replace, html_title)
        print('\nWebsite Has Been Generated, Take A look!')

    def run(self):
        """ Main Function Where We Tie Our Function Together
        And Pass The Functions Their Arguments
        (We Also Have Our Original Dictionary).
        """

        # Below We Have The Menu And User options Defined.
        # -------------------------------------------------------------------
        while True:

            print(MENU)
            # -------------------------------------------------------------------
            try:
                user_menu_choice = int(input('Enter choice (0-9): '))
            except ValueError:
                user_menu_choice = 'ERROR'
            # --------------------------------------------------------------------
            if user_menu_choice == 0:
                print('\nBYE *\(^o^)/*\n')
                exit()

            # -------------------------------------------------------------------
            if user_menu_choice == 1:
                movies = self.storage.list_movies()
                print(f'{len(movies)} in total:\n')
                for movie_title, info in movies.items():
                    rating = info['Rating']
                    year = info['Year']
                    print(f'{movie_title}:\n               Rating: {rating}  Year: {year}  ')

            # -------------------------------------------------------------------
            elif user_menu_choice == 2:
                try:
                    self._command_add_movie()
                except KeyError:
                    print("\nThis movie Doesn't Exist")
                except requests.exceptions.RequestException:
                    print("Couldn't Reach the Server")

            # -------------------------------------------------------------------
            elif user_menu_choice == 3:
                self._command_del_movie()

            # -------------------------------------------------------------------
            elif user_menu_choice == 4:
                self._command_update_movie()

            # -------------------------------------------------------------------
            elif user_menu_choice == 5:
                self._command_movie_stats()

            # -------------------------------------------------------------------
            elif user_menu_choice == 6:
                self._command_random_movie()

            # -------------------------------------------------------------------
            elif user_menu_choice == 7:
                self._command_search_movie()

            # -------------------------------------------------------------------
            elif user_menu_choice == 8:
                self._command_sorted_movies()

            # -------------------------------------------------------------------
            elif user_menu_choice == 9:
                self._command_generate_website()
            # -------------------------------------------------------------------
            elif user_menu_choice == 'ERROR':
                print('\n*** Please Enter A Number From The Menu Choices ***')

            # -------------------------------------------------------------------
            input('\nPress Enter To Continue ')


