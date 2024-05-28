from msilib import Feature
import os
import sys
import pathlib
import shutil
import re
import random
import time
import datetime
from typing import (
    List,
    Dict,
    NoReturn,
    Tuple,
    Callable,
    Any,
    Sequence,
)

import asyncio
import concurrent.futures
from concurrent.futures import (
    Future
)
import signal

import numpy as np
from sanic import file
import scipy as sp
import matplotlib.pyplot as plt
import japanize_matplotlib

async def async_hello():
    print('hello')
    await asyncio.sleep(1)
    print('world')

async def nested():
    return 54

async def async_top_level():
    print(await nested())

async def async_task_for_ready():
    task = asyncio.create_task(nested())
    print(await task)

# Future: 非同期処理の最終結果を表現する特別な低レベルのAwaitableオブジェクト
# Futureオブジェクトが待機(await)されているとは, Futureがどこか他の場所で
# 解決されるまでコルーチンが待機するということ
def blocking_io() -> Future:
    cur_dir: str = os.getcwd()
    filename: str = "random.txt"
    path: str = os.sep.join([
        cur_dir, filename
    ])
    with open(path, 'w') as f:
        f.write(f"ランダムな値: {random.randint(0, 100)}")
    future = Future()
    future.set_result('random fuck!!!')
    return future

def cpu_bound() -> Future:
    future = Future()
    pow_val: int = random.randint(a=1, b=6) # [1,5]
    future.set_result(sum(i * i for i in range (10 ** pow_val)))
    return future

async def async_executors():
    loop = asyncio.get_running_loop()

    # 1. Run in the default loop's executor
    future_1 = await loop.run_in_executor(executor=None, func=blocking_io)
    print('default thread pool future: ', future_1)
    print('result of future_1: ', future_1.result())


    # 2. Run in a custom thread pool
    with concurrent.futures.ThreadPoolExecutor() as thread_pool:
        # 事前に用意したカスタムスレッドプールで非同期用のイベントループを起動させる
        future_2_1 = await loop.run_in_executor(executor=thread_pool, func=cpu_bound)
        print('custom thread pool future_2_1: ', future_2_1)
        print('result of future_2_1: ', future_2_1.result())
        future_2_2 = await loop.run_in_executor(executor=thread_pool, func=cpu_bound)
        print('custom thread pool future_2_2: ', future_2_2)
        print('result of future_2_2: ', future_2_2.result())


    # # 3. Run in a custom process pool
    # with concurrent.futures.ProcessPoolExecutor() as process_pool:
    #     # 事前に用意したカスタムプロセスで非同期用のイベントループを起動させる
    #     future_3_1 = await loop.run_in_executor(executor=process_pool, func=cpu_bound)
    #     print('custom thread pool future_3_1: ', future_3_1)
    #     print('result of future_3_1: ', future_3_1.result())

def main_0():
    asyncio.run(async_hello())

def main_1():
    asyncio.run(async_top_level())

def main_2():
    asyncio.run(async_task_for_ready())

def main_3():
    asyncio.run(async_executors())

if __name__ == "__main__":
    # main_0()
    # main_1()
    # main_2()
    main_3()