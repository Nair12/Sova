from numbers import Number
from datetime import datetime, UTC, timedelta

from shared import sessions


def check_user_session():
    to_delete = []
    for key,value in sessions.items():
        to_delete = []
        last_activity = value.last_activity
        if (datetime.now(UTC) - last_activity) > timedelta(minutes=15):
            to_delete.append(key)



    for key in to_delete:
        sessions.pop(key)








