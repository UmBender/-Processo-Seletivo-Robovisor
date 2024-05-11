import asyncio
import os

queue = asyncio.Queue()


async def producer():
    while True:
        if os.path.isfile("./cache"):
            file = open("./cache", "r")
            f = file.read()
            f = f.split("\n")
            file.close()
            os.system("rm ./cache")
            for i in f:
                if (i != ""):
                    print(i)
                    await queue.put(i)
        await asyncio.sleep(3)


async def consumer(queue):
    consumed = 0
    while True:
        token = await queue.get()
        os.system(f"echo \'{token}\' > .temp")
        festival_command = "festival --tts .temp"
        process = await asyncio.create_subprocess_shell(
            festival_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        os.system("rm .temp")
        queue.task_done()
        consumed += 1
        os.system(f"echo '{consumed} : \"{token}\"' >> .log")
        await asyncio.sleep(1)


async def main():
    print("UP READER")

    producers = [asyncio.create_task(producer()) for _ in range(1)]
    consumers = [asyncio.create_task(consumer(queue)) for _ in range(1)]

    await asyncio.gather(*consumers)
    await asyncio.gather(*producers)


if __name__ == "__main__":
    asyncio.run(main())
