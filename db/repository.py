import asyncio
from typing import Dict
import datetime

from db.database import new_session, RobotLifeCycle


async def write_robot_info(number_bot: int, data: Dict[int, dict]):
    async with new_session() as session:
        robot = RobotLifeCycle(
            start_time = data[number_bot]["start_time"].strftime("%H:%M:%S"),
            duration = str(datetime.timedelta(seconds=data[number_bot]["duration"])).zfill(8),
            date = str(data[number_bot]["date"])
        )
        session.add(robot)
        await session.commit()
