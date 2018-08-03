"""Models and database functions for Fuji project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of the chatapp."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=True)
    language = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User user_id={self.user_id} email={self.email}
                    fname={self.fname} language={self.language}>"""


class Message(db.Model):
    """User messages."""

    __tablename__ = "messages"

    message_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    timestap = db.Column(db.DateTime)
    texts = db.Column(db.String(3000))

    # Define relationship to user.
    user = db.relationship("User",
                           backref=db.backref("messages", order_by=message_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<texts={self.texts} timestap={self.timestap} 
                   author_id={self.author_id}>"""


class Chatroom(db.Model):
    """Chatrooms."""

    __tablename__ = "chatrooms"

    chatroom_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('messages.message_id'))

    # Define relationship to message.
    message = db.relationship("Message",
                           backref=db.backref("chatrooms", order_by=chatroom_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Chatroom chatroom_id={self.chatroom_id} chat_id={self.chat_id}>"

# Do not need the below middle table, one message belongs to one chatroom.
# class MessageRoom(db.Model):
#     """Association table for Message and Chatroom table."""

#     __tablename__ = "messagerooms"

#     messageroom_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)

class UserRoom(db.Model):       
    """Association table for User and Chatroom."""

    # User can be in multiple Chatrooms. Chatrooms can have many users.
    # Build the connection between User and Chatroom tables.
    # Each row will be a pair of one room and one user. 
    __tablename__ = "userrooms"

    userroom_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("chatrooms.chatroom_id"), nullable=False)

    user = db.relationship("User", backref="userrooms")
    chatroom = db.relationship("User", backref="userrooms")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Userroom userroom_id = {self.userroom_id}>"""


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fuji'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from fujiserver import app
    connect_to_db(app)
    print("Connected to DB.")
