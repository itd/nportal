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
    backref,
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


class AccountRequests(Base):
    __tablename__ = 'account_requests'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)

    # unid - uniq id -  looks like: OjMvAN2RERnRP
    unid = Column(String, nullable=False, unique=True, primary_key=True)

    # to be assigned by approver
    UserID = Column(String, nullable=True, default=None)

    cn = Column(Text)
    titlePrefix = Column(Text)
    givenName = Column(String(64))
    middleName = Column(String(64), nullable=True)
    sn = Column(String(64))
    suffix = Column(String(32), nullable=True)

    street = Column(Text, nullable=True, default=None)
    lcity = Column(String(128))
    st = Column(String(400))
    postalCode = Column(String(64))
    country = Column(String(64))

    mail = Column(String(128))
    # mailPreferred = Column(String(128), nullable=True, default=None)
    phone = Column(String(32))
    cell = Column(String(32), nullable=True, default=None)

    employerType = Column(String(32), nullable=True, default=None)
    employerName = Column(String(192), nullable=True, default=None)

    citizenStatus = Column(String(10), nullable=True, default=None)

    citizenships = relationship("Citizenships",
                                back_populates="request")
    birthCountry = Column(Text)

    nrelUserID = Column(String(16), nullable=True, default=None)
    preferredUID = Column(String(16), nullable=True, default=None)

    justification = Column(Text, nullable=True, default=None)
    comments = Column(Text, nullable=True, default=None)

    subTimestamp = Column(DateTime, nullable=True, default=None)
    couTimestamp = Column(DateTime, nullable=True, default=None)
    storTimestamp = Column(DateTime, nullable=True, default=None)

    approvalTimestamp = Column(DateTime, nullable=True, default=None)
    approvalStatus = Column(Integer, nullable=True, default=None)
    approvedBy = Column(Text, nullable=True, default=None)

    def __repr__(self):
        return "<AccountRequests(id='%s', unid='%s', subTimeStamp='%s')>" % (
                self.id, self.unid, self.subTimestamp)


class Citizenships(Base):
    """
    A list of country codes
    """
    __tablename__ = 'citizenships'
    id = Column(Integer, primary_key=True)
    req_id = Column(Integer, ForeignKey('account_requests.id'))
    code = Column(String, nullable=False)
    name = Column(String)

    request = relationship("AccountRequests",
                           back_populates="citizenships")

    def __repr__(self):
        return "<Citizenships(req_id='%s', code='%s')>" % (self.req_id,
                                                           self.code)


# class RequestCitizenLink(Base):
#     __tablename__ = 'req_cit_link'
#     req_id = Column(Integer, ForeignKey('account_requests.id'), primary_key=True)
#     cit_id = Column(Integer, ForeignKey('citizenships.id'), primary_key=True)
#     extra_data = Column(String(256))
#     request = relationship(AccountRequests,
#                            backref=backref("request_ass"))
#     citizenships = relationship(Citizenships,
#                                 backref=backref("citizenship_ass"))
