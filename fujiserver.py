"""Flask site for Fuji chat webapp."""

from flask import Flask, session, render_template, request, flash, redirect
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Message, Chatroom
from datetime import datetime

app = Flask(__name__)
app.secret_key = "iloayrengreblime"


# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined

# To fake data base to start it. Later need to create a database, a Message Class
# that has at least 3 attr(message, author, timestamp). Eventually making it to 
# SQLAchemy db. 
MESSAGES = []

@app.route("/")
def loginpage():
    """Provide login form."""

    # A dictionary of language options with it's keys. Key as html option id
    # dict[key] as language options. 

    lang_option = {"eng": "English", "swe": "Swedish", "chin": "Chinese", 
               "span": "Spanish", "fren": "French"}

    return render_template("loginpage.html",
                           lang_option=lang_option)


@app.route("/login", methods=['POST'])
def logininfo():
    """Login for the chatpage."""

    user_name = request.form.get("username")
    user_lang = request.form.get("userlang")

    # if session[user_name] = True:
    #     flash("Welcome back!")
    #     return redirect('/feedpage')

@app.route("/feedpage")
def feedpage():
    """Show entire chat feed."""

    return render_template('feedpage.html')

@app.route("/feedpage", methods=['POST'])
def add_messages():
    """Add meesages to Message database"""

    messages = request.form.get("messages")
    author_id = 1
    timestamp = datetime.now()
    chatroom_id = 1
    # change timestap to timestamp same goes to model.py!!!!
    new_message = Message(author_id=author_id, timestap=timestamp,
                          texts=messages, chatroom_id=chatroom_id)

    db.session.add(new_message)
    db.session.commit()

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


