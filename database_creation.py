import pickle

DATABASE = {}

filehandler = open("DATABASE.obj","wb")
pickle.dump(DATABASE,filehandler)
filehandler.close()

