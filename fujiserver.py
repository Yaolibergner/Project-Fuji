"""Flask site for Fuji chat webapp."""

from flask import Flask, session, render_template, request, flash, redirect
import jinja2

app = Flask(__name__)
app.secret_key = "iloayrengreblime"


# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so
#set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


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





#------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
