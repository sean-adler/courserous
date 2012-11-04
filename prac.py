from bs4 import BeautifulSoup
import urllib2
from flask import Flask, render_template, url_for
import os
from datetime import datetime

app = Flask(__name__)

def formatTime(s):
    """Takes a string like '11:00am' and returns '11:00 AM'"""
    sL = list(s)
    sL.insert(-2, ' ')
    sL = [c.upper() for c in sL]
    s = ''.join(sL)
    return s

def timeIsBeforeNoon(timeStr):
    if timeStr.isspace():
        return False
    else:
        baseDate = '2012-01-01'
        pivotTimeStr = '12:00 PM'
        format = '%Y-%m-%d %I:%M %p'
        pivotTime = datetime.strptime(baseDate + ' ' + pivotTimeStr, format)
        time = datetime.strptime(baseDate + ' ' + formatTime(timeStr), format)
        return time < pivotTime
    

baseDate = '2012-01-01'
baseTime = '12:00 PM'
format = '%Y-%m-%d %I:%M %p'
pivotTime = datetime.strptime(baseDate + ' ' + baseTime, format)
## We'll compare every time to the pivot -- is our time before noon, or after noon?

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
            csList[-1]['timeSlot'] = ''


@app.route('/')
def show_all():
    return render_template('index.html', masterList=csList)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
