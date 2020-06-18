import pytz
from datetime import datetime, timezone

local_tz = pytz.timezone('Asia/Ho_Chi_Minh') # use your local timezone name here
# NOTE: pytz.reference.LocalTimezone() would produce wrong result here

## You could use `tzlocal` module to get local timezone on Unix and Win32
# from tzlocal import get_localzone # $ pip install tzlocal

# # get local timezone    
# local_tz = get_localzone()

utc=pytz.UTC

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def now_between_t1_t2(t1,t2):
    t1 = utc.localize(t1)  
    t2 = utc.localize(t2)
    return t1 < utc_to_local(datetime.now()) < t2