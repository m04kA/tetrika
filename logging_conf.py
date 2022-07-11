from loguru import logger
import os
from datetime import datetime
import shutil

today_date = datetime.today().date()
files = os.listdir()
if not "logs" in files:
    os.mkdir("logs")
os.chdir("logs")
files = os.listdir()
if len(files) > 4:
    for name in files:
        data = name[:10]
        date = datetime.strptime(data, "%Y-%m-%d").date()
        if (today_date - date).days > 10:
            dir = os.path.abspath(os.curdir) + f'\\{name}'
            shutil.rmtree(dir)
            logger.info(f"Delete folder: {name}")
            files = os.listdir()
            print(files)

logger.add(f'{today_date}/logs.log', level='DEBUG')
logger.add(f'errors/{today_date}.log', level='ERROR')
logger.remove(0)

logger.info("Start logging.")