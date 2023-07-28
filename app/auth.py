from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models.user_models import User


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None



