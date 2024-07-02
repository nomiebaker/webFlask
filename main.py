from flask import Flask, render_template, url_for, flash, redirect, request
from form import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_debugtoolbar import DebugToolbarExtension
import git

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = '3acca409c7b773db79025add72e7393a'

app.debug = True
toolbar = DebugToolbarExtension(app)

@app.route("/")                          # this tells you the URL the method below is related to
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
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