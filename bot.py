import asyncio
import sys


async def print_number(start_num: int = 0):

    while True:
        print(start_num)
        await asyncio.sleep(1)
        start_num += 1


async def main():
    if len(sys.argv) > 1:
        await asyncio.create_task(print_number(int(sys.argv[1])))
    else:
        await asyncio.create_task(print_number())


if __name__ == "__main__":
    asyncio.run(main())


