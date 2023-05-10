import json
import requests

API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=e9c4608d&t='


def list_movies():
    """ This Function reads the data file and returns the
    contents of the file"""
    with open('data.json', 'r') as fileobj:
        data = fileobj.read()
        movies = json.loads(data)
    return movies


def api_get(title):
    space_replace_title = title.replace(' ', '+')
    response = requests.get(API_URL + space_replace_title)
    return response.json()


def add_movie(title):
    """ This function adds a movie to our data file """
    data = api_get(title)
    new_dict = {
        data['Title']: {'Rating': float(data['imdbRating']), 'Year': int(data['Year']), 'Poster': data['Poster']}}
    all_data = list_movies()
    all_data.update(new_dict)
    with open('data.json', 'w') as fileobj:
        json.dump(all_data, fileobj)


def delete_movie(title):
    """ This function deletes a movie found in the data file """
    movies = list_movies()
    del movies[title]

    with open('data.json', 'w') as fileobj:
        json.dump(movies, fileobj)


def update_movie(title, rating):
    """ This function changes/updates the rating of a movie in our data file """
    data = list_movies()
    data[title]['Rating'] = rating

    with open('data.json', 'w') as fileobj:
        json.dump(data, fileobj)


def html_format(replace_obj, page_title):
    with open('index_template.html', 'r') as fileobj:
        html_content = fileobj.read()
        new_html_content = html_content.replace('__TEMPLATE_MOVIE_GRID__', replace_obj).replace('__TEMPLATE_TITLE__',
                                                                                                page_title)

    with open('movie_app.html', 'w') as newfile:
        newfile.write(new_html_content)
