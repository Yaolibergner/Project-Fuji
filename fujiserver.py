"""Flask site for Fuji chat webapp."""

from flask import Flask, session, render_template, request, flash, redirect
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Message, Chatroom
from datetime import datetime
from translate import translate_text

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

@app.route('/register')
def register_form():
    """Show form for user signup."""

    # A dictionary of language options with it's keys. Key as html option id
    # dict[key] as language options. 
    lang_option = {"eng": "English", "swe": "Swedish", "chin": "Chinese", 
               "span": "Spanish", "fren": "French", "rus": "Russian"}


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

@app.route("/logout", methods=["POST"])
def logout():
    """User log out."""

    del session["user_id"]
    #flash("Logged out.")
    return redirect("/")


@app.route("/feedpage")
def feedpage():
    """Show entire chat feed."""

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


