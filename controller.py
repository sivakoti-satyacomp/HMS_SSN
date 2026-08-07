from flask import current_app as app
from flask import render_template,request,redirect,url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import *
from datetime import datetime,timedelta

@app.route("/")
def home():
    return "Hello, HMS"

'''
Authorization and authentication
'''
@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("emailid") #data from front end form
        pwd=request.form.get("pwd")
        user=db.session.query(User_Credentials).filter(User_Credentials.email==uname,User_Credentials.password==pwd).first()
        if user and user.role==0:
            login_user(user) #store into session
            return redirect(url_for("admin_dashboard"))
        elif user and user.role==1:
            login_user(user) 
            return render_template("dr_dashboard.html",id=user.id) #avoid this
        elif user and user.role==2:
            login_user(user)
            return redirect(url_for("pt_dashboard",id=user.id)) #Recommend this url_for
        else:
            return redirect(url_for('signup'))
    return render_template("login.html")

    

'''
Authorization and authentication
'''
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
            return redirect(url_for("signin"))
    else:
        #request type is get
        return render_template("signup.html")

@app.route('/logout')
def logout():
    logout_user() #delete from session
    return redirect(url_for('signin'))



'''
    #### Routes defined for admin dashboard ####
'''
@app.route("/admin")
@login_required
def admin_dashboard():
    dt_data=get_all_drs()
    pt_data=get_all_pts()
    return render_template("admin_dashboard.html",dr_data=dt_data, pt_data=pt_data)

#Editing doctor
@app.route("/ed_dr")
@login_required
def edit_dr():
    #render with specific dr data??
    dr_id=request.args.get("dr_id") #got query param
    dr_searched=search_dr(dr_id)
    return render_template("edit_doctor.html",dr_data=dr_searched)

#Approve doctor
@app.route("/approve_dr")
@login_required
def approve_dr():
    #render with specific dr data??
    dr_id=request.args.get("dr_id") #got query param
    dr_searched=search_dr(dr_id)
    dr_searched.status=1
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

#Update doctor
@app.route("/update_dr",methods=["GET","POST"])
@login_required
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


#Editing patient
@app.route("/ed_pt")
@login_required
def edit_patient():
    dr_id=request.args.get("dr_id") #got query param
    dr_searched=search_dr(dr_id)
    return render_template("edit_doctor.html",dr_data=dr_searched)


#Update patient
@app.route("/update_pt",methods=["GET","POST"])
def update_patient():
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
    return redirect(url_for("dr_dashboard"))





'''
### Routes for Dr dashboard ###
'''
@app.route("/dr/<id>")
@login_required
def dr_dashboard(id):
    return render_template("dr_dashboard.html",id=id)

@app.route("/pt_history/update")
def patient_history_update():
    return render_template("update_pt_history.html")


@app.route("/dr_availability/<id>")
def dr_avail(id):
    next_seven=generate_next_appts()
    return render_template("update_dr_avail.html",dr_av=next_seven,id=id)
    
@app.route("/update_availability",methods=["GET","POST"])
def save_avail():
    if request.method=="POST":
        dr_id=int(request.form.get("id"))
        dt=request.form.get("dt")
        fn=request.form.getlist("fn[]")
        an=request.form.getlist("an[]")
        #maxp=request.form.get("nop")
        # print("Max patient: ",maxp,dr_id)
        # print("date: ",dt,"FN: ",fn,"an: ",an) #['2026-08-01:9am-12Noon', '2026-08-03:9am-12Noon']
        #print("dr_id : ",dr_id)
        for d in fn:
            day,time=d.split(":")
            day=datetime.strptime(day,'%Y-%m-%d').date()
            dr_avail=Dr_Availability(dr_id=dr_id,avail_date=day,session=time)
            db.session.add(dr_avail)
            db.session.commit()

        for d in an:
            day,time=d.split(":")
            day=datetime.strptime(day,'%Y-%m-%d').date()
            dr_avail=Dr_Availability(dr_id=dr_id,avail_date=day,session=time)
            db.session.add(dr_avail)
            db.session.commit()
    return redirect(url_for("dr_dashboard",id=dr_id))

@app.route("/dr_details/<id>")
@login_required
def dr_details(id):
    dr_det=db.session.query(Dr_Profile.full_name,Dr_Profile.spl,Dr_Profile.exp,Dr_Profile.dr_id).filter(Dr_Profile.id==id).first()
    return render_template("dr_details.html",dr_details=dr_det)

    

'''
### Routes for Patient dashboard ###
'''
@app.route("/pt/<id>")
@login_required
def pt_dashboard(id):
    #print("Patient dashboard")
    depts=get_departments() #get departments
    return render_template("patient_dashboard.html",id=id,depts=depts)

@app.route("/pt_history/<id>")
def patient_history(id):
    #Get patient, appointments and consultant data
    patient,appts,cons_dtls=get_patient_history(id)
    return render_template("patient_history.html",pt_data=pt_data)

@app.route("/drs_by_spl/<spl>")
def dr_list_by_spl(spl):
    drs = db.session.query(Dr_Profile.id,Dr_Profile.full_name,Dr_Profile.spl,Dr_Profile.dr_id).filter(Dr_Profile.spl == spl).all()
    return render_template("dept_details.html",drs=drs,spl=spl)

@app.route("/book_appointment/<id>")
def book_appointment(id):
    print("ID: ",id)
    return render_template("book_appointment.html",id=id)

'''
    ### Additional python functions ###
'''
def get_all_drs():
    dr_data=db.session.query(Dr_Profile).filter().all()
    return dr_data


def get_all_pts():
    pt_data=db.session.query(Pt_Profile).filter().all()
    return pt_data

def search_dr(id):
    dr_searched=db.session.query(Dr_Profile).filter(Dr_Profile.dr_id==id).first()
    return dr_searched
    

def generate_next_appts():
    today=datetime.now().date()
    #generate next 7days
    days_7=[today+timedelta(days=i) for i in range(1,8)]
    return days_7


def get_patient_history(id):
    pt_user=db.session.query(User_Credentials).filter(User_Credentials.id==id).first() #get user
    appts=pt_user.appointments #get appointment of the user ie., patient
    cons_dtls=appts.consultations #all past consulations of the patient

    return (pt_user,appts,cons_dtls) #data objects

def get_departments():
    depts = db.session.scalars(db.session.query(Dr_Profile.spl).filter(Dr_Profile.status == 1).distinct()).all()
    return depts

