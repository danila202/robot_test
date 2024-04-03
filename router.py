from fastapi import APIRouter

import asyncio

from db.endpoint_decorators import deco_start_work, deco_end_work, robot_info
from db.repository import write_robot_info, get_all_entry
from robot import print_number

router = APIRouter(
    prefix='/robot',
    tags=["Робот"],
)

tasks = {}
number_of_bot = 1


@router.post("/start/{start_number}")
@deco_start_work(number_of_bot)
async def start_work(start_number: int):
    global number_of_bot
    task = asyncio.create_task(print_number(start_number))
    tasks[number_of_bot] = task
    number_of_bot += 1
    return {
        200: "OK"
    }


@router.post("/end/{number_bot}")
@deco_end_work
async def end_work(number_bot: int):
    if tasks.get(number_bot) is not None:
        kill_bot = tasks.get(number_bot)
        kill_bot.cancel()
        await write_robot_info(number_bot, robot_info)
        del tasks[number_bot]

        return {
            200: "OK"
        }
    else:
        return {
            400: f"Такой робот не запущен. Запущенные роботы {[*tasks.keys()]}"
        }


@router.get("/info")
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




