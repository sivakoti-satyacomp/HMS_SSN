from flask import Flask
from models import db,User_Credentials 
from config import *
from flask_login import LoginManager

app=None
login_manager=None

#creating configuration between app, controller and db model
def setup_app():
    global app,login_manager
    app=Flask(__name__)

    #Configure login manager
    app.config["SECRET_KEY"]=SECRET_KEY
    login_manager=LoginManager()
    login_manager.init_app(app) #Link login manager to app

    #Data base settings
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///hms.sqlite3"
    app.url_map.strict_slashes = False  
    db.init_app(app) #linking between db and flask
    app.app_context().push() #Giving accees of my current app to other modules
    print("HMS app is setup done...")


setup_app() #calling

@login_manager.user_loader
def load_user(user_id):
    return User_Credentials.query.get(int(user_id))


#executable of flask
from controller import *
if __name__=="__main__":
    app.run(debug=True)
