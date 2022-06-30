import time
from datetime import datetime


def get_time_unix():
    return time.mktime(datetime.now().timetuple())


def get_date_time():
    return datetime.fromtimestamp(get_time_unix())
    