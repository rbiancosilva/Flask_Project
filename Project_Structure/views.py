from flask import Flask, render_template, Blueprint, request
from flask_login import login_required, current_user, LoginManager
from .models import User, List, ListMovies, Movie

import json
import requests



#Starts API Data
url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYTlkZWNhZjg5NzNlMGVmMGNjNWZkNzU4Y2E5ZTFiZSIsInN1YiI6IjY2MmQ0MjBmZDk2YzNjMDEyMjk4NDgzOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CTAPTXO9OkucFMYvBdeoO94A_04p6ArYDE_Tic0JRls"
}

datas = (json.loads((requests.get(url, headers=headers)).content))['results']

#Initializes python module views.py
views = Blueprint("views", __name__)

#Route for home page layout using data from API
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", title = "Home", datas = datas, api_datas = datas, user=current_user)

#Route for login page layout
@views.route('/login_page', methods = ['GET', 'POST'])
def login_page():
    return render_template("login_page.html", title = "Login", user = current_user)

#Route for register page layout
@views.route('/register_page', methods = ['GET', 'POST'])
def register_page():
    return render_template("register_page.html", title = "Register", error = None, user = current_user)

#Route for profile page with user's movie list
@views.route('/profile_page', methods = ['GET', 'POST'])
@login_required
def profile_page():
    user_movies_query = current_user.notes[0].listmovies

    user_movies_list = []

    for data in datas:
        for movie in user_movies_query:
            if data['id'] == movie.movie_id:
                user_movies_list.append(data)
    
    return render_template("profile_page.html", title = "Profile", user=current_user, datas = user_movies_list)

#Route for API data filtering, loads home layout
@views.route('/filter_home', methods = ['GET', 'POST'])
@login_required
def filter_home():
    cat = request.args.get('category')
    data_filtered = []
    if cat == "":
        return render_template("home.html", datas = datas,api_datas = datas, user=current_user)
    else:
        for data in datas:
            for genre_id in data['genre_ids']:
                if int(cat) == int(genre_id):
                    data_filtered.append(data)
    return render_template("home.html", datas = datas, api_datas = data_filtered, user=current_user)

#Route for API data details
@views.route('/details_page/<int:data_id>', methods = ['GET', 'POST'])
@login_required
def details_page(data_id):
    for data in datas:
        if data_id == data['id']:
            data_detailed = data
            return render_template("details_page.html", data = data_detailed, user=current_user, title=data_detailed['original_title'])

#Route for users page layout, loading all users from db
@views.route('/users_page', methods = ['GET', 'POST'])
@login_required
def users_page():
    users = User.query.all()

    return render_template("users_page.html", user = current_user, users = users, title="Users")

#Route for user's details page, loading user's list
@views.route('/user_details/<int:user_id>')
@login_required
def user_details(user_id):
    users = User.query.all()
    for user in users:
        if user.id == user_id:
            user_x = user
    user_list = user_x.notes
    listmovies_list = ListMovies.query.all()
    
    list_movies_id = []

    for movie in listmovies_list:
        for note in user_list:
            if movie.list_id == note.id:
                list_movies_id.append(movie)

    list_movies = []

    for data in datas:
        for movie in list_movies_id:
                if movie.movie_id == data['id']:
                    list_movies.append(data)

    return render_template("user_details.html", user = current_user, user_details = user_x, datas = list_movies, title=user_x.username)
                    