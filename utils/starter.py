import random
from utils.dogs import DogsHouse
from data import config
from utils.core import logger
import datetime
import pandas as pd
from utils.core.telegram import Accounts
import asyncio
import os


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    dogs = DogsHouse(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'
    try:
        await dogs.login()

        tasks = await dogs.get_tasks()
        for task in tasks:
            if task['complete'] or task['slug'] in config.BLACKLIST_TASK: continue
            if await dogs.verify_task(task['slug']):
                logger.success(f'Thread {thread} | {account} | Completed task «{task["slug"]}». Reward {task["reward"]}')
            else:
                logger.warning(f'Thread {thread} | {account} | Can\' complete task «{task["slug"]}»')
            await asyncio.sleep(random.uniform(*config.DELAYS['TASK']))

        balance, age = await dogs.login()
        logger.success(f'Thread {thread} | {account} | Account age: {age}; Balance: {balance}')
        await dogs.logout()
    except Exception as e:
        logger.error(f'Thread {thread} | {account} | Error: {e}')


async def stats():
    accounts = await Accounts().get_accounts()

    tasks = []
    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        tasks.append(asyncio.create_task(DogsHouse(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy).stats()))

    data = await asyncio.gather(*tasks)

    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['Phone number', 'Name', 'Balance', 'Leaderboard', 'Age', 'Streak', 'Referrals', 'Referral link', 'Connected wallet', 'Proxy (login:password@ip:port)']

    if not os.path.exists('statistics'): os.mkdir('statistics')
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')

    logger.success(f"Saved statistics to {path}")
