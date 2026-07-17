from flask import current_app as app
from flask import render_template,request,redirect,url_for
from models import *

@app.route("/")
def home():
    return "Hello, HMS"


@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("emailid") #data from front end form
        pwd=request.form.get("pwd")
        user=db.session.query(User_Credentials).filter(User_Credentials.email==uname,User_Credentials.password==pwd).first()
        if user and user.role==0:
            return render_template("admin_dashboard.html")
        else:
            return redirect(url_for('signup'))
    return render_template("login.html")

    


@app.route("/register", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        uname=request.form.get("emailid") #data from front end form
        pwd=request.form.get("pwd") 
        role=request.form.get("utype")
        user=db.session.query(User_Credentials).filter(User_Credentials.email==uname).first() #check existence/uniqueness
        if user:
            return render_template("signup.html",err_msg="Sorry, email is already used!!")
        else:
            #need to store in user_credentials
            uc=User_Credentials(email=uname,password=pwd,role=int(role))
            db.session.add(uc)
            db.session.commit() #save in the db
    
    #request type is get
    return render_template("signup.html")



#data dictionary
app_dct=[{"dname":"abc","pname":"xyz","spz":"Neurology"},
         {"dname":"pqr","pname":"lmn","spz":"Cardiology"},
         {"dname":"123 ","pname":"jkl","spz":"Ortho"}]


@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html",app_data=app_dct)


