from flask import Flask, render_template


# Create a Falsk Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')

#def index():
#    return "<h1>Hello world!<h1>"

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


