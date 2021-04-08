from flask import Flask, render_template, url_for, flash, redirect, request;
from app import app, db, bcrypt;
from app.forms import LoginForm, RegistrationForm, FileUpload;
from app.models import User, TriviaGame;
from flask_login import login_user, current_user, logout_user, login_required;
import json;
import datetime;

@app.route('/home')
@app.route("/")
def home():
    now = datetime.date.today();
    logged_in = current_user.is_authenticated;
    raw = TriviaGame.query.all();
    content = [];
    date = [];
    users = [];
    for i in range(len(raw)-1, -1, -1):
        users.append(raw[i].author.username);
        content.append(json.loads(raw[i].content));
        date.append(raw[i].date);
    # print(content);
    # print(date);
    return render_template("home.html", title="home",users=users, is_logged_in=logged_in, content=content, length=len(content), date=date, now=now);

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
        return redirect(url_for('home'));
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

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = FileUpload();
    fine = True;
    if(request.method == "POST"):
        file = request.form['file'];
        print(file)
        trivia = request.form;
        keylist = [];
        questions = [];
        answers = [];
        if(file):
            # some lines of code
            return redirect(url_for('home'));
        for d in trivia:
            keylist.append(d);
        for key in keylist:
            if(key.__contains__('question')):
                # print(key);
                questions.append(key);
            elif(key.__contains__('answer')):
                answers.append(key);
            if(trivia[key] == '' and key != 'file'):
                flash(key+" has not been filled.","warning");
                fine = False;
                break;
        if(fine):
            triviagame = TriviaGame(content=json.dumps(trivia), author=current_user);
            db.session.add(triviagame);
            db.session.commit();
            return redirect(url_for("home"));
    number = int(len(request.form)/2)-1;
    # print(number);
    if(number == -1):
        number = 1;
    return render_template('create.html',is_logged_in=current_user.is_authenticated, number=number, form=form);

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    if(request.method == "POST"):
        print(request.form['fileToUpload']);    
    return render_template('upload.html',is_logged_in=current_user.is_authenticated);

@app.route('/upload.php')
@login_required
def uploadphp():    
    return render_template('upload.php',is_logged_in=current_user.is_authenticated);