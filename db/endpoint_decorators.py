from datetime import datetime
from functools import wraps

from db.repository import write_robot_info

robot_info = {}


def deco_start_work(number_of_bot):
    def deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal number_of_bot
            start = datetime.now()
            robot_info[number_of_bot] = \
                {
                    'start_time': start,
                    'duration': None,
                    'date': str(start.date())
                }
            response = await func(*args, **kwargs)
            number_of_bot += 1
            return response
        return wrapper
    return deco


def deco_end_work(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            robot_info[kwargs['number_bot']]['duration'] = \
                round((datetime.now() - robot_info[kwargs['number_bot']]['start_time']).total_seconds())
            result = await func(*args, **kwargs)
            del robot_info[kwargs['number_bot']]
        except KeyError:

            return {400: f"Такого робота нет"}

        return result
    return wrapper
