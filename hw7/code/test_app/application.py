from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash('cool_admin'),
    "advanced": generate_password_hash("advanced"),
    "beginner": generate_password_hash("beginner"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


@app.route('/profile')
@auth.login_required
def profile():
    return "{}, this is your profile!".format(auth.current_user())


@app.route('/photos')
@auth.login_required
def photos():
    return 'Photos'


@app.route('/photos/<number>')
@auth.login_required
def photo(number):
    return f'Photo number {number}'


@app.route('/shareware')
def shareware():
    return 'Free for all!'


@app.route('/logout')
@auth.login_required
def logout():
    return f"{auth.current_user()} was logout!", 401


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5555)
