from sqlalchemy import select, and_, or_
from database.basedao import BaseDAO
from messages.models import Message
from database.connection import async_session_maker


class MessagesDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_history(cls, user_id_1: int, user_id_2: int):
        """
        Асинхронно находит и возвращает все сообщения между двумя пользователями.

        Аргументы:
            user_id_1: ID первого пользователя.
            user_id_2: ID второго пользователя.

        Возвращает:
            Список сообщений между двумя пользователями.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    and_(cls.model.from_user_id == user_id_1, cls.model.to_user_id == user_id_2),
                    and_(cls.model.from_user_id == user_id_2, cls.model.to_user_id == user_id_1)
                )
            ).order_by(cls.model.id)
            result = await session.execute(query)
            return result.scalars().all()