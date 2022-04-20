from datetime import datetime
import time


def get_time_unix():
    return time.mktime(datetime.now().timetuple())


def get_date_time():
    return datetime.fromtimestamp(get_time_unix())
    