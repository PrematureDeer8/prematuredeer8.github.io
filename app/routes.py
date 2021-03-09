from flask import Flask, render_template, url_for, flash, redirect;
from app import app;
from app.forms import LoginForm, RegistrationForm;


@app.route("/")
@app.route('/home')
def home():
    return render_template("home.html", title="home");

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm();
    if(form.validate_on_submit()):
        if(form.email.data == 'test@gmail.com' and form.password.data == 'password'):
            flash(f"You have been logged in!","info");
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger');
            return redirect(url_for('login'))
        return redirect(url_for('home'));
    return render_template("login.html", form=form);

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm();
    if(form.validate_on_submit()): 
        flash(f'Account created for {form.username.data}!','info');
        return redirect(url_for('home'));
    return render_template('register.html', form=form)
