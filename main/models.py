from main import db

class User(db.Model):
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(64), unique=True, primary_key=True)
    password = db.Column(db.String(120), unique=False)
    verified = db.Column(db.Boolean, unique=False)
    name = db.Column(db.String(64), unique=False)
    num_cycles = db.Column(db.String(64), unique=False)
    num_breathes = db.Column(db.String(64), unique=False)
    cycle_time = db.Column(db.String(64), unique=False)

    def __repr__(self):
        return 'Username: {}\nPassword: {}'.format(self.username, self.password)