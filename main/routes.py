from main import app, db
from main.form import InputForm, LoginForm, UserForm, UsernameForm, PasswordForm
from main.models import User
from main.verify import generate_confirmation_token, generate_send_email, confirm_token, sendgrid_send

from flask import render_template, request, redirect, session, url_for

#global variables
empty = 0
cycle_count = 0

#base url redirect
@app.route('/')
def redirect_to_input():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    session['input_array'] = [False, False, False]

    #reset empty counter
    global empty
    empty = 0
    form = LoginForm()


    if form.validate_on_submit():

        #get login info from form
        form.username = request.form['username']
        form.password = request.form['password']

        user_login = db.session.query(User).filter_by(username=form.username).first()
        if user_login:
            if form.password != user_login.password:
                return render_template('login.html', wrong_pass=True, form=form)
            else:
                session['username'] = user_login.username
                if user_login.verified:
                    return redirect(url_for('input_page'))
                else:
                    return redirect(url_for('verify'))
        else:
            return redirect(url_for('create_user'))

    return render_template('login.html', form=form)

@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if db.session.query(User).filter_by(email=email).first():
            if db.session.query(User).filter_by(username=username).first():
                return render_template('create_user.html', email_password=True, form=form)
            else:
                return render_template('create_user.html', email=True, form=form)
        if db.session.query(User).filter_by(username=username).first():
            return render_template('create_user.html', username=True, form=form)
        user = User(email=email, username=username, password=password, verified=False, name="", num_cycles="", num_breathes="", cycle_time="")
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['email'] = email
        return redirect(url_for('verify'))
    return render_template('create_user.html', form=form)

@app.route('/input/<email>', methods=['GET', 'POST'])
def input_page(email):
    global empty
    global cycle_count
    cycle_count = 0

    user_info = db.session.query(User).filter_by(email).first()
    if not user_info.verified:
        return redirect(url_for('verify'))
    form = InputForm()
    form.setup(user_info.name, user_info.num_cycles, user_info.num_breathes, user_info.cycle_time)
    if form.validate_on_submit():
        #reset empty counter
        empty = 0
        user_info.name = request.form['name']
        user_info.num_cycles = request.form['num_cycles']
        user_info.num_breathes = request.form['num_breathes']
        user_info.cycle_time = request.form['cycle_time']

        #run input checks
        try:
            int(user_info.num_cycles)
        except ValueError:
            session['input_array'][0] = True
        else:
            if not (int(user_info.num_cycles) > 0 and int(user_info.num_cycles) <= 10):
                session['input_array'][0] = True
            else:
                session['input_array'][0] = False

        try:
            int(user_info.num_breathes)
        except ValueError:
            session['input_array'][1] = True
        else:
            if not (int(user_info.num_breathes) > 0 and int(user_info.num_breathes) <= 10):
                session['input_array'][1] = True
            else:
                session['input_array'][1] = False

        try:
            int(user_info.cycle_time)
        except ValueError:
            session['input_array'][2] = True
        else:
            if not (int(user_info.cycle_time) > 0 and int(user_info.cycle_time) <= 4):
                session['input_array'][2] = True
            else:
                session['input_array'][2] = False

        #modifying session values
        session.modified = True

        db.session.commit()

        for element in session['input_array']:
            if(element):
                return redirect(url_for('input_page'))

        return redirect(url_for('runtime_breath'))
    empty += 1

    return render_template('input_form.html', input_array=session['input_array'], form=form, empty=empty)

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/verify/sent', methods=["GET", "POST"])
def verify_email():
    user = User.query.filter_by(username=session['username']).first()
    email = user.email
    token = generate_confirmation_token(email)
    url = request.base_url + '/' + token
    sendgrid_send(email, render_template('verify_email.html', confirm_url=url))
    return render_template('verify_sent.html')

@app.route('/verify/sent/<token>')
def confirm_email(token):
    email_confirmation = confirm_token(token)
    if bool(email_confirmation):
        user = User.query.filter_by(email=email_confirmation).first()
        user.verified = 1
        db.session.commit()
        return redirect(url_for('input_page', email=email_confirmation))
    
    return render_template('verify_sent.html')

@app.route('/change-username', methods=['GET', 'POST'])
def username():

    form = UsernameForm()

    if form.validate_on_submit():
        form.username = request.form['username']

        if User.query.filter_by(username=form.username).first():
            return render_template('username.html', user=session['username'], form=form, exists=True)
        else:
            user = User.query.filter_by(username=session['username']).first()
            user.username = form.username

            #commit changes to user
            db.session.commit()
            return redirect(url_for('login_page'))



    return render_template('username.html', user=session['username'], form=form, exists=False)

@app.route('/change-password', methods=['GET', 'POST'])
def password():

    form = PasswordForm()

    if form.validate_on_submit():
        form.password = request.form['password']
        user = User.query.filter_by(username=session['username']).first()
        user.password = form.password

        #commit changes to user
        db.session.commit()
        return redirect(url_for('login_page'))

    return render_template('password.html', user=session['username'], form=form)

@app.route('/runtime-breath')
def runtime_breath():

    global cycle_count

    user = User.query.filter_by(username=session['username']).first()
    data = {
           'name': user.name,
           'num_cycles': user.num_cycles,
           'num_breathes': user.num_breathes,
           'cycle_time': user.cycle_time
    }

    if(cycle_count < int(data['num_cycles'])):
        cycle_count += 1
        return render_template('runtime-breath.html', data=data)

    return redirect(url_for('runtime_end'))


@app.route('/runtime-hold')
def runtime_hold():

    user = User.query.filter_by(username=session['username']).first()
    data = {
        'name': user.name,
        'num_cycles': user.num_cycles,
        'num_breathes': user.num_breathes,
        'cycle_time': user.cycle_time
    }

    return render_template('runtime-hold.html', data=data)

@app.route('/runtime-end')
def runtime_end():

    return render_template('runtime-end.html')