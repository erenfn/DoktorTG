from flask import Blueprint

bp = Blueprint('api', __name__)
payload = Blueprint('payload', __name__)

from app.api import user_routes, \
                    doctor_routes
