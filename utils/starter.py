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
        balance, age = await dogs.login()
        logger.success(f'Thread {thread} | {account} | Account age: {age}; Balance: {balance}')

        if await dogs.first_visit():
            if await dogs.set_first_visit():
                logger.success(f'Thread {thread} | {account} | Set first visit')
                await asyncio.sleep(random.uniform(*config.DELAYS['FIRST_VISIT']))

        current_day = await dogs.get_calendar()
        if current_day:
            day = current_day['ID']

            if current_day['IsChecked']:
                logger.info(f'Thread {thread} | {account} | Already checked day: {day}')
            else:
                if await dogs.check_calendar(day):
                    logger.success(f'Thread {thread} | {account} | Checked day: {day}')

            time_to_sleep = await dogs.timer() + random.uniform(*config.DELAYS['ADDITION_TIME'])
            logger.info(f"Thread {thread} | {account} | Sleep {round(time_to_sleep, 1)} seconds to next check")
            await asyncio.sleep(time_to_sleep)

    except Exception as e:
        logger.error(f'Thread {thread} | {account} | Error: {e}')

    finally:
        logger.info(f"Thread {thread} | {account} | End work.")
        await dogs.logout()

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
