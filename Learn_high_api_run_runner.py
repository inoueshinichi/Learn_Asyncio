import os
import sys
import pathlib
import shutil
import re
import random
import time
import datetime

import asyncio
import signal

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import japanize_matplotlib

def handler_gracefull_shutdown(signum: int):
    print(f"シグナル{signum}を受け取りました.")
    print("Gracefull shutdownを実行します.")
    loop.stop()

async def async_hello():
    await asyncio.sleep(1)
    print('hello')

async def async_thank():
    await asyncio.sleep(0.5)
    print('thank')

async def async_fuck():
    await asyncio.sleep(0.2)
    print('fuck!!!')

async def async_gather():
    print(f"[START] coroutine with asyncio.gather")
    asyncio.gather(
        async_hello(),
        async_thank(),
        async_fuck(),
    )
    print(f"[END] coroutine with asyncio.gather")

# asyncio.run()
def main_1():
    # asyncio.run()は同じスレッドで, 他の非同期イベントループが実行中は呼び出せない
    # loop_factoryがNone出ない場合, イベントループを作成するためにfactory関数が実行される.
    # それ以外は, asyncio.new_event_loop()が利用される.
    asyncio.run(main=async_hello(), 
                debug=None,
                #loop_factory=None, 
                ) # python3.12でloop_factoryが追加

# asyncio.Runner    
def main_2():
    # デフォルトは, asyncio.new_event_loop()でイベントループを設定
    # loop_factory=Noneの場合, asyncio.set_event_loop()で現在のイベントループがセットされる.
    with asyncio.Runner() as runner:
        runner.run(async_hello()) # return result or raise
        runner.run(async_thank())
        runner.run(async_fuck())

# signal.SIGINGを使うと, asyncio内部でプログラムがハングアップする可能性があるので
# 追加の対策が必要
def main_3():
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    # sigintとsigtermの両方に対応
    loop.add_signal_handler(signal.SIGINT, handler_gracefull_shutdown, signal.SIGINT)
    # loop.add_signal_handler(signal.SIGTERM, handler_gracefull_shutdown, signal.SIGTERM)
    loop.run_until_complete(async_gather())

if __name__ == "__main__":
    # main_1()
    # main_2()
    main_3()

