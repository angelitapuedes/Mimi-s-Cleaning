from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import datetime 

app = Flask(__name__)
#Add Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Secret Key
app.config['SECRET_KEY'] = "Secret Key"

#Initialize db
db = SQLAlchemy(app)

#Create a Model
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

class CustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

class NamerForm(FlaskForm):
    name = StringField("Whats your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/customer/add', methods =['GET', 'POST'])
def add_customer():
    name = None
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer is None:
            customer = Customers(name=form.name.data, email=form.email.data)
            db.session.add(customer)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        
        flash("User Added successfully!!")
    our_customers = Customers.query.order_by(Customers.date_added)
    return render_template("add_customer.html", 
        form=form, 
        name=name,
        our_customers=our_customers)

@app.route('/')

def index():
    return render_template("index.html")

services = ["Residential", "Commercial", "Pressure Waashing", "windows", 
            "Organizing", "Decluttering"]

@app.route('/services')

def services():
    return render_template("services.html")

@app.route('/packages')

def packages():
    return render_template("packages.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(505)
def page_not_found(e):
    return render_template("505.html"), 505

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")

    return render_template("name.html", 
            name = name, 
            form = form)