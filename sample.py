from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    _personality = Column('personality', String(50))  # Use a private column for the personality attribute

    # Books relationship
    books = relationship("Book", backref="user")

    def __init__(self, name, personality=None):
        self.name = name
        self._personality = personality

    @hybrid_property
    def personality(self):
        if self._personality:
            # If _personality is set, use it as the personality value
            return self._personality
        else:
            # Otherwise, calculate personality based on the user's books
            book_titles = [book.title for book in self.books]
            personality_type = self.calculate_personality_from_books(book_titles)
            return personality_type

    @personality.setter
    def personality(self, value):
        # Set the personality directly if needed (for SQLAlchemy session)
        self._personality = value

    def calculate_personality_from_books(self, book_titles):
        # Implement your logic to calculate personality based on the books list
        # For example, you can return a simple combination of book titles as a personality type
        return '-'.join(sorted(book_titles))

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))

# Usage example
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Replace 'your_database_uri' with the URI for your actual database
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a user with an initial personality value
    user = User(name="John Doe", personality="Introvert")
    user.books = [Book(title="Book A"), Book(title="Book B"), Book(title="Book C")]

    # The personality property will use the initialized value
    print(user.personality)  # Output: "Introvert"

    # Add the user to the session and commit to the database
    session.add(user)
    session.commit()

    # Query the user and check their personality
    queried_user = session.query(User).filter_by(name="John Doe").first()
    print(queried_user.personality)  # Output: "Introvert"