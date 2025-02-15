import time
import datetime
import calendar
import pytz

def now(milliseconds=False):
    if milliseconds:
        return time.time() * 1000
    return time.time()

def day():
    return datetime.datetime.now().strftime('%A')

def isWeekDay():
    return True if datetime.datetime.now().strftime('%A') not in ["Saturday","Sunday"] else False

def isWeekend():
    return not isWeekDay()

def year():
    return int(datetime.datetime.now().strftime('%Y'))

def month():
    return int(datetime.datetime.now().strftime('%m'))

def dt(format="%d-%m-%Y",epoch=None):
    if epoch:
        return datetime.datetime.fromtimestamp(epoch).strftime(format)
    return datetime.datetime.now().strftime(format)

def isLastDay(workingDays=False):
    lastDay = calendar.monthrange(year(), month())[1]
    if workingDays:
        if datetime.datetime.now().strptime(f"{lastDay}-{month()}-{year()}","%d-%m-%Y").strftime('%A') == "Saturday":
            lastDay -= 1
        elif datetime.datetime.now().strptime(f"{lastDay}-{month()}-{year()}","%d-%m-%Y").strftime('%A') == "Sunday":   
            lastDay -= 2
    return lastDay == datetime.datetime.now().strftime('%-d')

def dateBetween(startDateStr, endDateStr, dateStr=None):
    if dateStr == None:
        dateStr = datetime.datetime.now().strftime('%H:%M %d-%m-%Y')
    startDate = datetime.datetime.strptime(startDateStr, '%H:%M %d-%m-%Y')
    endDate = datetime.datetime.strptime(endDateStr, '%H:%M %d-%m-%Y')
    date = datetime.datetime.strptime(dateStr, '%H:%M %d-%m-%Y')
    return startDate < date < endDate

def timeBetween(startTimeStr, endTimeStr, timeStr=None):
    if timeStr == None:
        timeStr = datetime.datetime.now().strftime('%H:%M')
    startTime = datetime.datetime.strptime(startTimeStr, '%H:%M')
    endTime = datetime.datetime.strptime(endTimeStr, '%H:%M')
    time = datetime.datetime.strptime(timeStr, '%H:%M')
    if startTime > endTime:
        return time >= startTime or time <= endTime
    else:
        return startTime <= time <= endTime

def datetimeToEpoch(datetimeStr,format="%Y%m%dT%H%M%S.%fZ"):
    dt = datetime.datetime.strptime(datetimeStr, format)
    return int(dt.timestamp())

def timezoneOffset(tz):
    dt = datetime.datetime.now(pytz.timezone(tz))
    return dt.strftime('%z')

def secondsToDays(seconds):
    return str(datetime.timedelta(seconds = seconds))

def adjustTime(timestamp=None,value=1,period="seconds"):
    if not timestamp:
        timestamp = time.time()
    return (datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(**{period : value})).timestamp()