## hackathon
## i'm on my disney shit

from bs4 import BeautifulSoup
import urllib2
from flask import Flask, render_template, url_for

app = Flask(__name__)

## Create our kick-ass data structure

soup = BeautifulSoup(urllib2.urlopen('https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Portlet.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-9033-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=CSCI&yr=2013&sess=SP'))

### Construct the list of classes
trs = soup.findAll('tr')

masterList = []
for i in range(35, len(trs) - 1):  ## courses start at 5th element of trs
    tags = [tag.text for tag in trs[i].findAll()]
    if len(tags) > 14:
        course = str(tags[-2]).strip()
        days = str(tags[-5])
        days = days.replace('-', '')
        days = days.strip()
        days = ' '.join(days)
        masterList.append( {
            'course': [course[:course.find('  ')]],  ## strip the 'Textbook Info' bullshit
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'CS'
        } )
        
        if 'A R R' in masterList[-1].values():
            ## fix 'ARR' fields
            masterList[-1]['days'] = 'TBA'
            masterList[-1]['startTime'] = ''
            masterList[-1]['endTime'] = ''


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
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Math'
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
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Dance'
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
            'days': days,
            'startTime': str(tags[-4]),
            'endTime': str(tags[-3]),
            'prof': str(tags[2]),
            'dept': 'Economics'
        } )
        
        if 'A R R' in econList[-1].values():
            ## fix 'ARR' fields
            econList[-1]['days'] = 'TBA'
            econList[-1]['startTime'] = ''
            econList[-1]['endTime'] = ''


## Concatenate lists together?? ##

masterList += mathList + danceList + econList


@app.route('/')
def show_all():
    return render_template('index.html', masterList=masterList)

if __name__ == '__main__':
    app.run(port=3000)

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
