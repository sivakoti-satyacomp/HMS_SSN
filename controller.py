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
        elif user and user.role==1:
            return render_template("dr_dashboard.html")
        elif user and user.role==2:
            return render_template("patient_dashboard.html")
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
            #After user credential, then separate pt & dr
            fname=request.form.get("fname")
            address=request.form.get("address")
            phno=request.form.get("phno")
            if int(role)==2:
                pt_profile=Pt_Profile(pt_id=uc.id,full_name=fname,address=address,phno=phno)
                db.session.add(pt_profile) #if it patient role
            else:
                splz=request.form.get("splz")
                exp=request.form.get("exp")
                dr_profile=Dr_Profile(dr_id=uc.id,full_name=fname,address=address,phno=phno,spl=splz,exp=exp)
                db.session.add(dr_profile) #if it dr role
            db.session.commit() #Save everything
    else:
        #request type is get
        return render_template("signup.html")


@app.route("/admin")
def admin_dashboard():
    dt_data=get_all_drs()
    pt_data=get_all_pts()
    return render_template("admin_dashboard.html",dr_data=dt_data, pt_data=pt_data)

@app.route("/ed_dr")
def edit_dr():
    #render with specific dr data??
    dr_id=request.args.get("dr_id") #got query param
    dr_searched=search_dr(dr_id)
    return render_template("edit_doctor.html",dr_data=dr_searched)

@app.route("/update_dr",methods=["GET","POST"])
def update_dr():
    uid=request.form.get("uid")
    name=request.form.get("d_name")
    splz=request.form.get("splz")
    exp=request.form.get("exp")
    address=request.form.get("address")
    old_dr_details=db.session.query(Dr_Profile).filter(Dr_Profile.dr_id==uid).first()
    #update
    old_dr_details.full_name=name
    old_dr_details.spl=splz
    old_dr_details.exp=exp
    old_dr_details.address=address
    db.session.commit() #saved
    return redirect(url_for("admin_dashboard"))

@app.route("/dr")
def dr_dashboard():
    return render_template("dr_dashboard.html")

@app.route("/pt_history")
def patient_history():
    return render_template("patient_history.html")


@app.route("/pt_history/update")
def patient_history_update():
    return render_template("update_pt_history.html")


#Additional python functions
def get_all_drs():
    dr_data=db.session.query(Dr_Profile).filter().all()
    return dr_data


def get_all_pts():
    pt_data=db.session.query(Pt_Profile).filter().all()
    return pt_data

def search_dr(id):
    dr_searched=db.session.query(Dr_Profile).filter(Dr_Profile.dr_id==id).first()
    return dr_searched
    
