from flask import Flask, render_template, Blueprint, request, url_for, redirect, jsonify
from .models import User, List, Movie, ListMovies
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from .views import datas

import requests


auth = Blueprint("auth", __name__)

@auth.route('/register', methods = ['POST'])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = str(request.form.get("password"))
    confirmPassword = str(request.form.get("confirmPassword"))

    user = User.query.filter_by(email=email).first()

    if user:
        return render_template("register_page.html", error = "Email already registered", user = current_user)
    elif len(username) < 6 or email == "":
        return render_template("register_page.html", error = "Username not long enough", user = current_user)
    elif len(email)<6 or email == "":
        return render_template("register_page.html", error = "Email is not valid", user = current_user)
    elif len(password) < 8 or str(password) == "":
        return render_template("register_page.html", error = "Your password is too small", user = current_user)
    elif password != confirmPassword:
        return render_template("register_page.html", error = "The passwords don't match", user = current_user)
    else:
        new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), username=username)
        db.session.add(new_user)
        db.session.commit()
        

        return render_template("login_page.html", error=False, user = current_user)

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    password = str(request.form.get("password"))
    user = User.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            if not current_user.notes:
                new_list = List(list_name=current_user.username +"List", user_id=current_user.id)
                db.session.add(new_list)
                db.session.commit()
            return render_template("home.html", user = current_user, api_datas = datas)
        else:
            return render_template("login_page.html", error="Incorrect password", user = current_user)
    else:
        return render_template("login_page.html", error="The email address is not registered", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login_page'))

@auth.route('/add_movie/<int:data_id>', methods = ['GET', 'POST'])
@login_required
def add_movie(data_id):
    
    movie_in_db_id = []

    for movie in Movie.query.all():
        movie_in_db_id.append(movie.id)

    user_movies_query = current_user.notes[0].listmovies
    user_movies_id = []

    for movie in user_movies_query:
        user_movies_id.append(movie.movie_id)
    
    for data in datas:
        if data['id'] == data_id:
            temp_movie = data
    
    if temp_movie['id'] not in movie_in_db_id:
        new_movie = Movie(id=temp_movie['id'],title=temp_movie['original_title'],poster_path=temp_movie['poster_path'])
        db.session.add(new_movie)
        db.session.commit()

    if temp_movie['id'] not in user_movies_id:
        new_listmovie = ListMovies(list_id=current_user.notes[0].id, movie_id=temp_movie['id'])
        db.session.add(new_listmovie)
        db.session.commit()

    user_movies_query = current_user.notes[0].listmovies

    user_movies_list = []

    for data in datas:
        for movie in user_movies_query:
            if data['id'] == movie.movie_id:
                user_movies_list.append(data)

    return render_template("profile_page.html", user = current_user, datas = user_movies_list)

    

    


    