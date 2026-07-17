from flask import Flask
from models import db

app=None

#creating configuration between app, controller and db model
def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///hms.sqlite3"
    db.init_app(app) #linking between db and flask
    app.app_context().push() #Giving accees of my current app to other modules
    print("HMS app is setup done...")

#executable of flask
setup_app() #calling
from controller import *
if __name__=="__main__":
    app.run(debug=True)
