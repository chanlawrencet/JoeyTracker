from datetime import datetime, timedelta
import csv

dateStringToDateID = {
	'mo' : 1, 
	'tu' : 2, 
	'we' : 3, 
	'th' : 4, 
	'fr' : 5, 
	'sa' : 6, 
	'su' : 7,
}

dateToFullDate = {
	'mo' : "04/01/2019",
	'tu' : "04/02/2019",
	'we' : "04/03/2019",
	'th' : "04/04/2019",
	'fr' : "04/05/2019",
	'sa' : "04/06/2019",
	'su' : "04/07/2019",
}


locationToID = {
	'cc_p' : 0,
	'ds'   : 1,
	'tab'  : 2,
	'cc_t' : 3,
	'carm' : 4,
	'olin' : 5,
}

locationToLong = {
	'cc_p' : 'CC Pro Row',
	'ds'   : 'Davis Square',
	'tab'  : 'TAB',
	'cc_t' : 'CC Talbot',
	'carm' : 'Carm',
	'olin' : 'Olin',
}


days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
now = datetime.now()

def convertBack(oldDate):
	# start
	startDateTime = datetime.strptime('04/01/2019 00:00:00', '%m/%d/%Y %H:%M:%S')
	timedeltaDifference = now.date() - startDateTime.date()
	return oldDate + timedelta(weeks=(timedeltaDifference.days // 7))

def whatDay(nextJoey):
	if (now.isoweekday() == nextJoey.isoweekday()):
		return 'today'
	elif (now.isoweekday() + 1 == nextJoey.isoweekday()) or (now.isoweekday() == 7 and nextJoey.isoweekday() == 1):
		return 'tomorrow'
	else:
		return 'Monday'

location = input()
locationID = locationToID[location]
times = []	
for day in days:
	with open('./data/' + day + '.csv') as csvfile:
	    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	    for row in spamreader:
	    	if row[locationID] != '':
		    	times.append(datetime.strptime(dateToFullDate[day] + ' ' + row[locationID], '%m/%d/%Y %I:%M %p'))


firstOnMonday1 = times[:10]
firstOnMonday8 = []

for monDT in firstOnMonday1:
	firstOnMonday8.append(monDT + timedelta(weeks=1))
times = times + firstOnMonday8

# now
newdateString = '04/0' + str(now.isoweekday()) + '/2019 ' + now.time().isoformat('seconds')
newdateTime = datetime.strptime(newdateString, '%m/%d/%Y %H:%M:%S')


i = 0
while newdateTime > times[i]:
	i = i + 1

nextJoey = convertBack(times[i])
follJoey = convertBack(times[i+1])

message = 'The next Joey at ' + locationToLong[location] + ' is ' + whatDay(nextJoey) + " at " + nextJoey.strftime("%I:%M %p")
print(message)
message = 'The next following Joey is ' + whatDay(nextJoey) + " at " + follJoey.strftime("%I:%M %p")
print(message)









