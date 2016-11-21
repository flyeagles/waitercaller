import flask

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for


from flask.ext.login import LoginManager
from flask.ext.login import login_required
#from flask.ext.login import login_user



from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper


DB=DBHelper()
PH=PasswordHelper()


app = Flask(__name__)
app.secret_key = 'WNqjax4aSrj3XEl+vagSbZM6pnhScgywpzn64MqAtuFAkLMZQfJ3/OsnKiGg8Q3od8E8OChBwE4+tuhltyPMqkhxqQ1in8eDlWP'

login_manager = LoginManager(app)


@app.route('/')
def home():
	return render_template("home.html")


@app.route('/account')
@login_required
def account():
	return "You are logged in"


@app.route('/login', methods=["POST"])
def login():
	email= request.form.get("email")
	password=request.form.get("password")
	stored_user=DB.get_user(email)
	if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
		user = User(email)
		flask.ext.login.login_user(user, remember=True)
		return redirect(url_for('account'))

	return redirect(url_for("home"))


@app.route('/logout')
def logout():
	flask.ext.login.logout_user()
	return redirect(url_for("home"))


@app.route('/register', methods=["POST"])
def register():
	email = request.form.get('email')
	pw1 = request.form.get('password1')
	pw2 = request.form.get('password2')
	if not pw1 == pw2:
		return redirect(url_for('home'))
	if DB.get_user(email):
		return redirect(url_for('home'))

	salt = PH.get_salt()
	hashed = PH.get_hash(pw1 + salt)
	DB.add_user(email, salt, hashed)
	return redirect(url_for('home'))



@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

	return None



if __name__ == "__main__":
	app.run(port=5000, debug=True)


