import ntptime
import utime
import time
 
 
wday = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
 
def zfill(s, width):
    if len(s) < width:
        return ("0" * (width - len(s))) + s
    else:
        return s
 
def get_now():
    datetimetuple = ntptime.time()
    year = str(datetimetuple[0])
    month = zfill(str(datetimetuple[1]),2)
    mday = zfill(str(datetimetuple[2]),2)
    hour = zfill(str(datetimetuple[3]),2)
    minute = zfill(str(datetimetuple[4]),2)
    seconds = zfill(str(datetimetuple[5]),2)
    wd_index = datetimetuple[6]
    datetime = year + "/" + month + "/" + mday + " " + wday[wd_index] + " " + hour + ":" + minute + ":" + seconds
    return datetime