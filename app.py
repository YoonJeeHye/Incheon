"""Flask Login Example and instagram fallowing find"""


from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from instagram import getfollowedby, getname
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    userid = db.Column(db.String(80), unique=True)
    userpassword = db.Column(db.String(80))
    userphone = db.Column(db.String(80))

    def __init__(self, username, userid, userpassword, userphone):
        self.username = username
        self.userid = userid
        self.userpassword = userpassword
        self.userphone = userphone

@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html', data=getfollowedby(username))
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['userid']
        passw = request.form['userpassword']
        try:
            data = User.query.filter_by(userid=name, userpassword=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template('register2.html')
        except:
            return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], userid=request.form['userid'], userpassword=request.form['userpassword'], userphone=request.form['userphone'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route('/register2/', methods=['GET', 'POST'])
def register2():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], userid=request.form['userid'], userpassword=request.form['userpassword'], userphone=request.form['userphone'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route('/')
@app.route('/index')
def hello():
    db = sqlite3.connect("GYM_table.db")
    cur = db.cursor()
    ## db.row_factory = sqlite3.Row
    items = cur.execute('SELECT gCategory, gName, gAddress, gNumber FROM GYM'
    ).fetchall()
    
 ##   items = db.excute(
 ##       'SELECT gCategory, gName, gAddress, gNumber FROM GYM'
 ##   ).fetchall()

    output = ''
    for item in items:
        output += item[0] + '<br>'
        output += item[1] + '<br>'
        output += item[2] + '<br>'
        output += item[3] + '<br>'
     ##   return item
     ##   print(item[0])
    
    ## return output
    print(output)
    return(output)

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    hello()
    app.run(host='')

    
