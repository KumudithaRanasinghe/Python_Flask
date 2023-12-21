from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Create a Falsk Instance
app = Flask(__name__)

#Add Database
#Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#New MySQL DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/our_users'


#Secret Key
app.config['SECRET_KEY'] = "hello world!"
#Initialize The Databas
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("submit")

#Create login page
@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #chech hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("login successfully")
                return redirect(url_for('dashbord'))
            else:
                flash("Try again")
        else:
             flash("Try again")

    return render_template('login.html', form=form)

#logoput page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("YOu have logged out")
    return redirect(url_for('login'))
    


#create dashboard page
@app.route('/dashbord',methods=['GET', 'POST'])
@login_required
def dashbord():
    return render_template('dashbord.html')


#Json
@app.route('/date')
def get_current_date():
    return {"date ": datetime.today()}


#Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favourite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Do some password stuff
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(20))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Create A String
    def __repr__(self):
        return '<name %r>' % self.name
    
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted Successfully!")
        our_user = Users.query.order_by(Users.date_added).all()
        return render_template("add_user.html", 
                                form=form,
                                name=name,
                                our_users=our_user)

    except:
        flash("There is a problem, Try again!!")
        return render_template("add_user.html", 
                                form=form,
                                name=name,
                                our_users=our_user)
    
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("UserName", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("submit")

#Update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                    form=form,
                                    name_to_update=name_to_update)
        except:
            flash("Error Try Again..!")
            return render_template("update.html",
                                    form=form,
                                    name_to_update=name_to_update)
        
    else:
        return render_template("update.html",
                                    form=form,
                                    name_to_update=name_to_update,
                                    id=id)

class PasswordForm(FlaskForm):
    email = StringField("What is Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What is Your Password", validators=[DataRequired()])
    submit = SubmitField("submit")

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("submit")


# Create a route decorator
@app.route('/')

def index():
    first_name = "Ravindu"
    stuff = "this is <strong>Bold</strong> Text"
    favourite_pizza = ["BBQ", "Devil Chicken", "Seafood", 69]
    return render_template("index.html", 
                           first_name=first_name, 
                           stuff=stuff, 
                           favourite_pizza=favourite_pizza)

@app.route('/user/<name>')

# localhost:5000/user/Ravindu
def user(name):
    return render_template("user.html", user_name=name)

@app.route('/user/add_user', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash the password
            hashed_pw = generate_password_hash(form.password_hash.data,)
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favourite_color=form.favourite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favourite_color.data = ''
        form.password_hash = ''
        
        flash("User Added Successfully!")
    our_user = Users.query.order_by(Users.date_added).all()
    return render_template("add_user.html", 
                           form=form,
                           name=name,
                           our_users=our_user)


#Create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

#create Password test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''

        #Lookup User by email address
        
        pw_to_check =Users.query.filter_by(email=email).first()
        #chech Hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)


    return render_template("test_pw.html", 
                           email = email,
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed,
                           form = form)

#create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html", 
                           name = name,
                           form = form)

@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all()
        flash("Database tables created successfully!")
    return "Database tables created"






