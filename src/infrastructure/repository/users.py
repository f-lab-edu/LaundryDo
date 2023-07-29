from src.domain.repository import UserRepository
from src.domain import User
from .session import FakeSession

class MemoryUserRepository(UserRepository) :

    def __init__(self, session : FakeSession) :
        self.session = session

    def get(self, userid : str) -> User:
        return self.session.query(User).get(userid)

    def list(self) :
        return list(self.session.query(User).values())
    
    def add(self, user: User) :
        self.session.query(User)[user.userid] = user


class SqlAlchemyUserRepository(UserRepository) :

    def __init__(self, session) :
        self.session = session

    def get(self, userid : str) -> User:
        return self.session.query(User).filter_by(userid = userid).one()

    def list(self) :
        return self.session.query(User).all()
    
    def add(self, user: User) :
        self.session.add(user)