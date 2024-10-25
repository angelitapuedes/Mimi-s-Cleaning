from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#Add Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Secret Key
app.config['SECRET_KEY'] = "Secret Key"

#Initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Customers.query.get_or_404(id)
    name = None
    form = CustomerForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        our_customers = Customers.query.order_by(Customers.date_added)
        return render_template("add_customer.html", 
            form=form, 
            name=name,
            our_customers=our_customers)
    except:
        flash("Whoops there was a problem deleting")
        return render_template("add_customer.html", 
            form=form, 
            name=name,
            our_customers=our_customers)

#Create a Model
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    clean_package = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #password stuff
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

#update record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = CustomerForm()
    name_to_update = Customers.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()

            flash("Customer Updated Successfully!")
            return render_template("update.html", 
                form=form, 
                name_to_update = name_to_update)
        except:
            flash("Looks like there was a problem...try again")
            return render_template("update.html", 
                form=form, 
                name_to_update = name_to_update)
    else:
        return render_template("update.html", 
            form=form, 
            name_to_update = name_to_update,
            id = id)
    
#review
@app.route('/review/<int:id>', methods=['GET', 'POST'])
def review(id):
    form = CustomerForm()
    review_to_update = Customers.query.get_or_404(id)
    if request.method == "POST":
        review_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()

            flash("Customer Review Successfully!")
            return render_template("add_review.html", 
                form=form, 
                review_to_update = review_to_update)
        except:
            flash("Looks like there was a problem...try again")
            return render_template("add_review.html", 
                form=form, 
                review_to_update = review_to_update)
    else:
        return render_template("add_review.html", 
            form=form, 
            review_to_update = review_to_update,
            id = id)
    
class CustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class NamerForm(FlaskForm):
    name = StringField("Whats your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("Whats your email", validators=[DataRequired()])
    password_hash = PasswordField("What's your Password hash", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/customer/add', methods =['GET', 'POST'])
def add_customer():
    name = None
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer is None:
            # Hah the password
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            customer = Customers(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(customer)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        
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
#Password Test Page
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
        #Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        pw_to_check = Customers.query.filter_by(email=email).first()
        
    return render_template("test_pw.html", 
            email = email, 
            password = password,
            pw_to_check = pw_to_check,
            form = form)