"""Flask site for Fuji chat webapp."""

from flask import Flask, session, render_template, request, flash, redirect, url_for, g
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Message, Chatroom, UserRoom, Translation
from datetime import datetime
from translate import translate_text
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']


# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


# Use g the thread local to check if a user is logged in. 
# https://stackoverflow.com/questions/13617231/how-to-use-g-user-global-in-flask
# before any request, assign g.
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
# http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
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
        return redirect("/register")

    if user.password != password:
        flash('Invalid password, please try again!')
        return redirect("/")

    session["user_id"] = user.user_id

    return redirect("/feedpage")

@app.route("/logout")
def logout():
    """User log out."""

    del session["user_id"]
    flash("You are logged out, see you soon.")
    return redirect("/")


@app.route("/feedpage")
@login_required
def feedpage():
    """Show entire chat feed."""

    # This page should not be seen for people who aren't login. 
    # http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    # Use login required decorator @login_required.

    return render_template('feedpage.html')

@app.route("/feedpage", methods=['POST'])
def add_message():
    """Add meesages to Message database"""

    message = request.form.get("message")
    author_id = g.user.user_id
    timestamp = datetime.now()
    chatroom_id = 1
    new_message = Message(author_id=author_id, timestamp=timestamp,
                          text=message, chatroom_id=chatroom_id)

    db.session.add(new_message)
    # Messages on line 60 will be passed in to be translated. 
    # Call detect_language(text) and translate_text(target, text) functions. 

    languages = db.session.query(User.language).distinct()
    # Loop over all existing user distinct languages. And translate the original message
    # to each language. Add translated messages to database.
    for language in languages:
        # languages returns a list of tuples. language is still a tuple of one element.
        # index language[0] to fix it. 
        trans_text = translate_text(language[0], message).translated_text
        message_id = new_message.message_id
        new_translation = Translation(message_id=message_id, trans_text=trans_text,
                                      language=language)
        db.session.add(new_translation)
    
    db.session.commit()

    return ""
    

@app.route("/messages")
def show_messages():
    """Show messages on feedpage"""

    messages = Message.query.all()
    # translation_list = [""]

    for message in messages:
        # message.translation gives list of objects. All the translation for the 
        # language. Here assgin it to one trans_text based on user's language
        # selection. 
        message.translation = Translation.query.filter_by(language=g.user.language, 
                                            message_id=message.message_id).first()

    return render_template("messages.html", messages=messages, user=g.user)
                          
    

#------------------------------------------------------------------------------#
if __name__ == "__main__": # pragma: no cover

    app.debug = True

    connect_to_db(app)
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


