from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html")

services = ["Residential", "Commercial", "Pressure Waashing", "windows", 
            "Organizing", "Decluttering"]

@app.route('/services')

def services():
    return render_template("services.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(505)
def page_not_found(e):
    return render_template("505.html"), 505
