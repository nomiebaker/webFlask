from flask import Flask, render_template, url_for, flash, redirect, request
from form import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
# from flask_debugtoolbar import DebugToolbarExtension
import git
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '3acca409c7b773db79025add72e7393a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()


# app.debug = True
# toolbar = DebugToolbarExtension(app)

@app.route("/")                          # this tells you the URL the method below is related to
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/nomiekb/webFlask')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")