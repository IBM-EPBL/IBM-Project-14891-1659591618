from flask import *
import ibm_db
app=Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate:DigiCertGlobalRootCA;PROTOCOL=TCPIP;UID=GYH78840;PWD=SvvauA91JzjtLOTJ;", "", "")
# conn=None
@app.route("/", methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("index.html",status="",colour="red")
    elif request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        query = '''select * from users where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is not False):
            if(row['PASSWORD'] != password):
                return render_template("index.html",status="Invalid Password",colour="red")
            else:
                return "Dashboard"

        return render_template("index.html",status="Invalid Email",colour="red")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template("signup.html",status="",colour="red")
    elif request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        name=request.form["name"]
        phone_number=request.form["phone_number"]
        query = '''select * from users where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into users(email, password, name,phone_number) values('{}', '{}', '{}', '{}')'''.format(email, password, name,phone_number)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("signup.html",status="Signup Success",colour="green")
        else:
            return render_template("signup.html",status="User Already Exists",colour="red")

if __name__=="__main__":
    app.run()


