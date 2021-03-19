from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "EcoMe"

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM building")
    building = cur.fetchall()
    cur.execute("SELECT * FROM class")
    year = cur.fetchall()
    cur.execute("SELECT * FROM major")
    major = cur.fetchall()
    cur.callproc('total_score')
    scores = cur.fetchall()
    cur.execute("SELECT avgScore()")
    avgScore = cur.fetchall()
    cur.close()
    return render_template("index.html", buildings = building, year = year, major= major, scores = scores, avgScore = avgScore)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("You have successfully taken the survey. View your score below.")
        fname = request.form['fname']
        lname = request.form['lname'] 
        age = request.form['age']
        year = request.form['year']
        email = request.form['email']
        gender = request.form['gender']
        building = request.form['building']
        major = request.form['major']
        recycle = request.form['recycle']
        trash = request.form['trash']
        disposables = request.form['disposables']
        shower = request.form['shower']
        dishes = request.form['dishes']
        plantb = request.form['plantb']
        finishf = request.form['finishf']
        meat = request.form['meat']
        pmode = request.form['pmode']
        lengthc = request.form['lengthc']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO waste (recycle, tbags, disposable) VALUES (%s, %s, %s)", (recycle, trash, disposables))
        mysql.connection.commit()
        cur.execute("SELECT wasteid FROM waste WHERE recycle=%s && tbags=%s && disposable=%s", [recycle, trash, disposables])
        w = cur.fetchall()
        w1 = w[0][0]

        cur.execute("INSERT INTO water (shower, dishes) VALUES (%s, %s)", (shower, dishes))
        mysql.connection.commit()
        cur.execute("SELECT waterid FROM water WHERE shower=%s && dishes=%s", [shower, dishes])
        wat = cur.fetchall()
        wat1 = wat[0][0]

        cur.execute("INSERT INTO food (plant, finishfood, meat) VALUES (%s, %s, %s)", (plantb, finishf, meat))
        mysql.connection.commit()
        cur.execute("SELECT foodid FROM food WHERE plant=%s && finishfood=%s && meat=%s", [plantb, finishf, meat])
        f = cur.fetchall()
        f1 = f[0][0]

        cur.execute("INSERT INTO transport (pmode, length) VALUES (%s, %s)", (pmode, lengthc))
        mysql.connection.commit()
        cur.execute("SELECT transportid FROM transport WHERE pmode=%s && length=%s", [pmode, lengthc])
        t = cur.fetchall()
        t1 = t[0][0]

        cur.execute("INSERT INTO users (first_name, last_name, age, grade, email, gender, building, water, food, transport, waste, major) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, age, year, email, gender, building, (int(wat1)), (int(f1)), (int(t1)), (int(w1)), major))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/update', methods = ["POST", "GET"])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname'] 
        age = request.form['age']
        year = request.form['year']
        email = request.form['email']
        gender = request.form['gender']
        building = request.form['building']
        major = request.form['major']
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE users
        SET first_name=%s, last_name=%s, age=%s, grade=%s, email=%s, gender=%s, building=%s, major=%s
        WHERE pid=%s
        """, (fname, lname, age, year, email, gender, building, major, id_data))
        flash("User info successfully updated")
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ["POST", "GET"])
def delete(id_data):
    flash("User deleted successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE pid = %s", [id_data])
    mysql.connection.commit()
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(debug=True)