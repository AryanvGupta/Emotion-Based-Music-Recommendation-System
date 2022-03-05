
# Import Libraires
from flask import Flask , request , render_template ,Markup, url_for
from tensorflow.keras import models
import cv2
import os
import numpy as np
import pandas as pd
import pickle
import smtplib, ssl
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array, load_img
app = Flask(__name__)
app.debug = True

# list to store playlist for each emotion 
playlist = ["https://www.youtube.com/playlist?list=PL_MH8gOS_ETiNT1NF8B46JYHZe6fXWfVW",
			"https://www.youtube.com/playlist?list=PL1VuYyZcPYIJTP3W_x0jq9olXviPQlOe1",
			"https://www.youtube.com/playlist?list=PLfQAe5M2BkwCKimscRq-F9wkO5tUPY9TS",
			"https://www.youtube.com/playlist?list=PLgzTt0k8mXzHcKebL8d0uYHfawiARhQja", 
			"https://www.youtube.com/playlist?list=PLLd27tZalu3zRpolGDrklbbS1T-L5Lc7g"]

# welcome page
@app.route("/")
def home():
	return render_template("welcome.html")

# back to login page
@app.route("/back")
def back():
	return render_template("login.html")

# user login page
@app.route("/login")
def login():
	return render_template("login.html")

# forgot password page
@app.route("/forgetPassword", methods=['POST'])
def forgotPassword():

	eid = str("")

	# query string gg for image operation 
	# query string for forgot pasword operation
	get = request.args.get('gg')
	if get == '1':
		# data loding and fetching
		eid = request.form['email']
		file = open("DATABASE.obj",'rb')
		object_file = pickle.load(file)
		file.close()

		exist = object_file.get(eid)
		if exist:
			# Email to password for forgot password
			gmail_user = 'autowareautomation@gmail.com' 
			gmail_password = 'Auto!1234'

			password = "Your Password is " + object_file[eid]["password"]
			
			sent_from = gmail_user
			to = [eid]
			subject = 'Forgot Password Request'
			body = f"Email Id: {eid} \n" + password

			email_text = """\
			From: %s
			To: %s
			Subject: %s

			%s
			""" % (sent_from, ", ".join(to), subject, body)

			try:
			    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			    smtp_server.ehlo()
			    smtp_server.login(gmail_user, gmail_password)
			    smtp_server.sendmail(sent_from, to, email_text)
			    smtp_server.close()
			    password = "Email sent successfully!"
			    print ("Email sent successfully!")
			except Exception as ex:
			    print ("Something went wrong….",ex)
		else:
			password = "Please create account! No such ID exist"
	else:
		password = ""

	return render_template("forgot_password.html", message = password, email = eid)

# user input 
@app.route("/input", methods = ["POST"])
def input():

	try:
		# data loding and fetching
		eid = request.form["email"]
		password = request.form["password"]
		file = open("DATABASE.obj",'rb')
		object_file = pickle.load(file)
		file.close()
		exist = object_file.get(eid)

		if exist:
			# authentication and verification
			if password == object_file[eid]["password"]:
				print("Welcome!",object_file[eid]["fname"])
				return render_template("input.html")
			else:
				message = "Incorrect Password!"
				print(message)
				return render_template("login.html",message=message)

		else:
			message = "No such ID/Password exist!"
			print(message)
			return render_template("login.html",message=message)

	except:
		message = "Please enter the required field!"
		print(message)
		return render_template("login.html",message=message)

# output
@app.route("/output", methods = ["POST"])
def output():
	classes = ('angry','happy','neutral', 'sad', 'surprise')

	get = request.args.get('gg')
	eid = request.args.get("eid")
	sid = request.args.get('sid')
	sid = int(sid)
	eid = int(eid)
	
	print(get,type(get))
	# emotion prediction using live feed (webcam)  
	if get == '0':
		face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
		classifier = models.load_model('./Emotion_Detection.h5')
		cap = cv2.VideoCapture(0)
		fd = 0
		while True:
			if fd:
				cap.release()
				break

			ret, frame = cap.read()
			labels = []
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			faces = face_classifier.detectMultiScale(gray,1.3,5)
			for (x,y,w,h) in faces:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
				roi_gray = gray[y:y+h,x:x+w]
				roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
				
				if np.sum([roi_gray])!=0:
					roi = roi_gray.astype('float')/255.0
					roi = img_to_array(roi)
					roi = np.expand_dims(roi,axis=0)

					preds = classifier.predict(roi)[0]
					max_index = preds.argmax()

					fd = 1


		cap.release()
		
	
	# emotion predtion using static image
	elif get == '2':
		imagename = request.form["image"]
		try:
			print("try!")
			face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
			classifier = models.load_model('./Emotion_Detection.h5')

			frame = cv2.imread("test/"+ imagename)

			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

			faces = face_classifier.detectMultiScale(gray,1.3,5)
			
			max_index = None

			for (x,y,w,h) in faces:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
				roi_gray = gray[y:y+h,x:x+w]
				roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
					
				if np.sum([roi_gray])!=0:
					roi = roi_gray.astype('float')/255.0
					roi = img_to_array(roi)
					roi = np.expand_dims(roi,axis=0)

					preds = classifier.predict(roi)[0]
					max_index = preds.argmax()

			if not max_index:
				raise

		except:
			message = "Face not detected. Please Try again!"
			print(message)
			return render_template("input.html", message = message)


	# emotion predtion using button
	else:
		max_index = request.args.get('eid')
		max_index = int(max_index)



	mood = classes[max_index]
	path = "static/songs/"+mood
	songs = os.listdir(path)
	song = path + "/" +songs[sid]
	songname = songs[sid][:-4]

	song1 = songs[0][:-4]
	song2 = songs[1][:-4]
	song3 = songs[2][:-4]
	song4 = songs[3][:-4]
	song5 = songs[4][:-4]
	link = playlist[eid]

	return render_template("output.html",eid=eid,mood=mood,songname= songname,song=song,song1=song1,song2=song2,song3=song3,song4=song4,song5=song5, link=link)

# sign up page
@app.route("/signup")
def signup():
	return render_template("signup.html")

# processing page
@app.route("/loading")
def loading():
	return render_template("loding.html")

# new user
@app.route("/signed" , methods=["POST"])
def signed():

	details = [i for i in request.form.values()]

	fname = details[0]
	eid = details[1]
	pw = details[2]
	cpw = details[3]

	if pw != cpw:
		print("Password doesn't match")

	# storing user data to database
	else:
		file = open("DATABASE.obj",'rb')
		object_file = pickle.load(file)
		file.close()

		if not object_file.get(eid):
			dts = {}
			dts["fname"] = fname
			dts["password"] = pw 
			dts["history"] = []

			object_file[eid] = dts 

			file = open("DATABASE.obj","wb")
			pickle.dump(object_file,file)
			file.close()

			print("User has been created :",dts)

		else:
			print("User already exist")
		
	return render_template("login.html")

if __name__ == '__main__':
	app.run(debug = True)