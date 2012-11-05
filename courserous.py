## hackathon
## i'm on my disney shit

from bs4 import BeautifulSoup
import urllib2
from flask import Flask, render_template, url_for
import os
from datetime import datetime

app = Flask(__name__)

## Helper functions for timeSlot CSS class

def formatTime(s):
    """Takes a string like '11:00am' and returns '11:00 AM'"""
    sL = list(s)
    sL.insert(-2, ' ')
    sL = [c.upper() for c in sL]
    s = ''.join(sL)
    return s

def timeIsBeforeNoon(timeStr):
    if ':' not in timeStr:
        return False
    else:
        baseDate = '2012-01-01'
        pivotTimeStr = '12:00 PM'
        format = '%Y-%m-%d %I:%M %p'
        pivotTime = datetime.strptime(baseDate + ' ' + pivotTimeStr, format)
        time = datetime.strptime(baseDate + ' ' + formatTime(timeStr), format)
        return time < pivotTime

## More helper code for time comparisons
## We'll compare every time to the pivot -- is our time before noon, or after noon?

baseDate = '2012-01-01'
baseTime = '12:00 PM'
format = '%Y-%m-%d %I:%M %p'
pivotTime = datetime.strptime(baseDate + ' ' + baseTime, format)

## Create our kick-ass data structure

csSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=CSCI&yr=2013&sess=SP'))

### Construct the list of classes
csTrs = csSoup.findAll('tr')

csList = []
for i in range(35, len(csTrs) - 1):  ## courses start at 5th element of trs
    tags = [tag.text for tag in csTrs[i].findAll()]
    if len(tags) > 14:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        csList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'CS',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'
        } )
        
        if 'A R R' in csList[-1].values():
            ## fix 'ARR' fields
            csList[-1]['days'] = 'TBA'
            csList[-1]['startTime'] = ''
            csList[-1]['endTime'] = ''

        ## add general time flag

        


mathSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=MATH&yr=2013&sess=SP'))
mathTrs = mathSoup.findAll('tr')
mathList = []
for i in range(48, len(mathTrs) - 1):
    tags = [tag.next for tag in mathTrs[i].findAll()]
    if len(tags) > 14:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        mathList.append( {
            'course': [course], #[course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Math',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'
        } )
        
        if 'A R R' in mathList[-1].values():
            ## fix 'ARR' fields
            mathList[-1]['days'] = 'TBA'
            mathList[-1]['startTime'] = ''
            mathList[-1]['endTime'] = ''


danceSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=DANC&yr=2013&sess=SP'))
danceTrs = danceSoup.findAll('tr')
danceList = []

for i in range(23, len(danceTrs) - 1):
    tags = [tag.text for tag in danceTrs[i].findAll()]
    if len(tags) > 13:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        danceList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Dance',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in danceList[-1].values():
            ## fix 'ARR' fields
            danceList[-1]['days'] = 'TBA'
            danceList[-1]['startTime'] = ''
            danceList[-1]['endTime'] = ''

econSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=ECON&yr=2013&sess=SP'))
econTrs = econSoup.findAll('tr')
econList = []
for i in range(20, len(econTrs) - 1):
    tags = [tag.text for tag in econTrs[i].findAll()]
    if len(tags) > 13:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        econList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Economics',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in econList[-1].values():
            ## fix 'ARR' fields
            econList[-1]['days'] = 'TBA'
            econList[-1]['startTime'] = ''
            econList[-1]['endTime'] = ''

bioSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=BIOL&yr=2013&sess=SP'))
bioTrs = bioSoup.findAll('tr')
bioList = []
for i in range(96, len(bioTrs) - 1):
    tags = [tag.text for tag in bioTrs[i].findAll()]
    if len(tags) > 16:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        bioList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Biology',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in econList[-1].values():
            ## fix 'ARR' fields
            bioList[-1]['days'] = 'TBA'
            bioList[-1]['startTime'] = ''
            bioList[-1]['endTime'] = ''

chemSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=CHEM&yr=2013&sess=SP'))
chemTrs = chemSoup.findAll('tr')
chemList = []
for i in range(55, len(chemTrs) - 1):
    tags = [tag.text for tag in chemTrs[i].findAll()]
    if len(tags) > 16:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        chemList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Chemistry',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in chemList[-1].values():
            ## fix 'ARR' fields
            chemList[-1]['days'] = 'TBA'
            chemList[-1]['startTime'] = ''
            chemList[-1]['endTime'] = ''

engSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=ENGR&yr=2013&sess=SP'))
engTrs = engSoup.findAll('tr')
engList = []
for i in range(63, len(engTrs) - 1):
    tags = [tag.text for tag in engTrs[i].findAll()]
    if len(tags) > 16:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        engList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Engineering',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in engList[-1].values():
            ## fix 'ARR' fields
            engList[-1]['days'] = 'TBA'
            engList[-1]['startTime'] = ''
            engList[-1]['endTime'] = ''


govSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=GOVT&yr=2013&sess=SP'))
govTrs = govSoup.findAll('tr')
govList = []
for i in range(5, len(govTrs) - 1):
    tags = [tag.text for tag in govTrs[i].findAll()]
    if len(tags) > 16:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        govList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Government',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in govList[-1].values():
            ## fix 'ARR' fields
            govList[-1]['days'] = 'TBA'
            govList[-1]['startTime'] = ''
            govList[-1]['endTime'] = ''

psychSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=PSYC&yr=2013&sess=SP'))
psychTrs = psychSoup.findAll('tr')
psychList = []
for i in range(27, len(psychTrs) - 1):
    tags = [tag.text for tag in psychTrs[i].findAll()]
    if len(tags) > 16:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        psychList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Psychology',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in psychList[-1].values():
            ## fix 'ARR' fields
            psychList[-1]['days'] = 'TBA'
            psychList[-1]['startTime'] = ''
            psychList[-1]['endTime'] = ''


philSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=PHIL&yr=2013&sess=SP'))
philTrs = philSoup.findAll('tr')
philList = []
for i in range(11, len(philTrs) - 1):
    tags = [tag.text for tag in philTrs[i].findAll()]
    if len(tags) > 12:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        philList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Philosophy',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in philList[-1].values():
            ## fix 'ARR' fields
            philList[-1]['days'] = 'TBA'
            philList[-1]['startTime'] = ''
            philList[-1]['endTime'] = ''

litSoup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=LIT%20&yr=2013&sess=SP'))
litTrs = litSoup.findAll('tr')
litList = []
for i in range(12, len(litTrs) - 1):
    tags = [tag.text for tag in litTrs[i].findAll()]
    if len(tags) > 12:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        litList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'number': str(tags[0]),
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Literature',
            'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'

        } )
        
        if 'A R R' in litList[-1].values():
            ## fix 'ARR' fields
            litList[-1]['days'] = 'TBA'
            litList[-1]['startTime'] = ''
            litList[-1]['endTime'] = ''

## Concatenate lists together ##

masterList = csList + bioList + chemList + mathList + danceList + econList + \
             engList + govList + psychList + philList + litList


@app.route('/')
def show_all():
    return render_template('index.html', masterList=masterList)

#"""
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
#"""

"""
if __name__ == '__main__':
    app.run(port=3000)
"""

    
"""

### DAY(S) OF WEEK:

daysOfWeek = str(trs[7].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.string)

### TIME OF DAY, START:

timeStart = str(trs[7].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.string)

### TIME OF DAY, END:

timeEnd = str(trs[7].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.string)

### COURSE NAME:

course = str(trs[7].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.text).strip()


print daysOfWeek
print timeStart
print timeEnd
print course

classesList = []
for i in range(35, len(trs)-1):  ## courses start at 5th element of trs
    print i
    classesList.append({'course': str(trs[i].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.text).strip(),
                    'daysOfWeek': str(trs[i].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.string),
                    'timeStart': str(trs[i].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.string),
                    'timeEnd': str(trs[i].find('td').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.string)
                    })
"""
