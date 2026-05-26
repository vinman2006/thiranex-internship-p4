from flask import (
Flask,
render_template,
request,
redirect,
session
)

import sqlite3

from flask_bcrypt import (
Bcrypt
)

app = Flask(__name__)

app.secret_key="super_secret_key"

bcrypt=Bcrypt(app)


def db():

    return sqlite3.connect(
        "users.db"
    )


def create():

    conn=db()

    conn.execute("""

CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY,

username TEXT UNIQUE,

password TEXT

)

""")

    conn.close()


create()


@app.route("/")

def home():

    if "user" not in session:

        return redirect(
            "/login"
        )

    return render_template(
        "dashboard.html",
        user=session["user"]
    )


@app.route(
"/register",

methods=[
"GET",
"POST"
]
)

def register():

    if request.method=="POST":

        username=request.form[
            "username"
        ]

        password=request.form[
            "password"
        ]

        if len(password)<8:

            return "Password too short"

        hashed=bcrypt.generate_password_hash(
            password
        ).decode()

        conn=db()

        try:

            conn.execute(

"INSERT INTO users(username,password) VALUES (?,?)",

(
username,
hashed
)

)

            conn.commit()

            return redirect(
                "/login"
            )

        except:

            return "User exists"

    return render_template(
        "register.html"
    )


@app.route(
"/login",

methods=[
"GET",
"POST"
]
)

def login():

    if request.method=="POST":

        username=request.form[
            "username"
        ]

        password=request.form[
            "password"
        ]

        conn=db()

        cur=conn.cursor()

        cur.execute(

"SELECT password FROM users WHERE username=?",

(
username,
)

)

        row=cur.fetchone()

        if row:

            if bcrypt.check_password_hash(

                row[0],

                password

            ):

                session[
                    "user"
                ]=username

                return redirect(
                    "/"
                )

        return "Invalid Login"

    return render_template(
        "login.html"
    )


@app.route(
"/logout"
)

def logout():

    session.clear()

    return redirect(
        "/login"
    )


if __name__=="__main__":

    app.run(
        debug=True
    )
