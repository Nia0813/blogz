from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#below-connection string used to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLAlCHEMY_ECHO'] = True #turns on query logging
db = SQLAlchemy(app)#connects the constructor to the app
app.secret_key = 'za997kGcys&zP3A'

class Blog(db.Model):# extends the blog class to the database model class

    id = db.Column(db.Integer, primary_key = True)#this will be an integer in this column unique to each blog
    title = db.Column (db.String (120))#title of blog that is created with 120 varchar max
    body = db.Column(db.Text())# the body of the blog with 1000 varchar max
    applicant_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, applicant):
        self.title = title
        self.body = body
        self.applicant = applicant

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column (db.String(120), unique = True)
    password = db.Column (db.String (120))
    blogs = db.relationship('Blog', backref='applicant')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    routes_allowed = ['login','index','signup','blog_list']
    if request.endpoint not in routes_allowed and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['POST','GET'])
def index():
    all_users = User.query.all()
    return render_template('index.html', all_users = all_users)

#blog displays post
@app.route('/blog', methods = ['GET'])
def blog_list():
    title = "Blogs"
    if session:
        applicant=User.query.filter_by(username=session['username']).first()
    
    if 'id' in request.args:
        post_id = request.args.get('id')
        blog = Blog.query.filter_by(id = post_id).all()
        return render_template('blogs.html', title = title, blog = blog, post_id = post_id)

    if 'user' in request.args:
        user_id = request.args.get('user')
        blog = Blog.query.filter_by (applicant_id = user_id).all()
        return render_template('blogs.html', title = title, blog = blog)

    else:
        blog = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blogs.html', title = title, blog = blog)

@app.route('/login', methods = ['POST', 'GET'])
def login():

    username = ""
    error_username = ""
    error_pwd= ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form ['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            error_username = 'Sorry, username does not exist'
            if username == "":
                error_username = 'Please enter username'

        if password == "":
            error_pwd = 'Enter your password'

        if user and user.password != password:
            error_pwd = "Incorrect password"
        
        if user and user.password != password:
            session['username'] = username
            return redirect ('/newpost')
        
    return render_template('login.html', username = username, 
           error_username = error_username, error_pwd= error_pwd)

        
@app.route('/signup', methods= ['POST', 'GET'])
def signup():
    
    verify= ""
    password = ""
    username = ""
    error_username = ""
    error_pwd = ""
    error_verify = ""
    

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        verify = request.form ['verify']
        
        existing_user = User.query.filter_by(username= username).first()

    if len (username) < 3:
        error_username= 'Username must be a minimum of 3 characters'
        if username == "":
            error_username = "Please Enter A Username "

        if password != verify:
            error_pwd = "Passwords must match"
            error_verify = "Passwords must match"

        if len (password) < 3:
            error_pwd = "Passwords must be a minimum of 3 characters"
            if password == "":
                error_pwd = "Please Enter A Password"
            
        if not error_username and not error_pwd and not error_verify:
            if not existing_user:
                new_user = User(username, password,verify)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                error_username = "Username already in use"
    
    return render_template('signup.html', username=username, error_username= error_username, error_pwd = error_pwd, error_verify= error_verify)



@app.route('/newpost', methods=['POST','GET'])
def new_blogs():
        blog_title = ""
        blog_body = ""
        error_title= ""
        error_body = ""
        applicant = User.query.filter_by(username = session['username']).first()

        if request.method == 'POST':
            blog_title = request.form['blog_title']
            blog_body = request.form['blog_body']

        if blog_title == "":
            error_title = "Please enter a title"

        if blog_body == "":
            error_body= "Please write a post"

        if error_title =="" and error_body == "":
            new_blog = Blog(blog_title, blog_body, applicant)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = Blog.query.order_by(Blog.id.desc()).first()
            user = applicant
            
            return redirect('/blog?id={}&user={}'.format(blog_id.id, user.username))

             
        return render_template('newpost.html', title = " Blogz", blog_title = blog_title, blog_body = blog_body, error_title = error_title, error_body = error_body)
     
        

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
   
if __name__=='__main__':#allow us to use the functions in other projects without starting up the app
    app.run()