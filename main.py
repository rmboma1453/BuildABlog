from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True   
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/buildablog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))    
    body = db.Column(db.String(120))    

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/add", methods=['POST','GET'])
def add_movie():
    title_name = ''
    body_name=''
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        

    
        #initializing all the error statements
        title_error =''
        body_error =''
        # checking for errors
        if (title_name == '') and (not body_name == ''):
            title_error = 'You did not enter the title'
            title_name = ''
        elif (body_name == '') and (not title_name == ''):
            body_error = 'You did not write a blog'
            body_name = ''
        elif (title_name == '') and (body_name == ''):
            title_error = 'You did not enter the title'
            body_error = 'You did not write a blog'
            title_name = ''
            body_name = ''

        if (not title_error and not body_error):
            new_blog = Blog(title_name, body_name)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('add-confirmation.html',new_blog=new_blog)

        else:
            return render_template('add.html',title_error=title_error,body_error=body_error) 

    #if we have the id query parameter
    reqId = request.args.get('id')
    if not (reqId is None):
        post = Blog.query.filter_by(id=reqId).first()
    
        #use the id to query the database
        return render_template('add-confirmation.html',new_blog=post)

    else:
        return render_template('add.html')
    

    
    
    

     


@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('edit.html',title ="Build A Blog" ,blogs=blogs)

# @app.route('/blog', methods=['GET','POST'])
# def blog():

#     blogs = Blog.query.all()
#     return render_template('edit.html',title ="Build A Blog" ,blogs=blogs)


if __name__ == "__main__":
    app.run()