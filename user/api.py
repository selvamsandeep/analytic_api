from flask.views import MethodView
from flask import request, abort, jsonify
import bcrypt
import uuid
from datetime import datetime, timedelta

from user.models import User, Access


class UserAPI(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        if not "user_id" in request.json or not "password" in request.json:
            error = {
                "code": "MISSING_USER_ID_OR_PASSWORD"
            }
            return jsonify({'error': error}), 400
        existing_user = User.objects.filter(user_id=request.json.get('user_id')).first()
        if existing_user:
            error = {
                "code": "USER_ID_ALREADY_EXISTS"
            }
            return jsonify({'error': error}), 400
        else:
            # create the credentials
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(request.json.get('password'), salt)
            user = User(
                user_id=request.json.get('user_id'),
                password=hashed_password,
                domain=request.json.get('domain'),
            ).save()
            return jsonify({'result': 'ok'})


class AccessAPI(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        if not "user_id" in request.json or not "password" in request.json:
            error = {
                "code": "MISSING_USER_ID_OR_PASSWORD"
            }
            return jsonify({'error': error}), 400

        user = User.objects.filter(user_id=request.json.get('user_id')).first() 
        #print(user.get('domain'))
        print(user.domain)               
        if not user:
            error = {
                "code": "INCORRECT_CREDENTIALS"
            }
            return jsonify({'error': error}), 403
        else:
            # generate a token
            if bcrypt.hashpw(request.json.get('password'), user.password) == user.password:
                # delete existing tokens
                existing_tokens = Access.objects.filter(user=user).delete()
                token = str(uuid.uuid4())
                now = datetime.utcnow()                
                expires = now + timedelta(minutes=60)
                ##print(now, expires)
                access = Access(
                    user=user,
                    token=token,
                    expires=expires
                ).save()
                expires_3339 = expires.isoformat("T") + "Z"
                return jsonify({'token': token, 'domain':user.domain, 'expires': expires_3339}), 200
            else:
                error = {
                    "code": "INCORRECT_CREDENTIALS"
                }
                return jsonify({'error': error}), 403