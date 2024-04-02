from datetime import datetime
from functools import wraps

from db.repository import write_robot_info

robot_info = {}


def deco_start_work(number_of_bot):
    def deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = datetime.now()
            robot_info[number_of_bot] = \
                {
                    'start_time': start,
                    'duration': None,
                    'date': str(start.date())
                }
            response = await func(*args, **kwargs)
            return response
        return wrapper
    return deco


def deco_end_work(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        robot_info[kwargs.get('number_bot')]['duration'] = \
            round((datetime.now() - robot_info[kwargs.get('number_bot')]['start_time']).total_seconds())
        result = await func(*args, **kwargs)

        return result
    return wrapper
