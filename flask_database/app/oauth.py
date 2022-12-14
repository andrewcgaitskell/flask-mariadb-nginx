# app/oauth.py

import os

from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

from app.models import db, OAuth, User

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

GITHUB_OAUTH_CLIENT_ID = environ.get("GITHUB_OAUTH_CLIENT_ID")
GITHUB_OAUTH_CLIENT_SECRET = environ.get("GITHUB_OAUTH_CLIENT_SECRET")

github_blueprint = make_github_blueprint(
    client_id=GITHUB_OAUTH_CLIENT_ID,
    client_secret=GITHUB_OAUTH_CLIENT_SECRET,
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)

# setup SQLAlchemy backend
# github_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)


def github_logged_in(github_blueprint, token):
    if not token:
        flash("Failed to log in with GitHub.", category="error")
        return False

    resp = github_blueprint.session.get("/user")
    if not resp.ok:
        msg = "Failed to fetch user info from GitHub."
        flash(msg, category="error")
        return False

    github_info = resp.json()
    github_user_id = str(github_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=github_blueprint.name,
        provider_user_id=github_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=github_blueprint.name,
            provider_user_id=github_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with GitHub.")

    else:
        # Create a new local user account for this user
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on GitHub!
            email=github_info["email"],
            name=github_info["name"],
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with GitHub.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(github_blueprint)
def github_error(github_blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=github_blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")
