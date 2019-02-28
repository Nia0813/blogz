from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#below-connection string used to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLAlCHEMY_ECHO'] = True #turns on query logging
db = SQLAlchemy(app)#connects the constructor to the app
app_secret_key = 'paint'
class Blog(db.Model):# extends the blog class to the database model class

    id = db.Column(db.Integer, primary_key=True)#this will be an integer in this column unique to each blog
    title = db.Column (db.String (150))#title of blog that is created with 150 varchar max
    body = db.Column(db.String(1000))# the body of the blog with 1000 varchar max
    applicant_id = db.Column(db.Integer, db.ForeignKey("user_id"))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner= owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key = TRUE)
    username = db.Column (db.String(120), unique = True)
    password = db.Column (db.String (120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return str(self.username)

@app.before_request

def require_login():
    routes_allowed = ['login','index','singleuser','signup']
    if request.endpoint not in routes_allowed and 'username' not in session:
        return redirect('/login')

@app.toute('/')
def index():
    all_users = User.query.distinct()
    return render_template('index.html', list_all_users = all_users)

#blog displays post
@app.route('/blog', methods = ['GET'])
def blog_list():
    blog_id = request.args.get('id')
    if (blog_id):
        sin_blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('singleblog.html', sin_blog = sin_blog)
    else:
        all_blogs= Blog.query.all()
        return render_template('blog.html', blogs = all_blogs)

def empty_field(self):
    if self:
        return True
    else:
        return False

@app.route('/newpost', methods=['POST','GET'])
def new_blog():
    if request.method == 'POST':
        title_error = ""
        entry_error = ""
        new_title = request.form['blog_title']
        new_body = request.form['body_blog']
        new_blog = Blog(new_title, new_body)
        print (new_title)
        if empty_field(new_title) and empty_field(new_body):
            db.session.add(new_blog)
            db.session.commit()
            blog_link = "/blog?id=" + str(new_blog.id)
            return redirect(blog_link)
        else:
            if not empty_field(new_title) and not empty_field(new_body):
                title_error = "Please enter blog title"
                entry_error = "Please enter blog text"
                return render_template('newpost.html',title_error=title_error, entry_error=entry_error)
            elif not empty_field(new_title):
                title_error = "Please enter blog title"
                return render_template('newpost .html',title_error=title_error,new_body=new_body)
            elif not empty_field(new_body):
                entry_error = "Please enter blog text"
                return render_template('newpost.html', entry_error=entry_error,new_title=new_title)
    else:
        return render_template('newpost.html', title= "Build A Blog")
       

   @app.route('/signup', methods= ['POST', 'GET'])
   def add_user():

       if request.method == 'POST':
           username = request.form['username']
           user_pwd = request.form['password']
           val_user_pwd = request.form['val_password']
        
       if not empty_field(username) or not empty_field(user_pwd) or not empty_field(val_user_pwd):
            flash ('All fields must be filled in', 'error')
            return render_template('signup.html')

        if len (user_pwd)< 3 and len (username)< 3:
            flash ('Passwords must match', 'error')
            return render_template('signup.html')  
        
        if len (username) < 3:
            flash('Username must be a minium of 3 characters', 'error')
            return render_template('signup.html')

        previous_user= User.query.filter_by(username=username).first()
        if not previous_user:
            new_user = User (username, user_pwd)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('New account created', 'success')
            return redirect('/newpost')
        else:
            flash('Oops, this username already exists', 'error')
            return render_template('signup.html')

else:
    return render_template('signup.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form ['password']


        if not username and not pwd:
            flash('Please enter username and password', 'error')
            return render_template('login.html')
        if not username:
            flash('Please enter username', 'error')
            return render_template('login.html')
        if not pwd:
            flash('Please enter password', 'error')
            return render_template('login.html')
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Sorry, username does not exist', 'error')
            return render_template('login.html')
        if user.password != password:
            flash ('Incorrect password', 'error')
            return render_template('login.html')
        if user and user.password == password:
            session['username'] = username
            return redirect('newpost')
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    flash('You are logged out', 'success')
    return redirect('/blog')
   

     
    
        



if __name__=='__main__':#allow us to use the functions in other projects without starting up the app
    app.run()