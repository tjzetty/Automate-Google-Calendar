import re
from datetime import datetime, timedelta
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import *
from functions import convertMonthToNum, convertDaysToList, findDay

# open banweb detail class schedule and calendar
inputFile = open("class_scehdule_on_drive.txt", "r")  # downloaded webpage as txt file from banweb
calendar = GoogleCalendar('myemail@business.net') # until published this tool will only work for my email

# initialize variables
courseName = {}
courseNumber = {}

time = {}
startTime = {}
endTime = {}
days = {}
month = {}

location = {}
dateRange = {}
professor = {}

# HTML indicators to extract class info.
findClass = '<table class="datadisplaytable" summary="This layout table is used to present the schedule course detail"><caption class="captiontext">'
checkString = '<th class="ddheader" scope="col">Instructors</th>'

data = 0
index = -1
# extract class info and add to calendar
for line in inputFile:
    if findClass in line:
        index = index + 1
        # extracting substrings for course name and number
        course = re.findall('<caption class="captiontext">(.+)</caption>', line)[0]
        courseName[index] = re.findall('(.*?) - ', course)[0]
        courseNumber[index] = re.findall(' - (.*?) - (.*?)\Z', course)[0]
        courseNumber[index] = courseNumber[index][0] + " " + courseNumber[index][1]
    if checkString in line:
        data = 1
    if data > 0:
        if data == 5:
            time[index] = re.findall('<td class="dddefault">(.+)</td>', line)[0]
        if data == 6:
            days[index] = re.findall('<td class="dddefault">(.+)</td>', line)[0]
        if data == 7:
            location[index] = re.findall('<td class="dddefault">(.+)</td>', line)[0]
        if data == 8:
            dateRange[index] = re.findall('<td class="dddefault">(.+)</td>', line)[0]
        if data == 9:
            professor[index] = re.findall('<td class="dddefault">(.+)</td>', line)[0]
            data = -1
        data = data + 1

# Date and Month Calculations:
endRange = re.findall(' - (.*)', dateRange[0])[0]
monthStart = convertMonthToNum(re.findall('\A(.*?) ', dateRange[0])[0])
monthEnd = convertMonthToNum(re.findall(' - (.*?) ', dateRange[0])[0])
dateStart = int(re.findall(' (.*?), ', dateRange[0])[0])
dateEnd = int(re.findall(' (.*?),', endRange)[0])
yearStart = int(re.findall(', (.*?) - ', dateRange[0])[0])
yearEnd = int(re.findall(', (.+)', endRange)[0])

for x in range(0, index+1):
    startTime = 12
    endTime = 12
    hourStart = 0
    hourEnd = 0
    minStart = 0
    minEnd = 0

    paramFindDay = str(dateStart) + ' ' + str(monthStart) + ' ' + str(yearStart)
    # Adjust start date from semester start to real class start
    adjustDate = findDay(paramFindDay, days[x])

    if time[x][0] != '<':
        # Start Time Calculations: minutes, hours
        startTime = re.findall('(.*) - ', time[x])[0]
        if re.findall(' (.+)', startTime)[0][0] == 'p':
            hourStart = int(re.findall('(.+):', startTime)[0]) + 12
            minStart = int(re.findall(':(.+) p', startTime)[0])
        if re.findall(' (.+)', startTime)[0][0] == 'a':
            hourStart = int(re.findall('(.+):', startTime)[0])
            minStart = int(re.findall(':(.+) a', startTime)[0])

        # End Time Calculations: minutes, hours
        endTime = re.findall(' - (.+)', time[x])[0]
        if re.findall(' (.+)', endTime)[0][0] == 'p':
            hourEnd = int(re.findall('(.+):', endTime)[0]) + 12
            minEnd = int(re.findall(':(.+) p', endTime)[0])
        else:
            if re.findall(' (.+)', endTime)[0][0] == 'a':
                hourEnd = int(re.findall('(.+):', endTime)[0])
                minEnd = int(re.findall(':(.+) a', endTime)[0])

    if hourEnd == 24:
        hourEnd = 12
    if hourStart == 24:
        hourStart = 12

    daysOfWeek = list(convertDaysToList(days[x]).values())
    event = Event(
        courseName[x],
        start=datetime(year=yearStart, month=monthStart, day=dateStart, hour=hourStart, minute=minStart) + timedelta(adjustDate),
        end=datetime(year=yearStart, month=monthStart, day=dateStart, hour=hourEnd, minute=minEnd) + timedelta(adjustDate),
        minutes_before_popup_reminder=20,
        recurrence=Recurrence.rule(freq=WEEKLY, until=date(year=yearEnd, month=monthEnd, day=dateEnd), by_week_day=daysOfWeek)
    )
    calendar.add_event(event)
