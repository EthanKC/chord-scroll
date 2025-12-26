import os
os.environ["TERM"] = "dumb"

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, error

# Configure application
app = Flask(
	__name__,
	template_folder=os.path.join(os.path.dirname(__file__), "templates"),
	static_folder=os.path.join(os.path.dirname(__file__), "static")
 )
app.secret_key = 'gG45agd2fa2dg45df64saf51adf451'

# Configure session to use filestystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(
	os.path.dirname(__file__), 
	"flask_session"

)

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///" + os.path.join(os.path.dirname(__file__), "chord-scroll.db"))


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Display saved songs"""
    # Query database for all songs saved by user
    songs = db.execute("SELECT s.title, s.id, s.artist, t.type, g.genre FROM songs s, type t, genre g WHERE s.user_id = ? AND t.id = s.type_id AND g.id = s.genre_id", session["user_id"])
    return render_template("index.html", songs=songs) 


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.pop("user_id", None)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must Provide Username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Provide Password")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid Username and/or Password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    questions = db.execute("SELECT * FROM security")
    question = request.form.get("securityQuestion")
    answer = request.form.get("securityAnswer")

    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            flash("Must Provide Username")
            return redirect("/register")

        # Ensure password was submitted
        elif not password:
            flash("Must Provide Password")
            return redirect("/register")

        # Ensure password and confirm password match
        elif password != confirmation:
            flash("Passwords Don't Match")
            return redirect("/register")

        # Validate security question
        elif not question:
            flash("Must Choose Question")
            return redirect("/register")

        # Validate security answer
        elif not answer:
            flash("Must provide answer")
            return redirect("/register")

        else:
            db.execute("INSERT INTO users (username, hash, security_question, security_answer_hash) VALUES(?, ?, ?, ?)", username, generate_password_hash(password), question, generate_password_hash(answer))
            flash("Successfully Registered")
            return redirect("/login")
    return render_template("register.html", questions=questions)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/account")
@login_required
def account():
    """Account info"""

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = username[0]["username"]

    return render_template("account.html", username=username)


@app.route("/password_reset", methods=["GET", "POST"])
@login_required
def password_reset():
    """Reset password"""

    if request.method == "POST":
        oldPassword = request.form.get("oldPassword")
        newPassword = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate entries
        if not oldPassword:
            flash("Old Password Required")
            return redirect("/password_reset")

        elif not newPassword:
            flash("New Password Required")
            return redirect("/password_reset")

        elif not confirmation:
            flash("Confirm Password Required")
            return redirect("/password_reset")

        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure oldPassword is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("oldPassword")):
            flash("Invalid Password")
            return redirect("/password_reset")

        # Ensure newPassword and confirmation match
        elif newPassword != confirmation:
            flash("New Password Mismatch")
            return redirect("/password_reset")

        # Update database with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(newPassword), session["user_id"])
        flash("Password Updated")
        return redirect("/account")

    return render_template("password_reset.html")


@app.route("/forgot_password_u", methods=["GET", "POST"])
def forgot_password_u():
    """Forgot Password - Prep for Reset"""

    if request.method == "POST":
        username = request.form.get("username")

        # Ensure username was entered
        if not username:
            flash("Missing Username")
            return redirect("/forgot_password_u")
        
        # Validate username exists in database
        user = db.execute("SELECT id FROM users WHERE username = ?", username)
        if not user:
            flash("User Not Found")
            return redirect("/forgot_password_u")
        
        # Query database for users chosen security question
        questionID = db.execute("SELECT security_question FROM users WHERE id = ?", user[0]["id"])
        question = db.execute("SELECT question FROM security WHERE id = ?", questionID[0]["security_question"])
        question = question[0]["question"]
        session["temp_user_id"] = user[0]["id"]

        return render_template("forgot_password.html", question=question)

    return render_template("forgot_password_username.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Forgot Password - Reset Password"""

    if request.method == "POST":
        answer = request.form.get("answer")
        newPassword = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate entries
        if not answer:
            flash("Security Answer Required")
            return redirect("/forgot_password")

        elif not newPassword:
            flash("New Password Required")
            return redirect("/forgot_password")

        elif not confirmation:
            flash("Confirm Password Required")
            return redirect("/forgot_password")

        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["temp_user_id"])

        # Ensure answer to security question is correct
        if not check_password_hash(rows[0]["security_answer_hash"], answer):
            flash("Invalid Answer")
            return redirect("/forgot_password")

        # Ensure newPassword and confirmation match
        elif newPassword != confirmation:
            flash("New Password Mismatch")
            return redirect("/forgot_password")

        # Update database with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(newPassword), session["temp_user_id"])

        flash("Password Successfully Reset")
        return redirect("/login")

    return render_template("forgot_password_username.html")

