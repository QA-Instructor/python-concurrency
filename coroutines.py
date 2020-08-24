import asyncio
import time

# using async marks a method or object as concurrent meaning it can be 
# scheduled for concurrent execution

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def example1():
    print(f"example1 - started at {time.strftime('%X')}")

    # an async routine can be called directly, it must be scheduled to run
    # so the two invocations below never occur
    say_after(1, '1 - hello')
    say_after(2, '1 - world')

    # the await keyword schedules coroutines for execution, 
    # and then blocks until coroutine has executed
    await say_after(1, '1 - hello')
    await say_after(2, '1 - world')

    print(f"example1 - finished at {time.strftime('%X')}")

# no awaiting in this example, the method comepletes before the 
# coroutines can be executed, because say_after() are created
# as part of this example coroutine, when this coroutine ends they end
async def example2_tasks_no_awaits():
    print(f"example2 - started at {time.strftime('%X')}")

    # using asyncio.create_task() creates and schedules a task to run immediately
    # but they never execute because the housing coroutine completes
    # execution before the schedular can run them
    task1 = asyncio.create_task(say_after(1, '2 - hello'))
    task2 = asyncio.create_task(say_after(2, '2 - world'))

    print(f"exampl2 - finished at {time.strftime('%X')}")

# in this example both tasks are awaited so execution is as expected
async def example3_tasks_with_both_awaits():
    print(f"example3 - started at {time.strftime('%X')}")

    # using asyncio.create_task() creates and schedules a task to run immediately
    task1 = asyncio.create_task(say_after(1, '3 - hello'))
    task2 = asyncio.create_task(say_after(2, '3 - world'))

    # in this context the await keyword simply blocks until each task completes
    # the creation and scheduling of the tasks was doen through 
    # the asyncio.create_task() method
    await task1
    await task2

    print(f"exampl3 - finished at {time.strftime('%X')}")

# in this example only task1 is awaited
async def example4_with_await_on_task1():
    print(f"example4 - started at {time.strftime('%X')}")

    # using asyncio.create_task() creates and schedules a task to run immediately
    task1 = asyncio.create_task(say_after(1, '4 - hello'))
    task2 = asyncio.create_task(say_after(2, '4 - world'))

    # in this context the await keyword schedules blocks until task1 completes
    # both tasks have started, but when task1 completes this housing coroutine
    # completes, not giving task2 the chance to complete because it has a 2 sec delay
    # so we only see "hello" printed out
    await task1

    print(f"exampl4 - finished at {time.strftime('%X')}")

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
    await task2

    print(f"exampl5 - finished at {time.strftime('%X')}")

asyncio.run(example1())
asyncio.run(example2_tasks_no_awaits())
asyncio.run(example3_tasks_with_both_awaits())
asyncio.run(example4_with_await_on_task1())
asyncio.run(example5_with_await_on_task2())
