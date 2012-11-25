## utils.py
## Helper functions for 'timeSlot' CSS class ##

from datetime import datetime

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
