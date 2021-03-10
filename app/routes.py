from flask import Flask, render_template, url_for, flash, redirect, request;
from app import app, db, bcrypt;
from app.forms import LoginForm, RegistrationForm, QuestionForm;
from app.models import User;
from flask_login import login_user, current_user, logout_user, login_required;

@app.route("/")
@app.route('/home')
def home():
    logged_in = current_user.is_authenticated;
    return render_template("home.html", title="home", is_logged_in=logged_in);

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm();
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first();
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data);
            next_page = request.args.get('next');
            flash(f"You have been logged in!","info");
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger');
            return redirect(url_for('login'))
        
    return render_template("login.html", form=form);

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm();
    if(form.validate_on_submit()): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8');
        user = User(username=form.username.data, email=form.email.data, password=hashed_password);
        db.session.add(user);
        db.session.commit();
        flash(f'Account created for {form.username.data}!','info');
        return redirect(url_for('home'));
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user();
    return redirect(url_for('home'));

@app.route('/create')
@login_required
def create():
    form = QuestionForm();
    return render_template('create.html',is_logged_in=current_user.is_authenticated, form=form);

