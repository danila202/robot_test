from datetime import datetime

import uvicorn
from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from db.database import create_tables
from db.work_with_unfinished_robot import write_unfinished_robot

from router import router as tasks_router, tasks




@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await write_unfinished_robot()

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)


async def main():
    for task in tasks.values():
        await task


if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    asyncio.run(main())
