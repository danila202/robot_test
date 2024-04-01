import asyncio
import sys


async def print_number(start_num: int):
    while True:
        print(start_num)
        await asyncio.sleep(1)
        start_num += 1


if __name__ == "__main__":
    start_num = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    asyncio.run(print_number(start_num))