@app.route("/new", methods=["GET","POST"])
@login_required
def new():
    """Input New Song"""

    if request.method == "POST":
        title = request.form.get("title")
        artist = request.form.get("artist")
        song = request.form.get("song")
        typeID = request.form.get("type")
        genreID = request.form.get("genre")

        # Ensure title was submitted
        if not title:
            flash("Title Required")
            return redirect("/new")
        
        # Ensure genre was submitted
        if not genreID:
            flash("Genre Required")
            return redirect("/new")

        # Ensure valid genre was submitted
        genreCheck = db.execute("SELECT id FROM genre WHERE id = ?", genreID)
        if not genreCheck:
            flash("Invalid Genre")
            return redirect("/new")
        
        # Ensure type was submitted
        if not typeID:
            flash("Type Required")
            return redirect("/new")

        # Ensure valid type was submitted
        typeCheck = db.execute("SELECT id FROM type WHERE id = ?", typeID)
        if not typeCheck:
            flash("Invalid Type")
            return redirect("/new")
        
        # Ensure song was submitted
        if not song:
            flash("Song Required")
            return redirect("/new")

        # Input new song into database
        if artist:
            db.execute("INSERT INTO songs (title, artist, song_text, type_id, genre_id, user_id) VALUES(?,?,?,?,?,?)", title, artist, song, typeID, genreID, session["user_id"])
        else:
           db.execute("INSERT INTO songs (title, song_text, type_id, genre_id, user_id) VALUES(?,?,?,?,?)", title, song, typeID, genreID, session["user_id"])
        
        flash("Song Saved")
        return redirect("/new")

    else:

        # Query database for genre and type options
        genres = db.execute("SELECT * FROM genre")
        types = db.execute("SELECT * FROM type")
        return render_template("new.html", genres=genres, types=types)

@app.route("/song/<title>_<int:id>", methods=["GET"])
@login_required
def song(title, id):
    """Display song"""

    # Query database for saved song
    song = db.execute("SELECT s.id, s.title, s.artist, s.song_text, t.type, g.genre FROM songs s, type t, genre g WHERE s.user_id = ? AND s.id = ? AND t.id = s.type_id AND g.id = s.genre_id", session["user_id"], id)

    # Validate and display song
    if song:
        song = song[0]
        return render_template("song.html", song=song)
    else:
        return error("Song Not Found", "404")

@app.route("/song/<title>_<int:id>/edit", methods=["GET","POST"])
@login_required
def edit(title, id):
    """Edit song"""

    if request.method == "POST":
        songTitle = request.form.get("title")
        artist = request.form.get("artist")
        song = request.form.get("song")
        songID = request.form.get("id")
        typeID = request.form.get("type")
        genreID = request.form.get("genre")
        redir = f"/song/{title}_{id}/edit"

        # Ensure title was submitted
        if not songTitle:
            flash("Title Required")
            return redirect(redir)
        
        # Ensure genre was submitted
        if not genreID:
            flash("Genre Required")
            return redirect(redir)

        # Ensure valid genre was submitted
        genreCheck = db.execute("SELECT id FROM genre WHERE id = ?", genreID)
        if not genreCheck:
            flash("Invalid Genre")
            return redirect(redir)
        
        # Ensure type was submitted
        if not typeID:
            flash("Type Required")
            return redirect(redir)

        # Ensure valid type was submitted
        typeCheck = db.execute("SELECT id FROM type WHERE id = ?", typeID)
        if not typeCheck:
            flash("Invalid Type")
            return redirect(redir)
        
        # Ensure song was submitted
        if not song:
            flash("Song Required")
            return redirect(redir)

        # Update existing song in database
        if artist:
            db.execute("UPDATE songs SET title=?, artist=?, song_text=?, type_id=?, genre_id=? WHERE id =? AND user_id =?", title, artist, song, typeID, genreID, id, session["user_id"])
        else:
           db.execute("UPDATE songs SET title=?, artist=?, song_text=?, type_id=?, genre_id=? WHERE id =? AND user_id =?", title, "No Artist", song, typeID, genreID, id, session["user_id"])
        
        flash("Song Saved")
        return redirect(f"/song/{title}_{id}")

    else:

        # Query database for existing song information to display
        song = db.execute("SELECT s.id, s.title, s.artist, s.song_text, s.type_id, t.type, s.genre_id, g.genre FROM songs s, type t, genre g WHERE s.user_id = ? AND s.id = ? AND t.id = s.type_id AND g.id = s.genre_id", session["user_id"], id)
        if song:
            song = song[0]
            genres = db.execute("SELECT * FROM genre")
            types = db.execute("SELECT * FROM type")
            return render_template("edit.html", song=song, genres=genres, types=types)
        else:
            return error("Song Not Found", "404")
        
@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """Delete song"""

    id = request.form.get("id")

    # Validate song exists and delete song
    if id:
        db.execute("DELETE FROM songs WHERE id = ? AND user_id = ?", id, session["user_id"])
        flash("Song Deleted")
        return redirect("/")
    else:
        flash("Error: id not found on song table")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
