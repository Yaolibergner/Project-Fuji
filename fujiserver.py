"""Flask site for Fuji chat webapp."""

from flask import Flask, session, render_template, request, flash, redirect
import jinja2

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

# Right a quick testing for main.js. This function is just to render fake message
# here as random number and passing it to feedpage. 

from random import choice
@app.route('/messages')
def get_random_num():

    return render_template("messages.html", randomnum=choice([1, 2, 3, 4, 5]))


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
