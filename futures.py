import asyncio
import time

# using async marks a method or object as concurrent meaning it can be 
# scheduled for concurrent execution

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return what

async def using_a_future( delay, theFuture ):
    print("I'll set the future when I'm done")
    await asyncio.sleep(delay)
    theFuture.set_result( "using_a_future is done")

#@asyncio.coroutine
async def loop_till( delay, count, future):
    for x in range(2):
        #await asyncio.sleep(delay)
        #yield x
        future.set_result(x)
    future.set_result(-1)

async def example1():
    print(f"example1 - started at {time.strftime('%X')}")

    # the await keyword schedules coroutines for execution, 
    # and then blocks until coroutine has executed
    future  = await say_after(1, '1 - hello')
    print( future )

    if asyncio.iscoroutinefunction(say_after):
        print( "say_after() is a coroutine()")

    if asyncio.isfuture( future ):
        print("this is a future object")

    await say_after(2, '1 - world')

    print(f"example1 - finished at {time.strftime('%X')}")

# in this example only task2 is awaited
async def example5_with_await_on_task2():
    print(f"example5 - started at {time.strftime('%X')}")

    # using asyncio.create_task() creates and schedules a task to run immediately
    task1 = asyncio.create_task(say_after(1, '5 - hello'))
    task2 = asyncio.create_task(say_after(2, '5 - world'))

    # in this context the await keyword schedules blocks until task2 completes
    # both tasks have started, because task1 only executes for 1 sec it can completes 
    # before task2 completes.  When task2 completes the housing coroutines continues
    # its execution so we see printed out "hello" "world"
    future = await task2

    if asyncio.isfuture( task2 ):
        print("task2 is a future, its value is: ", future)

    print(f"example5 - finished at {time.strftime('%X')}")

async def example3_creating_wating_on_future():
    print(f"example3 - started at {time.strftime('%X')}")
    loop = asyncio.get_event_loop()

    future = loop.create_future()
    asyncio.create_task(using_a_future(5, future))

    await future
    print( future.result() )

    print(f"example3 - finished at {time.strftime('%X')}")

async def example4_using_yield_for_a_future():
    print(f"example4 - started at {time.strftime('%X')}")
    loop = asyncio.get_event_loop()

    future = loop.create_future()
    asyncio.create_task(loop_till(1, 5, future))

    await future

    while future.result() != -1:
        print( future.result() )
        await future

    print(f"example4 - finished at {time.strftime('%X')}")

# asyncio.run(example1())
# asyncio.run(example5_with_await_on_task2())
# asyncio.run(example3_creating_wating_on_future())
asyncio.run(example4_using_yield_for_a_future())

