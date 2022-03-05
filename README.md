# Emotion Based Music Recommendation System
 
Project details:
- Emotion based music recommender system takes the live feed from the camera and predict the mood(emotion) of the user.
- Based on user mood, system recommend the music playlist.
- Playlist are predefined on the database and result will be fetch according to the model predictions.
- User interface will be website created using HTML CSS Bootstrap and JavaScript
- Model may be completely trained from scratch or fine-tunned on pretrained model on architecture such as Mobilenet for low latency improved with haar cascade.

Primary Language: Python

Dataset: 
 Fer 2013: https://www.kaggle.com/msambare/fer2013 
 Affect net: https://www.kaggle.com/mouadriali/affectnetsample 

Deployment: Web based / Website
- Backend 
 - Database (.csv or Sqlite3) (stage 1 and stage 2)
 - Python and library numpy pandas sklearn extensively used (stage 1 and stage 3)
 - Deep Learning model (Tensorflow Keras hyperparameter finetuned model) (stage 7)
 - Model deployment using flask/Django on website (stage 8)

- Frontend
 - HTML CSS and Bootstrap (Stage 4)
 - JavaScript (stage 5)

-	Libraries in use:
  o	Numpy
  o	Pandas
  o	Matplotlib
  o	Cv2
  o	OS
  o	Random
  o	Tqdm
  o	Tensorflow
  o	Keras
  o	Sklearn
  o	Flask
  o	smtplib
