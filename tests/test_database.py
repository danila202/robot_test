import pytest
from sqlalchemy import text, select

from db.database import create_tables, delete_tables, new_session, RobotLifeCycle


@pytest.mark.asyncio
async def test_write_database():
    await create_tables()

    try:
        async with new_session() as session:
            robot = RobotLifeCycle(start_time="00:02:00", duration="00:10:00", date="2024-02-01")
            session.add(robot)
            await session.commit()
            query = select(RobotLifeCycle)
            fetched_robot = await session.execute(query)
            assert fetched_robot is not None
            assert fetched_robot.first() is not None


    finally:
        await delete_tables()

