from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    email = "";
    username = "";
    password = "";

class InputForm(FlaskForm):
    def setup(self, name, num_cycles, num_breathes, cycle_time):
        self.name = name;
        self.num_cycles = num_cycles;
        self.num_breathes = num_breathes;
        self.cycle_time = cycle_time;

class LoginForm(FlaskForm):
        username = "";
        password = "";

class UsernameForm(FlaskForm):
        username = "";

class PasswordForm(FlaskForm):
        email = "";

class PasswordResetForm(FlaskForm):
        password = "";