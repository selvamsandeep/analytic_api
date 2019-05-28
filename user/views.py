from flask import Blueprint

from user.api import UserAPI, AccessAPI, UserDetailsAPI

user_app = Blueprint('user_app', __name__)

user_view = UserAPI.as_view('user_api')
user_app.add_url_rule('/users/', view_func=user_view, methods=['POST',])


access_view = AccessAPI.as_view('access_api')
user_app.add_url_rule('/auth/', view_func=access_view, methods=['POST',])

user_details_view = UserDetailsAPI.as_view('user_details_api')
user_app.add_url_rule('/user_domain/', view_func=user_details_view, methods=['GET',])