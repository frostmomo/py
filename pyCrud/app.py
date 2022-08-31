from flask import Flask, render_template, request, redirect, session, url_for
import pymysql

app = Flask(__name__)

def connection():
    s='localhost'
    d='pyexample'
    u='root'
    p=''
    conn = pymysql.connect(host=s,user=u,password=p,database=d)
    return conn

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        session['username']=request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    login=False
    if 'username' in session:
        login=True
    return render_template('login_home.html',login=login)

@app.route("/")
def main():
    datas = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    for row in cursor.fetchall():
        datas.append({"nip": row[0],"nama": row[1],"jabatan": row[2],"noHp": row[3],})
    conn.close()
    return render_template("empList.html", datas = datas)

@app.route("/add", methods = ['GET','POST'])
def addEmployee():
    if request.method == 'GET':
        return render_template("empAdd.html")
    if request.method == 'POST':
        nip = int(request.form["nip"])
        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        noHp = int(request.form["noHp"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (nip, nama, jabatan, noHp) VALUES (%s, %s, %s, %s)",(nip, nama, jabatan, noHp))

        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/update/<int:nip>',methods = ['GET','POST'])
def update(nip):
    datas = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM data WHERE nip = %s", (nip))
        for row in cursor.fetchall():
            datas.append({"nip": row[0],"nama": row[1],"jabatan": row[2],"noHp": row[3],})
        conn.close()
        return render_template("empAdd.html", datas = [0])
    if request.method == 'POST':
        nama = str(request.form["nama"])
        jabatan = str(request.form["jabatan"])
        noHp = int(request.form["noHp"])
        cursor.execute("UPDATE data SET nama = %s, jabatan = %s, noHp = %s WHERE nip = %s", (nama, jabatan, noHp, nip))
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/delete/<int:nip>')
def delete(nip):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data WHERE nip = %s", (nip))
    conn.commit()
    conn.close()
    return redirect('/')

# @app.route("/api")
# def main():
#     datas = []
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM data")
#     for row in cursor.fetchall():
#         datas.append({"nip": row[0],"nama": row[1],"jabatan": row[2],"noHp": row[3],})
#     conn.close()
#     return render_template("empList.html", datas = datas)

# @app.route("/api/add", methods = ['GET','POST'])
# def addEmployee():
#     if request.method == 'GET':
#         return render_template("empAdd.html")
#     if request.method == 'POST':
#         nip = int(request.form["nip"])
#         nama = request.form["nama"]
#         jabatan = request.form["jabatan"]
#         noHp = int(request.form["noHp"])
#         conn = connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO data (nip, nama, jabatan, noHp) VALUES (%s, %s, %s, %s)",(nip, nama, jabatan, noHp))

#         conn.commit()
#         conn.close()
#         return redirect('/')

# @app.route('/api/update/<int:nip>',methods = ['GET','POST'])
# def update(nip):
#     datas = []
#     conn = connection()
#     cursor = conn.cursor()
#     if request.method == 'GET':
#         cursor.execute("SELECT * FROM data WHERE nip = %s", (nip))
#         for row in cursor.fetchall():
#             datas.append({"nip": row[0],"nama": row[1],"jabatan": row[2],"noHp": row[3],})
#         conn.close()
#         return render_template("empAdd.html", datas = [0])
#     if request.method == 'POST':
#         nama = str(request.form["nama"])
#         jabatan = str(request.form["jabatan"])
#         noHp = int(request.form["noHp"])
#         cursor.execute("UPDATE data SET nama = %s, jabatan = %s, noHp = %s WHERE nip = %s", (nama, jabatan, noHp, nip))
#         conn.commit()
#         conn.close()
#         return redirect('/')

# @app.route('/api/delete/<int:nip>')
# def delete(nip):
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM data WHERE nip = %s", (nip))
#     conn.commit()
#     conn.close()
#     return redirect('/')

if(__name__ == "__main__"):
    app.run()