from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin #Protecting routes

db=SQLAlchemy()

class User_Credentials(db.Model,UserMixin): #Inherit credentials with UserMixin
    __tablename__='user_credentials'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,nullable=False) #allowed only a:0/d:1/p:2 

    patients=db.relationship("Pt_Profile",cascade="all,delete",backref='user_credentials') #Relation column linking parent to child. Ex: linking to patient profile
    doctors=db.relationship("Dr_Profile",cascade="all,delete",backref='user_credentials') #Relation column linking parent to child. Ex: linking to doctor profile
    availability=db.relationship("Dr_Availability",cascade="all,delete",backref='user_credentials') 
    appointments=db.relationship("Appointments",cascade="all,delete",backref='user_credentials') 



class Pt_Profile(db.Model):
    __tablename__='pt_profile'
    id=db.Column(db.Integer,primary_key=True)
    pt_id=db.Column(db.Integer,db.ForeignKey('user_credentials.id'),nullable=False) #linking child to parent
    full_name=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    phno=db.Column(db.String,nullable=False)
    status=db.Column(db.Integer,nullable=False,default=0) #0-register, 1-deactivated


class Dr_Profile(db.Model):
    __tablename__='dr_profile'
    id=db.Column(db.Integer,primary_key=True)
    dr_id=db.Column(db.Integer,db.ForeignKey('user_credentials.id'),nullable=False) #linking child to parent
    full_name=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    spl=db.Column(db.String,nullable=False)
    exp=db.Column(db.Float,nullable=False)
    phno=db.Column(db.String,nullable=False)
    status=db.Column(db.Integer,nullable=False,default=0) #0-register, 1-approved, 2-deactivated


class Dr_Availability(db.Model):
    __tablename__='dr_availability'
    id=db.Column(db.Integer,primary_key=True)
    dr_id=db.Column(db.Integer,db.ForeignKey('user_credentials.id'),nullable=False) #linking child to parent
    avail_date=db.Column(db.Date,nullable=True)
    session=db.Column(db.String,nullable=True)
    max_patients=db.Column(db.Integer,default=10)
    booked=db.Column(db.Integer,default=0) #Total count of bookings
    status=db.Column(db.String,default='a') #a-available,f-full

    appointments=db.relationship("Appointments",cascade="all,delete",backref='dr_availability') 


class Appointments(db.Model):
    __tablename__='appointments'
    id=db.Column(db.Integer,primary_key=True)
    avail_id=db.Column(db.Integer,db.ForeignKey('dr_availability.id'),nullable=False) #linking child to parent
    pt_id=db.Column(db.Integer,db.ForeignKey('user_credentials.id'),nullable=False) #linking child to parent
    token_no=db.Column(db.Integer,nullable=False)
    booking_time=db.Column(db.String,nullable=False)
    status=db.Column(db.String,default='b') #b-booked,d-completed,c-cancelled

    consultations=db.relationship("Consultation_Details",cascade="all,delete",backref='appointments') 


class Consultation_Details(db.Model):
    __tablename__='consultation_details'
    id=db.Column(db.Integer,primary_key=True)
    apt_id=db.Column(db.Integer,db.ForeignKey('appointments.id'),nullable=False) #linking child to parent
    consult_dt_time=db.Column(db.String,nullable=False)
    diagnosis_rem=db.Column(db.String,nullable=False)
    prescription_rem=db.Column(db.String,nullable=False)
    other_rem=db.Column(db.String,nullable=True)


    


    







    
