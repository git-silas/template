import uuid

from flask import render_template, redirect, url_for, flash, current_app

#from .utils import check_email, check_user
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

        if email:
            user = User(
                ident=ident,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email:
            flash('Sie sind nun eingeloogt.', category='alert alert-success')
            return redirect(url_for('home'))

        else:
            flash('Passwort oder E-Mail Adresse stimmen nicht.', category='alert alert-error')
            return redirect(url_for('login'))

    else:
        flash('Login hat nicht funktioniert.', category='alert alert-error')
        return redirect(url_for('login'))


def logout():
    
    flash('Sie sind nun ausgeloggt.', category='alert alert-success')
    

    return render_template('logout.html')