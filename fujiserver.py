"""Flask site for Fuji chat webapp."""

from flask import Flask, session, render_template, request, flash, redirect, url_for, g
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Message, Chatroom
from datetime import datetime
from translate import translate_text
from functools import wraps

app = Flask(__name__)
app.secret_key = "iloayrengreblime"


# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


# Use g the thread local to check if a user is logged in. 
# https://stackoverflow.com/questions/13617231/how-to-use-g-user-global-in-flask

@app.before_request
def load_user():
    """Check if user logged in for each route below."""
    if session.get("user_id"):
        user = User.query.filter_by(user_id=session["user_id"]).first()
    else: 
        user = None
    g.user = user

# Add a login_required decorator. This is to protect feedpage not being showed 
# if user not logged in.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("loginpage", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/register')
def register_form():
    """Show form for user signup."""

    # A dictionary of language options with it's keys. Key as html option id
    # dict[key] as language options. 
    lang_option = {"en": "English", "sv": "Swedish", "zh-CN": "Chinese", 
               "es": "Spanish", "fr": "French", "ru": "Russian"}


    return render_template("register.html", lang_option=lang_option)


@app.route('/register', methods=['POST'])
def add_user():
    """Process registration. Add registered user to database."""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    language = request.form.get("language")

    new_user = User(email=email, password=password,fname=fname,
                    lname=lname,language=language)

    db.session.add(new_user)
    db.session.commit()

    #flash(f"User {email} added.")
    return redirect("/")

@app.route("/")
def loginpage():
    """Provide login form."""

    return render_template("loginpage.html")


@app.route("/login", methods=['POST'])
def logininfo():
    """Login for the chatpage."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    # import pdb; pdb.set_trace()
    if not user:
        # flash('No such user')
        return redirect("/register")

    if user.password != password:
        #flash('Invalid password')
        return redirect("/")

    session["user_id"] = user.user_id
    #flash("Welcome, you are logged in.")
    return redirect("/feedpage")

@app.route("/logout")
def logout():
    """User log out."""

    del session["user_id"]
    #flash("Logged out.")
    return redirect("/")


@app.route("/feedpage")
@login_required
def feedpage():
    """Show entire chat feed."""

    # This page should not be seen for people who aren't login. 
    # http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    # Use login required decorator.

    return render_template('feedpage.html')

@app.route("/feedpage", methods=['POST'])
def add_message():
    """Add meesages to Message database"""

    message = request.form.get("message")
    author_id = session["user_id"]
    timestamp = datetime.now()
    chatroom_id = 1
    # change timestap to timestamp same goes to model.py!!!!
    new_message = Message(author_id=author_id, timestamp=timestamp,
                          text=message, chatroom_id=chatroom_id)

    db.session.add(new_message)
    db.session.commit()

    # Messages on line 60 will be passed in to be translated. 
    # Call detect_language(text) and translate_text(target, text) functions. 
    # Difficulties: how to solve the target arg? I can use user's id and their
    # selected lang_code to learn what language does the user want to be translated.
    # But how to present different language to the screen of different users?

    # translated_message = translate_text('zh-CN', messages).translated_text

    return redirect("/feedpage")

@app.route("/messages")
def show_messages():
    """Show messages on feedpage"""

    messages = Message.query.all()

    return render_template("messages.html", messages=messages)
    

#------------------------------------------------------------------------------#
if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


