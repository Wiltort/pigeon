from database.basedao import BaseDAO
from users.models import User


class UsersDAO(BaseDAO):
    model = User