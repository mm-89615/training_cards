import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from config import settings
from database.repo import Request

async_engine: AsyncEngine = create_async_engine(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def main():
    async with async_session() as session:
        pass

        # await Request(session).user_words.add_user_word(user_id=1, word_id=50, in_russian='слово', in_english='word')
        # result = await Request(session).words.get_four_random_words(123)
        # result = await Request(session).words.get_new_word_not_in_user_words(123)
        # result = await Request(session).user_words.get_new_word_from_user_words(123)
        # result = await Request(session).words.get_new_word_not_in_user_words(332637284)
        result = await Request(session).user_words.get_new_word_from_user_words(332637284)
        for r in result:
            print(r.repetition_counter, r.in_russian, r.in_english)
        # print(result.in_russian, result.in_english)

if __name__ == '__main__':
    asyncio.run(main())
