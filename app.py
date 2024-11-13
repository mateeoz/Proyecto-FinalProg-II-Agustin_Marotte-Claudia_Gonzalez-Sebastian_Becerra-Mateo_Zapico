from config import app
from flask import render_template, redirect, url_for, flash, request, session
from models import db, User
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('index'))  
        else:
            flash('Su usuario o contraseña es incorrecto.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cuenta creada con éxito', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/index')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('Cerraste sesión', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
