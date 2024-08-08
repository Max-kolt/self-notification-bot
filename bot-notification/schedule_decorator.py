import asyncio


def periodic(minutes: int = 1):
    """
    Executing a function in a periodic cycle
    :param minutes: period minutes
    """
    def scheduler(fcn):
        async def wrapper():
            while True:
                asyncio.create_task(fcn())
                await asyncio.sleep(minutes*60)

        return wrapper
    return scheduler

