##     CourserousMaximus     ##
## Sean Adler & Sean McQueen ##

from bs4 import BeautifulSoup
import urllib2
from flask import Flask, render_template
import os
from utils import *

app = Flask(__name__)

## All department URLs we parse have the same "root", basically a long string ##
## that includes a four-letter code near the end, like 'PSYC' for Psychology. ##

baseURL = 'https://portal.claremontmckenna.edu/ics/Portlets/CRM/CXWebLinks/Port\
let.CXFacultyAdvisor/CXFacultyAdvisorPage.aspx?SessionID={25715df1-32b9-42bf-90\
33-e5630cfbf34a}&MY_SCP_NAME=/cgi-bin/course/pccrscatarea.cgi&DestURL=http://cx\
-cmc.cx.claremont.edu:51081/cgi-bin/course/pccrslistarea.cgi?crsarea=%s&yr=2013\
&sess=SP'

class Department():

    def __init__(self, name, deptCode, firstTrTag, minTagLength, math=False):
        """Stores course data by having BeautifulSoup parse tags at the URL,
            then adds all tags containing course data to a list.
            The 'math' argument is a bit of a hack; for some reason, the Math
            department has a slightly different web page than others."""
        soup = BeautifulSoup(urllib2.urlopen(baseURL % deptCode))
        trs = soup.findAll('tr')
        self.list = []
        ## The 'first' tr tag is the first tag on a page which actually holds course data. ##
        for i in range(firstTrTag, len(trs) - 1):
            tags = [tag.text for tag in trs[i].findAll()]
            if len(tags) > minTagLength:
                course = str(tags[-2]).strip()
                days = str(tags[-5])
                days = days.replace('-', '')
                days = days.strip()
                days = ' '.join(days)
                ## Add all courses to the list. ##
                self.list.append( {
                    ## The weird Math inconsistency mentioned above:    ##
                    ## Remove any lingering 'Textbook Info' in the tag. ##
                    ## We don't have to do this for the Math page.      ##
                    'course': [course] if math else [course[:course.find('  ')]],
                    'number': str(tags[0]),
                    'days': days,
                    'startTime': str(tags[-4]),
                    'endTime': str(tags[-3]),
                    'prof': str(tags[2]),
                    'dept': name,
                    'timeSlot': 'Morning' if timeIsBeforeNoon(str(tags[-4])) else 'Afternoon'
                    } )
        ## We make all "arranged" or "A R R" courses store no time data. ##
        if 'A R R' in self.list[-1].values():
            self.list[-1]['days'] = 'TBA'
            self.list[-1]['startTime'] = ''
            self.list[-1]['endTime'] = ''

## Now for the fun part: Use our Department class a bunch! ##


cs = Department('CS',
                'CSCI',
                35,
                14)

dance = Department('Dance',
                   'DANC',
                   23,
                   13)

econ = Department('Economics',
                  'ECON',
                  20,
                  13)

bio = Department('Biology',
                 'BIOL',
                 96,
                 16)

chem = Department('Chemistry',
                  'CHEM',
                  55,
                  16)

eng = Department('Engineering',
                 'ENGR',
                 63,
                 16)

gov = Department('Government',
                 'GOVT',
                 5,
                 16)

phil = Department('Philosophy',
                  'PHIL',
                  11,
                  12)

lit = Department('Literature',
                 'LIT',
                 13,
                 12)

math = Department('Math',
                  'MATH',
                  48,
                  14,
                  math=True)

psych = Department('Psychology',
                   'PSYC',
                   27,
                   16)


masterList = bio.list + chem.list + cs.list + dance.list + econ.list + \
             eng.list + gov.list + lit.list + math.list + phil.list + \
             psych.list

## Inject masterList into webpage. ##

@app.route('/')
def show_all():
    return render_template('index.html', masterList=masterList)

## Flask/Heroku boilerplate. ##

if __name__ == '__main__':
    ## Bind to PORT if defined, otherwise default to 5000. ##
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
