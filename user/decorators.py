from functools import wraps
from flask import request, jsonify
import datetime

from user.models import User, Access

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get('X-USER-ID')
        user_token = request.headers.get('X-USER-TOKEN')

        if user_id is None or user_token is None:
            return jsonify({}), 403

        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return jsonify({}), 403

        access = Access.objects.filter(user=user).first()
        if not access:
            return jsonify({}), 403
        if access.token != user_token:
            return jsonify({}), 403
        if access.expires < datetime.datetime.utcnow():
            return jsonify({'error': "TOKEN_EXPIRED"}), 403

        return f(*args, **kwargs)
    return decorated_function