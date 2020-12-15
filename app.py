"""Flask Login Example and instagram fallowing find"""


from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from instagram import getfollowedby, getname
import sqlite3

app = Flask(__name__)

@app.route('/')
def GYMMenu():
    db = sqlite3.connect("GYM_table.db")
    db.row_factory = sqlite3.Row
    
    items = db.execute(
        'SELECT gCategory, gName, gAddress, gNumber FROM GYM'
    ).fetchall()

    db.close()
    return render_template('index.html', items=items)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GYM_table.db'
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


@app.route('/okay/',methods=['GET','POST'])
def okay():
    """Okay Form"""
    try:
        username=request.form.get("username","")
        userphone=request.form.get("userphone","")
        gNum=request.form.get("gNum","")
        startTime=request.form.get("startTime","")
        endTime=request.form.get("endTime","")

        conn=sqlite3.connect('GYM_table.db')
        sql="INSERT INTO Reservation (username, userphone, gNum, startTime, endTime) VALUES (?,?,?,?,?)"
        cur.execute(sql, (username,userphone,gNum,startTime,endTime))
        conn.commit()

        print("successfully added")
    except Exception as e:
        conn.rollback()
        print('db error:', e)
        print("Error in insert operation")
    finally : 
        conn.close()
        return redirect(url_for('okay'))

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/index', methods=['GET', 'POST'])
def search():
    search=request.form.get("search", "")
    conn=sqlite3.connect('GYM_table.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql="SELECT * FROM GYM WHERE gCategory LIKE ?"
    cur.execute(sql, ('%'+search+'%',))
    rows = cur.fetchall()
    conn.close()
    return render_template('index.html', data=rows)

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='')

    
