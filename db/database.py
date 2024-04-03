from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///robot.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class RobotLifeCycle(Model):
    __tablename__ = "robot_life_cycle"
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[str]
    duration: Mapped[str]
    date: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)



async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)