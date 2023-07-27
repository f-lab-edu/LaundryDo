from src.domain.repository import UserRepository
from src.dbmodel import User


class MemoryUserRepository(UserRepository) :

    def __init__(self, users : dict = {}) :
        self._users = users

    def get(self, userid : str) -> User:
        return self._users.get(userid)

    def list(self) :
        return self._users.values()
    
    def add(self, user: User) :
        self._users[user.userid] = user


class SqlAlchemyUserRepository(UserRepository) :

    def __init__(self, session) :
        self.session = session

    def get(self, userid : str) -> User:
        return self.session.query(User).filter_by(userid = userid).one()

    def list(self) :
        return self.session.query(User).all()
    
    def add(self, user: User) :
        self.session.add(user)