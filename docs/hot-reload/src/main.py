import asyncio

from m1.s import s
from m2.r import r

async def main():
    print("main")
    s()
    r()
    await asyncio.Future()

asyncio.run(main())
