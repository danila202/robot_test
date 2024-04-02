import uvicorn
from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager

from starlette.responses import JSONResponse

from db.database import create_tables
from db.endpoint_decorators import deco_start_work, deco_end_work, robot_info
from db.repository import write_robot_info, get_all_entry
from robot import print_number


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

tasks = {}
number_of_bot = 1



@app.post("/bot-start/{start_number}")
@deco_start_work(number_of_bot)
async def start_work(start_number: int):
    global number_of_bot
    task = asyncio.create_task(print_number(start_number))
    tasks[number_of_bot] = task
    number_of_bot += 1
    print(robot_info)
    return {
        200: "OK"
    }



@app.post("/bot-end/{number_bot}")
@deco_end_work
async def end_work(number_bot: int):
    if tasks.get(number_bot) is not None:
        kill_bot = tasks.get(number_bot)
        kill_bot.cancel()
        await write_robot_info(number_bot, robot_info)
        return {
            200: "OK"
        }
    else:
        return {
            400: f"Такой робот не запущен. Запущенные роботы {tasks.keys()}"
        }


@app.get("/bot-info")
async def get_entry():
    entries = await get_all_entry()
    data = []
    for entry in entries:
        data.append(
            {
                "id": entry.id,
                "start_time": entry.start_time,
                "duration": entry.duration,
                "date": entry.date
            }
        )
    return data


async def main():
    for task in tasks.values():
        await task


if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    asyncio.run(main())
