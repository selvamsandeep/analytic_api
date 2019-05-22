from application import db

class User(db.Document):
    user_id = db.StringField(db_field="ui", unique=True)
    password = db.StringField(db_field="up")
    domain   =  db.StringField(db_field="d")
    meta = {
        'indexes': [('user_id')]
    }

class Access(db.Document):
    user = db.ReferenceField(User, db_field="u")
    token = db.StringField(db_field="t")
    expires = db.DateTimeField(db_field="e")



