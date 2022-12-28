import os
from tkinter import INSERT
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

entries = {}
entryId = {}
entry = {}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#delete makes sure to return user to the same page were the delete button was clicked. if page is Sent the return to send , otherwise return to index(inbox page)
@app.route("/entry/delete-entry", methods=["POST"])
def delete_entry():
    page = request.form.get("page")
    entryId = request.form.get("entryId")
    if entryId:
        db.execute("DELETE from entries where id = ?", entryId)

    flash("Entry Deleted",)
    if page == "sent":
        return redirect("/sent")
    else:
        return redirect("/")


# home page route
@app.route("/home")
@login_required
def home():
    """Show entries"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    entries = db.execute("SELECT * FROM entries WHERE recipient = ?", username)
    return render_template("home.html", entries=entries)


#inbox page displaying entries (mainly for admin)
@app.route("/")
@login_required
def index():
    """Show entries"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    entries = db.execute("SELECT * FROM entries WHERE recipient = ? ORDER BY timestamp DESC", username)
    return render_template("index.html", entries=entries, entryId=entryId)


#compose route meant to attain user id for when entry is submitted
@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """Buy shares of stock"""
    if request.method == "GET":
        userId = session["user_id"]
        senderDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        sender = senderDB[0]["username"]
        return render_template("compose.html", sender=sender)

    else:
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        van = request.form.get("van")
        body = request.form.get("body")

        #making sure entries are only digits and not negative or past 99 while returning van as an int
        if not van.isdigit() or not (1 <= int(van) <= 99):
            return apology("Sorry, only integers between 1 and 99 are allowed", 403)
        van = int(van)

    #if not sender or not recipient or not subject or not body:
    if not van and not body:
        return apology("invalid username and/or password", 403)

    db.execute("INSERT INTO entries (sender, recipient, van, body) VALUES (?, ?, ?, ?)", sender,recipient, van, body)
    flash("Entry Succesfully Sent")
    return redirect("/sent")

#Sent route organzing by timestamp order
@app.route("/sent", methods=["GET", "DELETE"])
@login_required
def sent():
    """Sent entries"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    entries = db.execute("SELECT * FROM entries WHERE sender = ? ORDER BY timestamp ASC", username)
    return render_template("sent.html", entries=entries)


#entry route made to display entry from entries with the correct id
@app.route("/entry", methods=["GET", "POST"])
@login_required
def entry():
    if request.method == "POST":
        entryId = request.form.get("entryId")
        entryDetailDB = db.execute("SELECT * FROM entries WHERE id = ?", entryId)
        entryDetail = entryDetailDB[0]
        return render_template("entry.html", entryDetail=entryDetail)


#admin user page makes it have the ability to post a note in notes through the POST method
@app.route("/admin", methods=["GET", "POST"])
def admin_users():
    userId = session["user_id"]
    if userId < 1 or userId > 3:
        return apology("You are not authorized to access this page", 403)
    if request.method == "POST":
        usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        username = usernameDB[0]["username"]
        body = request.form.get("body")
        db.execute("INSERT INTO notes (sender, body) VALUES (?, ?)", username, body)
    notes = db.execute("SELECT * FROM notes")
    return render_template("admin.html", notes=notes)


#admin delete Note so that Notes has its own database of notes
@app.route("/admin/delete-note", methods=["POST"])
def delete_note():
  noteId = request.form.get("noteId")
  if noteId:
    db.execute("DELETE FROM notes WHERE id = ?", (noteId,))
  return redirect("/admin")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/compose")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    #POST section of my code
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username:
            return apology("Username Needed")

        if not password:
            return apology("Must Give Password")

        if not confirm:
            return apology("Must Give Confirmation")

        #Checks to see if passwords match with one another not too complicated with code like expected
        if password != confirm:
            return apology("Passwords Do Not Match")

        hash = generate_password_hash(password)

        try:
            #INSERT INTO table_name (column1, column2, column3,..)    VALUES (value1, value2, value3,..)
            new_user = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("Username already exists")

        session["user_id"] = new_user



        return redirect("/")

