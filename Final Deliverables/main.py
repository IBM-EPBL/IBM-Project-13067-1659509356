import os
import cv2
import pyrebase
import tensorflow as tf

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)       #Initialze flask constructor

loaded_model = tf.keras.models.load_model('IBM-Project-model.h5')

def preprocess_img(Image_path):
    X = []
    IMG_SIZE = 128
    img = cv2.imread(Image_path,cv2.IMREAD_UNCHANGED)
    kernel = np.array([[0, -1, 0],
                [-1, 5,-1],
                [0, -1, 0]])
    image_sharp = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    img_binary = cv2.resize(image_sharp, (IMG_SIZE,IMG_SIZE))
    X.append(np.array(img_binary))
    train_x=np.array(X,dtype=np.uint8)
    train_x=train_x/255
    return train_x


Fruits_map = {
    0 : "Apple",
    1 : "Banana",
    2 : "Orange",
    3 : "Pineapple",
    4 : "Watermelon"
}


config = {
  "apiKey": "AIzaSyAoOt0FQjAfTI0VuJ3u5Cjj-8xb420tsVw",
  "authDomain": "ibm-project-86cae.firebaseapp.com",
  "databaseURL": "https://ibm-project-86cae-default-rtdb.firebaseio.com",
  "projectId": "ibm-project-86cae",
  "storageBucket": "ibm-project-86cae.appspot.com",
  "messagingSenderId": "645635521240",
  "appId": "1:645635521240:web:573c4137733bb7dbcc75ad",
  "measurementId": "G-TRRJE8LBLD"
}
#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

Fruit = ""

#Login

@app.route("/upload", methods=['GET', 'POST'])
def data_page():
    if person["is_logged_in"] == False:
        return redirect(url_for('login'))

    if request.method == 'POST':
        filesDict = request.files.to_dict()
        uploadData = request.files['media']
        data_file_name = uploadData.filename
        uploadData.save(os.path.join(app.root_path, 'uploads\\' + data_file_name))
        Image_path = os.path.join(app.root_path, 'uploads\\' + data_file_name)
        processed_tensor = preprocess_img(Image_path)
        pred = loaded_model.predict(processed_tensor)
        pred_classes = np.argmax(pred,axis = 1)
        global Fruit 
        Fruit = Fruits_map[pred_classes]




    return render_template("upload.html")

@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        iframe = "upload"
        return render_template("welcome.html", email = person["email"], name = person["name"],iframe = iframe)
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information

            user = auth.sign_in_with_email_and_password(email, password)
            print("Sign in success")
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except Exception as e:
            #If there is any error, redirect back to login
            print(e)
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run()
