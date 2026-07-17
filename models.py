from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User_Credentials(db.Model):
    __tablename__='user_credentials'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,nullable=False) #allowed only a:0/d:1/p:2 
    patients=db.relationship("Pt_Profile",cascade="all,delete",backref='user_credentials') #Relation column linking parent to child. Ex: linking to patient profile
    doctors=db.relationship("Dr_Profile",cascade="all,delete",backref='user_credentials') #Relation column linking parent to child. Ex: linking to doctor profile


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


    
