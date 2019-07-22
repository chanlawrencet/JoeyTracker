from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime, timedelta, time
from pytz import timezone
import csv


dateIDToString = {
    1 : 'mo', 
    2 : 'tu', 
    3 : 'we', 
    4 : 'th', 
    5 : 'fr', 
    6 : 'sa', 
    7 : 'su',
}
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

idToLocation = {
    0 : 'cc_p',
    1 : 'ds',
    2 : 'tab',
    3 : 'cc_t',
    4 : 'carm',
    5 : 'olin',
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
app = Flask(__name__)
api = Api(app)


def prevDay(oldDay):
    return dateIDToString[7] if (dateStringToDateID[oldDay] - 1) == 0 else dateIDToString[dateStringToDateID[oldDay] - 1]


def nextDay(oldDay):
    return dateIDToString[7] if (dateStringToDateID[oldDay] + 1) % 7 == 0 else dateIDToString[(dateStringToDateID[oldDay] + 1) % 7]


def isBeforeEight(timeString):
    return datetime.strptime('04/01/2019 ' + timeString, '%m/%d/%Y %I:%M %p').time() < time(8,0,0,0)

def isBeforeEight24(timeString):
    return datetime.strptime('04/01/2019 ' + timeString, '%m/%d/%Y %H:%M:%S').time() < time(8,0,0,0)

def isAfterMidnight24(timeString):
    return datetime.strptime('04/01/2019 ' + timeString, '%m/%d/%Y %H:%M:%S').time() > time(0,0,0,0)

def convertBack(oldDate, now):
    # start
    startDateTime = datetime.strptime('04/01/2019 00:00:00', '%m/%d/%Y %H:%M:%S')
    timedeltaDifference = now.date() - startDateTime.date()
    return oldDate + timedelta(weeks=(timedeltaDifference.days // 7))


def whatDay(nextJoey, now):
    if (now.isoweekday() == nextJoey.isoweekday()):
        return 'today'
    elif (now.isoweekday() + 1 == nextJoey.isoweekday()) or (now.isoweekday() == 7 and nextJoey.isoweekday() == 1):
        return 'tomorrow'
    else:
        return 'Monday'


# TODO: make these time agnostic
def makeUnspecifiedMessageUntilEight(now, when):
    if now.isoweekday() != 6 and now.isoweekday() != 7 :
        message = 'Joey will arrive at and depart from ' + locationToLong['cc_p'] + ' ' + when + ' at 08:00 AM.'
    else:
        message = 'Joey will arrive at and depart from ' + locationToLong['cc_p'] + ' ' + when + ' at 11:00 AM.'

    return {"fulfillmentText": message}


def makeUnspecifiedMessage(now, locationID, nextLoc):
    message = 'Joey will arrive at and depart from ' + locationToLong[idToLocation[locationID]] + ' ' +  whatDay(nextLoc, now) + ' at ' + nextLoc.strftime("%I:%M %p") + '.'
    return {"fulfillmentText": message}

class getJoeyUnspecified(Resource):
    def get(self):
        eastern = timezone('US/Eastern')
        now = datetime.now(eastern)
        day = dateIDToString[now.isoweekday()]

        newDateString = '04/0' + str(now.isoweekday()) + '/2019 ' + now.time().isoformat('seconds')
        newDateTime = datetime.strptime(newDateString, '%m/%d/%Y %H:%M:%S')

        # need to check previous CSV if current time is before 8
        if isBeforeEight24(now.time().isoformat('seconds')):
            timesAfterMidnight = []
            with open('./data/' + prevDay(day) + '.csv') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

                for row in spamreader:
                    for i in range(0, len(row)):
                        if row[i] != '':
                            if isBeforeEight(row[i]):
                                # times before eight from yesterday are from today
                                tempDateTime = datetime.strptime(dateToFullDate[day] + ' ' + row[i], '%m/%d/%Y %I:%M %p')
                                timesAfterMidnight.append((i, tempDateTime))
            found = False
            nextJoeyEle = ''
            for pair in timesAfterMidnight:
                if pair[1] > newDateTime:
                    found = True
                    nextJoeyEle = pair
                    break

            if not found:
                return makeUnspecifiedMessageUntilEight(now, 'today')
            return makeUnspecifiedMessage(now, nextJoeyEle[0], convertBack(nextJoeyEle[1], now))

        times = []
        foundFirstAfterMidnight = False
        firstAfterMidnight = ''
        with open('./data/' + day + '.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                for i in range(0, len(row)):
                    if row[i] != '':
                        if not isBeforeEight(row[i]):
                            # times here are only within this day
                            tempDateTime = datetime.strptime(dateToFullDate[day] + ' ' + row[i], '%m/%d/%Y %I:%M %p')
                            times.append((i, tempDateTime))
                        elif not foundFirstAfterMidnight:
                            firstAfterMidnight = (i, datetime.strptime(dateToFullDate[nextDay(day)] + ' ' + row[i], '%m/%d/%Y %I:%M %p'))
                            foundFirstAfterMidnight = True
        found = False
        nextJoeyEle = ''
        for pair in times:
            if pair[1] > newDateTime:
                found = True
                nextJoeyEle = pair
                break

        # grab the first time from the next day; this occurs if time is between last trip before midnight and midnight
        if not found and foundFirstAfterMidnight:
            return makeUnspecifiedMessage(now, firstAfterMidnight[0], convertBack(firstAfterMidnight[1], now))
        elif not found:
            return makeUnspecifiedMessageUntilEight(now + timedelta(days=1), 'tomorrow')

        return makeUnspecifiedMessage(now, nextJoeyEle[0], convertBack(nextJoeyEle[1], now))

class getJoeySpecified(Resource):
    def get(self):
        location = request.headers['Data']

        eastern = timezone('US/Eastern')
        now = datetime.now(eastern)

        locationID = locationToID[location]
        times = []
        for day in days:
            with open('./data/' + day + '.csv') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if row[locationID] != '':
                        if isBeforeEight(row[locationID]):
                            times.append(datetime.strptime(dateToFullDate[nextDay(day)] + ' ' + row[locationID], '%m/%d/%Y %I:%M %p'))
                        else:
                            times.append(datetime.strptime(dateToFullDate[day] + ' ' + row[locationID], '%m/%d/%Y %I:%M %p'))

        # note: no need to worry about post-midnight Sunday times; they don't exist at the moment

        # add a few more overboard
        firstOnMonday1 = times[:10]
        firstOnMonday8 = []

        for monDT in firstOnMonday1:
            firstOnMonday8.append(monDT + timedelta(weeks=1))
        times = times + firstOnMonday8

        # now
        newDateString = '04/0' + str(now.isoweekday()) + '/2019 ' + now.time().isoformat('seconds')
        newDateTime = datetime.strptime(newDateString, '%m/%d/%Y %H:%M:%S')


        i = 0
        while newDateTime > times[i]:
            i = i + 1

        nextJoey = convertBack(times[i], now)
        follJoey = convertBack(times[i+1], now)
        nextMessage = 'The next Joey at ' + locationToLong[location] + ' is ' + whatDay(nextJoey, now) + ' at ' + nextJoey.strftime("%I:%M %p") + '.'
        follMessage = 'The following one is ' + whatDay(follJoey, now) + ' at ' + follJoey.strftime("%I:%M %p") + '.'

        fulfillmentText = nextMessage + '\n' + follMessage

        return {"fulfillmentText": fulfillmentText}


api.add_resource(getJoeySpecified, '/getJoeySpecified')
api.add_resource(getJoeyUnspecified, '/getJoeyUnspecified')


if __name__ == '__main__':
    app.run(debug=True)


