from main import app
from main.config import Config

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from flask import render_template

#import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": 'abreezemail@gmail.com',
    "MAIL_PASSWORD": 'Fellow3.0!'
}
app.config.update(mail_settings)
mail = Mail(app)



def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=Config.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False

    return email

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=mail_settings['MAIL_USERNAME']
    )
    with app.app_context():
        mail.send(msg)

def generate_send_email(email, template):
    generate_confirmation_token(email)
    send_email(email, Config.MAIL_SUBJECT, template)


#SendGrid config and run
def create_message(to, html):
    message = Mail(
        from_email='abreezemail@gmail.com',
        to_emails=to,
        subject='Meditation App Verification',
        html_content=html
    )

    return message

def sendgrid_send(to, html):
    try:
        message = create_message(to, html)
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)