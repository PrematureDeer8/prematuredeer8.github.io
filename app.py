from flask import Flask, render_template, url_for, flash, redirect;
from forms import RegistrationForm, LoginForm;
from flask_sqlalchemy import SQLAlchemy;

app = Flask(__name__);
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db';
db = SQLAlchemy(app);

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True);
    username = db.Column(db.String(120),  unique=True, nullable=False);
    email = db.Column(db.String(120), unique=True, nullable=False);
    password = db.Column(db.String(120), nullable=False);
    
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')";

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

if __name__ == "__main__":
    app.run(debug=True)