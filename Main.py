
from string import hexdigits
from flask import Flask, url_for, redirect, render_template, session, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from WebTools import webTools
from pprint import pprint
import json






app = Flask(__name__)
db = SQLAlchemy(app) #creates database instance


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userDB.db' #connects to user database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'RDYUI*HOU(&&@L}>KHM:@~' 




class Users(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      username = db.Column(db.String(20), nullable=False, unique=True)
      password = db.Column(db.String(80), nullable=False)
      mail = db.Column(db.String(100), nullable=False, unique=True)

      def __init__(self, username, password, mail):
            self.username = username
            self.password = password
            self.mail = mail


#login page
@app.route("/login",  methods=["GET","POST","DELETE"])
def login():
      session.permanent = True

      if request.method == "POST":
            
            user = request.form['username']
            passwd = webTools.Encrypt(request.form['password'].encode())
            found_user = Users.query.filter_by(username = user, password = passwd ).first() #checks if user name exists in db
            
            if found_user:
                  session["user"] = user
                  session['password'] = passwd
                  return redirect(url_for("userHome"))
            else:
                  flash("Invalid username or password", "info")
                  return render_template("Login.html", pg_title = "Code")
                   
      else:
            if "user" in session:
                  return redirect(url_for("userHome"))
            else:
                  return render_template("Login.html", pg_title = "Code")
     


#sign up
@app.route("/addUser", methods=["GET","POST","DELETE"])
def addUser():
      if request.method == "POST":
            username = request.form['username']
            userMail = request.form['userMail']
            password = webTools.Encrypt(request.form['password'].encode())
            found_user = Users.query.filter_by(username = username).first()
            found_email = Users.query.filter_by(mail = userMail).first()


            if found_user or found_email:
                  flash("Username or email not available")
                  return render_template("signup.html", pg_title = "Code")

            session["user"] = username
            session["Mail"] = userMail
            session['Password'] = password

            user = Users(session['user'], session['Password'], session['Mail'])
            db.session.add(user)
            db.session.commit()
            print("ID: ", user.id)
            return redirect(url_for("userHome"))
      else:
            return render_template("signup.html", pg_title = "Code")
      




#logged in home page
@app.route("/user", methods = ["POST","GET","DELETE"])
def userHome():
      #username = None
      if "user" in session:
            user = session["user"]
            return render_template("userIndex.html", pg_title = "Code", usr = user)
      else:
            return redirect(url_for("login", pg_title = "Code"))

#consider making each page take an extra argument, user = session["user"], which can then 
#be defined globally.




@app.route("/details", methods = ["POST","GET","DELETE"])
def details():
      if 'user' in session:
            if request.method == "POST":
                  user = Users.query.filter_by(username = session['user']).first()

                  newUsername = request.form['username']
                  newMail = request.form['userMail']
                  newPassword = webTools.Encrypt(request.form['password'].encode()) 

                  user.username = newUsername
                  user.mail = newMail
                  user.password = newPassword
                  db.session.commit()
                  flash("Details updated successfully. Please log in again")
                  return redirect(url_for('logout'))

            else:
                  user = Users.query.filter_by(username = session['user']).first()
                  return render_template('userDetails.html', pg_title = "Code" ,usr = user.username, username = user.username , mail = user.mail , password = user.password )
      else:
            return redirect(url_for('login'))





@app.route('/get_data/<language>/<name>/<id>', methods=['POST','GET', 'DELETE'])
#name is name of project
#id is the id of the given project in the json

def get_data(name,id,language):
      id_ = int(id)
      JSONpath = 'static/' + language + '.json'
      file = open(JSONpath,'r')
      data = file.read()
      jsonStr = json.loads(data)
      print(jsonStr[id_])
      return jsonify(jsonStr[id_])


#Language pages





@app.route('/scan_folder/<language>')
def scan_folder(language):
      print('LANG:', language)
      webTools.scanDX('/home/pi/Desktop/Programming_projects/' + language +'/', language, '/home/pi/Desktop/File_dir 3.0/static/' + language + '.json' )
      print('scan success')
      return(redirect(url_for(language)))




@app.route("/python", methods = ['GET','POST','DELETE'])
def python():
      if "user" in session:
            #Loads project data and displays it in main results table  
            user = session["user"]
            jsonFile = open('static/python.json','r')
            data = jsonFile.read()
            tabData = json.loads(data)
            pprint(tabData)
            return render_template("Python.html", pg_title = "Python", usr = user, tabData = tabData)
      else:
            return redirect(url_for('login'))




@app.route("/WebLang")
def WebLang():
      

      if 'user' in session:
            user = session["user"]
            jsonFile = open('static/WebLang.json','r')
            data = jsonFile.read()
            tabData = json.loads(data)
            pprint(tabData)
            return render_template('HTML:CSS:JS.html', pg_title = "WebDev", usr = session['user'], tabData = tabData)

      else:
            return redirect(url_for('login'))
            


@app.route("/cpp")
def cpp():
      if 'user' in session:
            user = session["user"]
            jsonFile = open('static/cpp.json','r')
            data = jsonFile.read()
            tabData = json.loads(data)
            pprint(tabData)
            return render_template('C++.html', pg_title = "C++", usr = session['user'], tabData = tabData)

      else:
            return redirect(url_for('login'))



@app.route("/Java")
def Java():
      if 'user' in session:
            user = session["user"]
            webTools.scanDX('/home/pi/Desktop/Programming_projects/Java/', 'HTML', '/home/pi/Desktop/File_dir 3.0/static/Java.json' )
            jsonFile = open('static/Java.json','r')
            data = jsonFile.read()
            tabData = json.loads(data)
            return render_template('Java.html', pg_title = "Java", usr = session['user'], tabData = tabData)

      else:
            return redirect(url_for('login'))


#Logout

@app.route("/logout")
def logout():
      session.pop("user", None) #clears all user session data
      return redirect(url_for("login"))

if __name__ == "__main__":
      db.create_all()
      app.run(debug = True)



#UPDATE 07/03/2022: Project view is now implemented on all language pages
# however, still only able to go inside a single layer of subfolders. 
# Download button added to LangBase, however is not yet active.
# NEXT SESSION:
#           -Put download button in correct place
#           -Make download button show, only when a project is selected
#           -Create test zip file to download
#           -Write python script to automatically zip a given directory
#           -Activate download button. Will need the button to request the file from 
#           -the server, and then download it.
#
# If all of the above is completed, then start thinking about uploading files.
# When a file is uploaded, if it is an update of a project that is already on the server,
# then need it to automatically update the correct files/folders, then store a zip
# of the previous version.


#UPDATE 06/03/2022: Project view now working on all pages, and one can now go inside a subfolder (only 1 layer deep so far)
#refresh button is now working, but only on the python page. Need to update the scan_folder function so that it can scan the 
#correct folder depending on the language.
#NEXT SESSION: Update scan_folder as described above. Check if PyData function is being used anywhere, if not then delete it.
# attempt to allow users to go into as many folders as needed. Begin making files downloadable. Will need to zip folders to be
# downloaded. Maybe create a python script that can create an up to date zip of a project (put this script inside WebTools.py)
# and make this accessible from the front-end. Also need to make each table column the same length. This would need to depend
# on the length required to contain the filename.


#UPDATE 05/03/2022: Project view is working on python and c++ pages, however 
#need to re-scan the folders when needed. 
#NEXT SESSION: create a button that can re-scan a folder when needed. Maybe 
#make this an admin only action? Need to implement Main.js into all other neccessary
#pages. 
# 
#IDEAS: 
#      -Inside project files window, if a folder is clicked, need to show contents of
#       that folder.
#      -Make individual files downloadable, as well as entire folders.
#      -When downloading a folder, there needs to be a zipped version.
#      -is it possible to create a zip from the front end? if so, implement as admin action



#UPDATE 20/02/2022: Project View is now functioning, but still needs some improving. 
#NEXT SESSION: when project is selected, try to request only the json data for that project 
# rather than importing the entire python.json data. See if fetch api can send the location of 
# the project data inside the json file to the server, then display the data using the same method
# as the main results table. This will make it easier and more efficient to implement on the 
# other language pages. Once this is complete, need to make files uploadable/downloadble.



#UPDATE 19/02/2022: File scanner fully working using JSON database. 
# Main results table now functioning. changing password is not working properly.
# NEXT SESSION: check password changing function. It may not be running the typed password through 
# the SHA256 algorithm. Need to get project view working, need it to be able to access contents of subfolders.


#UPDATE 14/02/2022: file scanner is semi implemented. So far, it collects the desired data and stores it inside of nested dictionaries. Need to
#make it insert data into a sql or json database. Password hashing is fully implemented using SHA256. 
#NEXT SESSION GOAL: update filescanner algorithm so that everything is stored in a database. Start working on displaying results in language pages, and make 
#a button to run the filescanner when a new folder is created. This can then evolve into auto updating the database when a file is uploaded to the server.
#
#THOUGHTS/IDEAS: can i create a folder from the webpage? download/update individual project files or just update entire project? 





#_____________________________________________________________________________________________________________________________________________

# Get results working again - implement file scanner into server code so that it can automatically display updates in real time.
# add in rest of pages - still need to create profile, messages, projects pages.

# implement instant messaging
# profiles
#     - profile pictures
#     - newsfeed
#     - profile search
#     - add friends



