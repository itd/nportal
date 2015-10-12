from sqlalchemy import (
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
    id = Column(Integer, primary_key=True)
    cn = Column(Text)           ## Kurt Bendl
    titlePrefix = Column(Text)    ## Dr.
    givenName = Column(String(64))  ## Kurt
    sn = Column(String(64))         ## Bendl
    middleName = Column(String(64))
    suffix = Column(String(32))      ## Sr.

    userTitle = Column(String(128)) ## Senior Systems Analyst
    street = Column(Text)       ## 123 No Way
    l = Column(String(128))     ## Golden
    st = Column(String(400))    ## Colorado
    postalCode = Column(String(64))   ## 80401
    country = Column(String(64))      ## USA

    mail = Column(String(128))   ## kbendl2@hpctest.nrel.gov|xx@nrel.gov|kurt@tool.net
    mailPreferred = Column(String(128))   ## kbendl2@hpctest.nrel.gov|xx@nrel.gov|kurt@tool.net
    phone = Column(String(32))   ## 777-777-7777
    cell = Column(String(32))   ## 666-666-6666
    phonePrimary = Column(String(32))   ## 666-666-6666

    employerType = Column(String(32))   ## [doe, gov, university, industry, non-us, other.
    employerName = Column(String(128))   ##
    employerAddress = Column(Text)   ##

    shipAddrSame = Column(Boolean)   ##
    shipAddr = Column(Text)   ##

    citizenStatus = Column(String(10))   ##
    citizenOf = Column(Text)   ##

    nrelExistingAccount = Column(Boolean)   ##
    nrelUserID = Column(String(16))  ## kbendl
    preferredUID = Column(String(16)) ## preferred userid: kbendl

    comments = Column(Text)   ##

    subTimestamp = Column(DateTime, nullable=False)
    couTimestamp = Column(DateTime, nullable=True)
    storTimestamp = Column(DateTime, nullable=True)
    cyberTimestamp = Column(DateTime, nullable=True)


citizen_types = [
    ("U.S. Citizen", "us"),
    ("U.S. Citizen with Multiple Citizenship", "us_multi"),
    ("Lawful Permanent Resident (LPR)", "lpr"),
    ("Other", "other")
    ]




default_ldap_fields = """
userPassword
userClass
mail
displayName
postalCode
krbLastSuccessfulAuth
ipaUniqueID
title
uid
street
krbPrincipalName
krbLoginFailedCount
sn
memberOf
krbTicketFlags
krbPasswordExpiration
loginShell
st
krbPrincipalKey
homeDirectory
initials
givenName
objectClass
cn
l
mepManagedEntry
krbLastFailedAuth
gecos
uidNumber
krbExtraData
gidNumber
krbLastPwdChange
"""

