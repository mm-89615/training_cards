from sqlalchemy.ext.asyncio import AsyncSession


class BaseRequest:

    def __init__(self, session: AsyncSession):
        self.session = session
