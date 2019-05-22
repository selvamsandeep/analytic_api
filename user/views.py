from flask import Blueprint

from user.api import UserAPI, AccessAPI

user_app = Blueprint('user_app', __name__)

user_view = UserAPI.as_view('user_api')
user_app.add_url_rule('/users/', view_func=user_view, methods=['POST',])


access_view = AccessAPI.as_view('access_api')
user_app.add_url_rule('/user/access_token/', view_func=access_view, methods=['POST',])
