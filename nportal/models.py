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


user_citizen = Table('user_citizen', Base.metadata,
                     Column('id', Integer, nullable=False,
                            unique=True, primary_key=True),
                     Column('user_id', String,
                            ForeignKey('user_request.unid',
                                       ondelete='CASCADE'),
                            index=True),
                     Column('code', String,
                            ForeignKey('countrycodes.code',
                                       ondelete='CASCADE'),
                            index=True)
                     )


class UserRequest(Base):
    __tablename__ = 'user_request'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    ## unid - uniq id -  looks like: OjMvAN2RERnRP
    unid = Column(String, nullable=False, unique=True, primary_key=True)
    UserID = Column(String(16), nullable=True)  ## to be assigned by approver
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
    citizenships = relationship("CountryCodes",
                                backref='user',
                                lazy='dynamic',
                                secondary=user_citizen,
                                cascade="all, delete",
                                passive_deletes=True
                                )
                                #order_by="Citizenship.id",
                                #secondary=user_citizen,
    birthCountry = Column(Text)  ##

    # nrelExistingAccount = Column(Boolean)  ##
    nrelUserID = Column(String(16), nullable=True) ## kbendl
    preferredUID = Column(String(16), nullable=True) ## kbendl

    justification = Column(Text)  ##
    comments = Column(Text, nullable=True)  ##

    subTimestamp = Column(DateTime, nullable=True)
    couTimestamp = Column(DateTime, nullable=True)
    storTimestamp = Column(DateTime, nullable=True)
    cyberTimestamp = Column(DateTime, nullable=True)

    def __repr__(self):
        return "<UserRequest(name='%s', fullname='%s', password='%s')>" % (
                self.id, self.preferredUID, self.unid, self.subTimestamp)


# class Citizenship(Base):
#     """
#     List of citizenships for users
#     """
#     __tablename__ = 'citizenships'
#     id = Column(Integer, primary_key=True)
#     code = Column(String)
#
#     user_id = Column(Integer, ForeignKey('user.id'))
#     # user = relationship("UserRequest", backref=backref('citizenships', order_by=id))
#     # user_ref = Column(Integer, ForeignKey('user.id'),
#     #                  nullable=False,
#     #                  index=True)
#
#     def __repr__(self):
#         return "<CitizenList(code='%s', userid='%s)>" % (
#                 self.code, self.user_ref)


class CountryCodes(Base):
    """
    A list of country codes, including None
    """
    __tablename__ = 'countrycodes'
    code = Column(String, unique=True, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return "<CountryCodes(code='%s', name='%s')>" % (self.code, self.name)

