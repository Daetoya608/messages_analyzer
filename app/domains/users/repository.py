from sqlalchemy.ext.asyncio import AsyncSession

from app.domains._base.repository import CRUDException, CRUDRepository
from app.domains.users.model import User


class UserRepository(CRUDRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User
