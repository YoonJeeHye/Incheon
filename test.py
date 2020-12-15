from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/')
#@app.route('/index/<int:GYM_gNum>/')
@app.route('/index')
def GYMMenu():
    db = sqlite3.connect("GYM_table.db")
    #cur = db.cursor()
    db.row_factory = sqlite3.Row
    #items = cur.execute('SELECT gCategory, gName, gAddress, gNumber FROM GYM'
    #).fetchall()
    
    items = db.execute(
        'SELECT gCategory, gName, gAddress, gNumber FROM GYM'
        #'WHERE GYM_gNum=?', (GYM_gNum,)
    ).fetchall()

    output = ''
    for item in items:
        output += item['gCategory'] + '<br>'
        output += item['gName'] + '<br>'
        output += item['gAddress'] + '<br>'
        output += item['gNumber'] + '<br>'
    return output

    #output = ''
    #for item in items:
    #    output += item[0] + '<br>'
    #    output += item[1] + '<br>'
    #    output += item[2] + '<br>'
    #    output += item[3] + '<br>'
    #return item
     #   print(item[0])
    
    ## return output
  # print(output)
    #db.close()
    #return render_template('index.html', items=items)

if __name__ == '__main__':
    app.debug = True
#hello()
    app.run(host='')

   