from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_url_path='/static')

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_hard_to_guess_string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Crrias123@localhost/online_voting'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Enable SQL debug output

app.config.from_object(Config)
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    id_number = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(80), nullable=False)
    ward_number = db.Column(db.String(80), nullable=False)
    candidate_party = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Vote {self.candidate_name}>'

# Routes
@app.route('/')
def home():
    return render_template('fpage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    id_number = request.form['id_number']
    user = User(username=username, id_number=id_number)
    try:
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('spage'))
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return "There was an issue adding the user to the database."

@app.route('/spage', methods=['GET', 'POST'])
def spage():
    return render_template('spage.html')

@app.route('/vote', methods=['POST'])
def vote():
    candidate_name = request.form['candidate_name']
    ward_number = request.form['ward_number']
    candidate_party = request.form['candidate_party']
    try:
        vote = Vote(candidate_name=candidate_name, ward_number=ward_number, candidate_party=candidate_party)
        db.session.add(vote)
        db.session.commit()
        print(f"Vote added: {vote}")
        return redirect(url_for('fopage'))
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return "There was an issue adding the vote to the database."

@app.route('/fopage')
def fopage():
    return render_template('fopage.html')

@app.route('/tpage')
def tpage():
    return render_template('tpage.html')

@app.route('/admin')
def admin():
    users = User.query.all()
    votes = Vote.query.all()
    return render_template('admin.html', users=users, votes=votes)

if __name__ == '__main__':
    with app.app_context():
        print("Creating all tables...")
        db.create_all()  # Ensure the database tables are created
        print("All tables created.")
    app.run(debug=True)
