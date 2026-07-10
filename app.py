from flask import Flask,render_template


hms_app=Flask(__name__)

@hms_app.route("/")
def home():
    return "Hello, HMS"


@hms_app.route("/login/")
def signin():
    return render_template("login.html")



#data dictionary
app_dct=[{"dname":"abc","pname":"xyz","spz":"Neurology"},
         {"dname":"pqr","pname":"lmn","spz":"Cardiology"},
         {"dname":"123 ","pname":"jkl","spz":"Ortho"}]


@hms_app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html",app_data=app_dct)

#executable of flask
if __name__=="__main__":
    hms_app.run(debug=True)
