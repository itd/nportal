from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean,
    Float,  ForeignKey, ForeignKeyConstraint, String,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class SiteModel(Base):
    __tablename__ = 'siteinfo'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('home_index', SiteModel.name, unique=True, mysql_length=255)


class UserAccountModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    unid = Column(Text, nullable=False, unique=True, primary_key=True)  ## OjMvAN2RERnRP
    cn = Column(Text)           ## Kurt Bendl
    titlePrefix = Column(Text)    ## Dr.
    givenName = Column(String(64))  ## Kurt
    middleName = Column(String(64), nullable=True)  # M
    sn = Column(String(64))         ## Bendl
    suffix = Column(String(32), nullable=True)      ## III

    street = Column(Text)       ## 123 No Way
    lcity = Column(String(128))     ## Golden
    st = Column(String(400))    ## Colorado
    postalCode = Column(String(64))  ## 80401
    country = Column(String(64))     ## USA

    mail = Column(String(128))  ## xx@nrel.gov
    mailPreferred = Column(String(128), nullable=True)  ## kurt@tool.net
    phone = Column(String(32))  ## 777-777-7777
    cell = Column(String(32), nullable=True)  ## 666-666-6666

    employerType = Column(String(32))  ##
    employerName = Column(String(128))  ##

    citizenStatus = Column(String(10)) ##
    #citizenOf = Column(Text)  ##
    citizenOf = relationship("CitizenOf",
                         backref='user'
                         )
    #
    #                      lazy='dynamic',
    #                      cascade="all, delete",
    #                      passive_deletes=True,
                         # secondary=user_citizen,
    birthCountry = Column(Text)  ##

    nrelExistingAccount = Column(Boolean)  ##
    nrelUserID = Column(String(16)) ## kbendl
    preferredUID = Column(String(16)) ## kbendl

    justification = Column(Text)  ##
    comments = Column(Text, nullable=True)  ##

    subTimestamp = Column(DateTime, nullable=True)
    couTimestamp = Column(DateTime, nullable=True)
    storTimestamp = Column(DateTime, nullable=True)
    cyberTimestamp = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                self.id, self.preferredUID, self.unid, self.subTimestamp)


# user_citizen = Table('user_citizen', Base.metadata,
#                      Column('user_id', Integer,
#                             ForeignKey('user.id',ondelete='CASCADE'),
#                             primary_key=True),
#                      Column('country', String)
#                      )


class CitizenOf(Base):
    """
    List of citizenships for a user
    """
    __tablename__ = 'citizenof'
    id = Column(Integer, primary_key=True)
    countrycode = Column(String)
    user = relationship("UserAccountModel", backref='bt_ids', order_by=id))

    # user_id = Column(Integer, ForeignKey('user.id'),
    #                  nullable=False,
    #                  index=True)


    def __repr__(self):
        return "<CitizenOf(name='%s', fullname='%s', password='%s')>" % (
                self.id, self.countrycode, self.user_id)
