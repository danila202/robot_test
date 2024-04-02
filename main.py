import uvicorn
from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from db.database import create_tables

from router import router as tasks_router
from router import main


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)


if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    asyncio.run(main())
