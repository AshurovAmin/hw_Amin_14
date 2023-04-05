from flask_login import UserMixin

from . import db, bcrypt, login_manager


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(100))
    value = db.Column(db.Integer)
    status = db.Column(db.String(40))
    unit = db.Column(db.String(60))
    subject = db.Column(db.String(255))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


