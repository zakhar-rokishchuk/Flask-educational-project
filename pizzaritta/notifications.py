from flask import session
from . import time_record


def add_notification(message):
    if not 'notifications' in session:
        session['notifications'] = []
    notification = {'message': message, 'time': time_record.get_time_unix()}
    session['notifications'].append(notification)


def get_notifications():
    if not 'notifications' in session:
        session['notifications'] = []
    for notification in session['notifications']:
        session.modified = True
        current_time = time_record.get_time_unix()
        if int((current_time - 2)) > int(notification['time']):
            session['notifications'].remove(notification)
    return session['notifications']