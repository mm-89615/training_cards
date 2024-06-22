from sqlalchemy.ext.asyncio import AsyncSession

class BaseRequest:

    def __init__(self, session):
        self.session: AsyncSession = session
