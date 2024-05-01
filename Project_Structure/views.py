from flask import Flask, render_template, Blueprint, request

import json
import requests

#Configuring data from API

url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYTlkZWNhZjg5NzNlMGVmMGNjNWZkNzU4Y2E5ZTFiZSIsInN1YiI6IjY2MmQ0MjBmZDk2YzNjMDEyMjk4NDgzOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CTAPTXO9OkucFMYvBdeoO94A_04p6ArYDE_Tic0JRls"
}

datas = (json.loads((requests.get(url, headers=headers)).content))['results']

views = Blueprint("views", __name__)

@views.route('/', methods = ['GET'])
def home():
    return render_template("home.html", title = "Home", datas = datas, api_datas = datas)

@views.route('/login_page', methods = ['GET', 'POST'])
def login_page():
    return render_template("login_page.html", title = "Login")

@views.route('/register_page', methods = ['GET', 'POST'])
def register_page():
    return render_template("register_page.html", title = "Register", error = None)

@views.route('/profile_page', methods = ['GET', 'POST'])
def profile_page():
    return render_template("profile_page.html", title = "Profile")

@views.route('/filter_home', methods = ['GET'])
def filter_home():
    cat = request.args.get('category')
    data_filtered = []
    if cat == "":
        return render_template("home.html", datas = datas,api_datas = datas)
    else:
        for data in datas:
            for genre_id in data['genre_ids']:
                if int(cat) == int(genre_id):
                    data_filtered.append(data)
    return render_template("home.html", datas = datas, api_datas = data_filtered)
    
    

@views.route('/details_page/<int:data_id>', methods = ['GET'])
def details_page(data_id):
    for data in datas:
        if data_id == data['id']:
            data_detailed = data
            return render_template("details_page.html", data = data_detailed)

    