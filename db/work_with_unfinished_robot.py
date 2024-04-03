from datetime import datetime

from db.endpoint_decorators import robot_info
from db.repository import write_robot_info


def update_duration_in_tasks_for_unfinished_robot():
    time_now = datetime.now()
    for key, value in robot_info.items():
        robot_info[key]['duration'] =\
            round((time_now - robot_info[key]['start_time']).total_seconds())


async def write_unfinished_robot():
    update_duration_in_tasks_for_unfinished_robot()
    for key in robot_info.keys():
        await write_robot_info(key, robot_info)