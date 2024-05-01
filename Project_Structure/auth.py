from flask import Flask, render_template, Blueprint, request

import requests


auth = Blueprint("auth", __name__)

@auth.route('/register', methods = ['POST'])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")

    if len(username) < 6 or email == "":
        return render_template("register_page.html", error = "Username not long enough")
    elif len(email)<6 or email == "":
        return render_template("register_page.html", error = "Email is not valid")
    elif len(password) < 8 or str(password) == "":
        return render_template("register_page.html", error = "Your password is too small")
    elif password != confirmPassword:
        return render_template("register_page.html", error = "The password don't match")
    else:
        return render_template("register_page.html", error = False)

