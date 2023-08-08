from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, case

Base = declarative_base()


class Pet(Base) :
    __tablename__ = 'pet'
    id = Column(Integer, primary_key= True )
    firstname = Column( String(255))
    ownerid = Column('ownerid', Integer, ForeignKey('owner.id'))

    

class Owner(Base):
    __tablename__ = "owner"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    pet_list = relationship('Pet', backref = 'owner')

    @hybrid_property
    def petnum(cls) :
        return len(cls.pet_list)
    
    @petnum.expression
    def petnum(cls) :
        return func.length(cls.pet_list)

    @hybrid_property
    def fullname(self):
        if self.firstname is not None:
            return self.firstname + " " + self.lastname
        else:
            return self.lastname

    @fullname.expression
    def fullname(cls):
        return case(
            (cls.firstname != None, cls.firstname + " " + cls.lastname),
            else_=cls.lastname,
        )
    

    

if __name__ == '__main__' :

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    session = sessionmaker(bind = engine, autoflush = False, autocommit = False)()
    
    owner1 = Owner(id = 123, firstname = 'eunsung', lastname = 'shin')
    pet1 = Pet(id = 123, firstname = 'Naro', ownerid = 123)
    session.add(owner1)
    session.commit()

    print(session.execute(func.count(session.query(Owner).join(Owner.pet_list))))

    