import asyncio
import csv

import aiofiles

from database.engine import async_session
from database.repo.word import WordRequests

words_path = "..\\data\\words_small.csv"


async def insert_words_to_db(filepath, as_session: async_session):
    async with aiofiles.open(filepath, 'r') as file:
        reader = csv.reader(await file.readlines())
        for row in reader:
            async with as_session() as session:
                await WordRequests(session).add_word(row[0], row[1])


if __name__ == '__main__':
    asyncio.run(insert_words_to_db(filepath=words_path, as_session=async_session))
