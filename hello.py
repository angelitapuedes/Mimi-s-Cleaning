from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
import datetime
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea

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

#Create a Blog Post model
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cleantype = db.Column(db.String(250))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#Create a Review Form
class ReviewForm(FlaskForm):
    cleantype = StringField("Title for Clean", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/reviews')
def reviews():
    reviews = Reviews.query.order_by(Reviews.date_posted)
    return render_template("reviews.html", reviews=reviews)


@app.route('/review/<int:id>')
def review(id):
    review = Reviews.query.get_or_404(id)
    return render_template('review.html', review=review)

@app.route('/reviews/edit/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
     review = Reviews.query.get_or_404(id)
     form = ReviewForm()
     if form.validate_on_submit():
          review.author = form.author.data
          review.content = form.content.data
          #update to database
          db.session.add(review)
          db.session.commit()
          flash("Review has been updated")
          return redirect(url_for('reviews', id=review.id))
     form.author.data = review.author
     form.content.data = review.content
     return render_template('edit_review.html', form=form)


class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	#content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	#author = StringField("Author")
	slug = StringField("Slug", validators=[DataRequired()])
	submit = SubmitField("Submit")

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
     post = Posts.query.get_or_404(id)
     form = PostForm()
     if form.validate_on_submit():
          post.title = form.title.data
          post.author = form.author.data
          post.slug = form.slug.data
          post.content = form.content.data
          #update to database
          db.session.add(post)
          db.session.commit()
          flash("Post has been updated")
          return redirect(url_for('post', id=post.id))
     form.title.data = post.title
     form.author.data = post.author
     form.slug.data = post.slug
     form.content.data = post.content
     return render_template('edit_post.html', form=form)

     

@app.route('/posts')
def posts():
	# Grab all the posts from the database
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)

# Add Post Page
@app.route('/add_post', methods=['GET', 'POST'])
#@login_required
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		
		post = Posts(title=form.title.data, content=form.content.data, slug=form.slug.data)
		# Clear The Form
		form.title.data = ''
		form.content.data = ''
		#form.author.data = ''
		form.slug.data = ''

		# Add post data to database
		db.session.add(post)
		db.session.commit()

		# Return a Message
		flash("Blog Post Submitted Successfully!")

	# Redirect to the webpage
	return render_template("add_post.html", form=form)

# Add Post Page
@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        post = Reviews(cleantype=form.cleantype.data, content=form.content.data, author=form.author.data)
        #Clear Form
        form.cleantype.data = ''
        form.content.data = ''
        form.author.data = ''
    #Add to datababse
        db.session.add(post)
        db.session.commit()

        flash("Review Submitted!")
        #Redirect
    return render_template("add_review.html", form=form)

@app.route('/rates')
def get_rates():
    rates = {
        "1st time cleans": "$75 per hour",
        "Monthly Client": "$65 per hour",
        "Referrals program": "10 percent off next clean"
    }
    return rates
    #return {"Date": date.today()}

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
# Create a Blog Post model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
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