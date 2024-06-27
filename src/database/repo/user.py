from typing import Optional

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRequest
from ..models import User


class UserRequests(BaseRequest):
    async def get_or_create_user(
            self,
            tg_id: int,
            username: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
    ):
        insert_stmt = (
            insert(User)
            .values(
                tg_id=tg_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            .on_conflict_do_update(
                index_elements=[User.tg_id],
                set_=dict(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    updated_at=func.now()
                )
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.one()
