from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    String,
    ForeignKeyConstraint,
    Boolean,
    Float,
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
                            ForeignKey('request.unid',
                                       ondelete='CASCADE'),
                            index=True),
                     Column('code', String,
                            ForeignKey('countrycodes.code',
                                       ondelete='CASCADE'),
                            index=True)
                     )


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)

    # unid - uniq id -  looks like: OjMvAN2RERnRP
    unid = Column(String, nullable=False, unique=True, primary_key=True)

    # to be assigned by approver
    UserID = Column(String, nullable=True, default=None)

    cn = Column(Text)           ## Kurt Bendl
    titlePrefix = Column(Text)    ## Dr.
    givenName = Column(String(64))  ## Kurt
    middleName = Column(String(64), nullable=True)  # M
    sn = Column(String(64))         ## Bendl
    suffix = Column(String(32), nullable=True)      ## III

    street = Column(Text, nullable=True, default=None)       ## 123 No Way
    lcity = Column(String(128))     ## Golden
    st = Column(String(400))    ## Colorado
    postalCode = Column(String(64))  ## 80401
    country = Column(String(64))     ## USA

    mail = Column(String(128))  ## kurt@tool.net
    mailPreferred = Column(String(128), nullable=True, default=None)
    phone = Column(String(32))  ## 777-777-7777
    cell = Column(String(32), nullable=True, default=None)  ## 666-666-6666

    employerType = Column(String(32), nullable=True, default=None)
    employerName = Column(String(128), nullable=True, default=None)

    citizenStatus = Column(String(10), nullable=True, default=None)

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

    # nrelExistingAccount = Column(Boolean)
    nrelUserID = Column(String(16), nullable=True, default=None) ## kbendl
    preferredUID = Column(String(16), nullable=True, default=None) ## kbendl

    justification = Column(Text, nullable=True, default=None)  ##
    comments = Column(Text, nullable=True, default=None)

    subTimestamp = Column(DateTime, nullable=True, default=None)

    couTimestamp = Column(DateTime, nullable=True, default=None)
    storTimestamp = Column(DateTime, nullable=True, default=None)

    approvalTimestamp = Column(DateTime, nullable=True, default=None)
    approvedBy = Column(Text, nullable=True, default=None)

    def __repr__(self):
        return "<Request(name='%s', fullname='%s', password='%s')>" % (
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
#     # user = relationship("Request", backref=backref('citizenships', order_by=id))
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

