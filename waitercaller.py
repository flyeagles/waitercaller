import datetime
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
import config
from bitlyhelper import BitlyHelper
from forms import RegistrationForm
from forms import LoginForm
from forms import CreateTableForm


DB=DBHelper()
PH=PasswordHelper()
BH=BitlyHelper()


app = Flask(__name__)
app.secret_key = 'WNqjax4aSrj3XEl+vagSbZM6pnhScgywpzn64MqAtuFAkLMZQfJ3/OsnKiGg8Q3od8E8OChBwE4+tuhltyPMqkhxqQ1in8eDlWP'

login_manager = LoginManager(app)


@app.route('/')
def home():
	registrationform=RegistrationForm()
	return render_template("home.html", registrationform=registrationform, loginform=LoginForm() )


@app.route('/account')
@login_required
def account():
	tables=DB.get_tables(flask.ext.login.current_user.get_id())
	return render_template("account.html", tables=tables, createtableform=CreateTableForm() )


@app.route('/account/createtable', methods=["POST"])
@login_required
def account_createtable():
	form=CreateTableForm(request.form)
	if form.validate():
		tableid = DB.add_table(form.tablenumber.data, flask.ext.login.current_user.get_id())
		new_url = BH.shorten_url( config.base_url+'newrequest/' + tableid )
		DB.update_table(tableid, new_url)
		return redirect(url_for("account"))

	return render_template("account.html", createtableform=form, tables=DB.get_tables(flask.ext.login.current_user.get_id() ) )


@app.route('/account/deletetable')
@login_required
def account_deletetable():
	table_id = request.args.get('tableid')
	DB.delete_table(table_id)
	return redirect(url_for("account"))


@app.route('/newrequest/<tid>')
def new_request(tid):
	DB.add_request(tid, datetime.datetime.now())
	return "Your request has been logged."



@app.route('/login', methods=["POST"])
def login():
	form=LoginForm(request.form)
	if form.validate():
		stored_user=DB.get_user(form.loginemail.data)
		if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
			user = User(form.loginemail.data)
			flask.ext.login.login_user(user, remember=True)
			return redirect(url_for('account'))

		form.loginemail.errors.append("Email or password invalid")

	return render_template("home.html", loginform=form, registrationform=RegistrationForm() )


@app.route('/logout')
def logout():
	flask.ext.login.logout_user()
	return redirect(url_for("home"))


@app.route('/register', methods=["POST"])
def register():
	form=RegistrationForm(request.form)
	if form.validate():
		if DB.get_user(form.email.data):
			form.email.errors.append("Email already reged.")
			return render_template('home.html', registrationform=form )

		salt = PH.get_salt()
		hashed = PH.get_hash(form.password.data + salt)
		DB.add_user(form.email.data, salt, hashed)

		return render_template("home.html", registrationform=form, onloadmessage="Registration successful. Please log in.", 
				loginform=LoginForm() )

	return render_template("home.html", registrationform=form, loginform=LoginForm() )


@app.route('/dashboard')
@login_required
def dashboard():
	now = datetime.datetime.now()
	requests = DB.get_requests(flask.ext.login.current_user.get_id())
	for req in requests:
		deltaseconds = (now - req['time']).seconds
		req['wait_minutes'] = "{}.{}".format( (deltaseconds//60), str(deltaseconds%60).zfill(2))
	return render_template("dashboard.html", requests = requests)


@app.route('/dashboard/resolve')
@login_required
def dashboard_resolve():
	request_id = request.args.get('request_id')
	print(request_id)
	DB.delete_request(request_id)
	return redirect(url_for('dashboard'))



@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

	return None



if __name__ == "__main__":
	app.run(port=5000, debug=True)


