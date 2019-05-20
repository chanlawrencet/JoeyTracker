f = open('workfile', 'w')
#f.write("[")
theInput = ""
theInput = input()
while (theInput != "done"):
	f.write("\'")
	f.write(theInput)
	f.write("\'")
	f.write(",")
	theInput = input()
#f.write("]")

