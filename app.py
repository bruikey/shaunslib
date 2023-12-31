from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from os import environ
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{environ['DB_USERNAME']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}:{environ['DB_PORT']}/{environ['DB_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # The constructor name should be "__init__" instead of "__init"
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Authentication successful
            return redirect(url_for('loggedin'))
        else:
            # Authentication failed
            return {'success': False}
    else:
        return render_template('login.html')
        
    
@app.route('/registered')
def registered():
    return render_template('registered.html')

@app.route('/loggedin')
def loggedin():
        return render_template('loggedin.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        with open('form_data.txt', 'w') as file:
            file.write(f"Username: {username}\n")
            file.write(f"Email: {email}\n")
            file.write(f"Password: {password}\n")
            file.write("\n")
        

        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
     
        return redirect(url_for('registered'))
    return render_template('signup.html')
    
if __name__ == "__main__":
    app.run(debug=True)
