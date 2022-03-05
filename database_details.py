import pickle 

file = open("DATABASE.obj",'rb')
object_file = pickle.load(file)

print("Email | Name | Password | History ")
for key,value in object_file.items():
	temp = [key]
	for k,v in value.items():
		temp.append(v)

	temp[-1] = ",".join(temp[-1])
	print(" | ".join(temp))

file.close()

