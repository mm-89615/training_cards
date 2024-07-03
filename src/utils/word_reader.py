import csv

import aiofiles

from database.engine import async_session
from database.repo.word import WordRequests

words_small_path = "data/words_small.csv"
words_big_path = "data/words.csv"


async def insert_words_to_db(filepath, as_session: async_session):
    async with aiofiles.open(filepath, "r") as file:
        reader = csv.reader(await file.readlines())
        for row in reader:
            async with as_session() as session:
                await WordRequests(session).add_word(row[0], row[1])


async def fill_db():
    while True:
        insert_words = input("Заполнить базу словами? (y/n): ")
        if insert_words == "y" or insert_words == "n":
            break
        else:
            print("Неверное значение")
    if insert_words == "y":
        while True:
            size_db = input(
                "Размер базы данных слов (big-5000слов, small-75слов): (b/s): "
            )
            if size_db == "b":
                await insert_words_to_db(words_big_path, async_session)
                break
            elif size_db == "s":
                await insert_words_to_db(words_small_path, async_session)
                break
            else:
                print("Неверное значение")

