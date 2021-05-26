import gcsa.recurrence
from gcsa.recurrence import _DayOfTheWeek
import datetime
import calendar


def convertMonthToNum(month):
    x = 0
    if month == "Jan":
        x = 1
    elif month == "Feb":
        x = 2
    elif month == "Mar":
        x = 3
    elif month == "Apr":
        x = 4
    elif month == "May":
        x = 5
    elif month == "Jun":
        x = 6
    elif month == "Jul":
        x = 7
    elif month == "Aug":
        x = 8
    elif month == "Sep":
        x = 9
    elif month == "Oct":
        x = 10
    elif month == "Nov":
        x = 11
    else:
        x = 12
    return x

def convertDaysToList(days):
    list = {}
    count = 0
    for char in days:
        if char == 'M':
            list[count] = gcsa.recurrence.MONDAY
        elif char == 'T':
            list[count] = gcsa.recurrence.TUESDAY
        elif char == 'W':
            list[count] = gcsa.recurrence.WEDNESDAY
        elif char == 'R':
            list[count] = gcsa.recurrence.THURSDAY
        elif char == 'F':
            list[count] = gcsa.recurrence.FRIDAY
        count = count + 1
    return list

def dayToNum(day):
    num = 0
    if day[0] == 'T':
        num = 1
    elif day[0] == 'W':
        num = 2
    elif day[0] == 'R':
        num = 3
    elif day[0] == 'F':
        num = 4
    return num

def findDay(beginSemester, startClass):
    temp = datetime.datetime.strptime(beginSemester, '%d %m %Y').weekday()
    y = calendar.day_name[temp]
    ynum = dayToNum(y)
    xnum = dayToNum(startClass)
    if ynum > xnum:
        return 7 - (ynum - xnum)
    return xnum - ynum

def removeTBA(text):
    if text[0] == '<':
        text = 'TBA'
    return text
