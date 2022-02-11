import uuid

from flask import render_template, redirect, url_for, flash, current_app, session

from .utils import check_email, hash_password, check_user
from .forms import RegisterForm, LoginForm

from webtemplate.repo.models import User


def registration():
    form = RegisterForm()

    return render_template('registration.html', form=form)


def register_user():
    con = current_app.get_connection()
    form = RegisterForm()

    if form.validate_on_submit():
        ident = uuid.uuid4().hex[:32]
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        if check_email(email):
            user = User(
                ident=ident,
                name=first_name.lower() + '_' + last_name.lower(),
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hash_password(password),
            )
            con.set_user(user)

            flash('Sie sind nun registriert.', category='alert alert-success')
            return redirect(url_for('login'))

        else:
            flash('Diese E-Mail Adresse ist bereits vergeben. Bitte wählen Sie eine neune.', category='alert, alert-error')
            return redirect(url_for('registration'))

    else:
        flash('Die Registrierung hat nicht geklappt.', category='alert alert-error')
        return redirect(url_for('registration'))


def login():
    form = LoginForm()

    return render_template('login.html', form=form)


def login_user():
    con = current_app.get_connection()
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = con.get_user(email=email)

        if check_user(email, password) and user:

            current_app.login(user)
                
            flash('Sie sind nun eingeloogt.', category='alert alert-success')
            return redirect(url_for('home'))
            
        else:
            flash('Passwort oder E-Mail Adresse stimmen nicht.', category='alert alert-error')
            return redirect(url_for('login'))

    else:
        flash('Login hat nicht funktioniert.', category='alert alert-error')
        return redirect(url_for('login'))


def logout():
    con = current_app.get_connection()

    try:
        con.logout()
        flash('Sie sind nun ausgeloggt.', category='alert alert-success')
    except:
        session.clear()
        flash('Sie sind nun ausgeloggt.', category='alert alert-success')
    
    return redirect(url_for('home'))