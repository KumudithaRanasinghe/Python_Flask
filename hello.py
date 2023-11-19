from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Create a Falsk Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "hello world!"

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your Name", validators=[DataRequired()])
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

#Create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

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





