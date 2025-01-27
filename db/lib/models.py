# coding: utf-8
from sqlalchemy import ARRAY, CHAR, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, UniqueConstraint, text, Table
from sqlalchemy.sql.sqltypes import BigInteger
from sqlalchemy.types import Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()
metadata = Base.metadata


class Constant(Base):
    __tablename__ = 'constant'

    const_id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v1()"))
    value = Column(Numeric)
    precision = Column(Integer)
    time_added = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class NamedConstant(Base):
    __tablename__ = 'named_constant'

    const_id = Column(ForeignKey('constant.const_id'), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    artificial = Column(Integer, nullable=False, server_default=text("0"))
    
    base = relationship('Constant', lazy='subquery')


class PcfConvergence(Enum):
    ZERO_DENOM = 0 # now considered an illegal PCF
    NO_FR = 1 # now considered an illegal PCF
    INDETERMINATE_FR = 2
    FR = 3
    RATIONAL = 4


class PcfCanonicalConstant(Base):
    __tablename__ = 'pcf_canonical_constant'
    __table_args__ = (
        UniqueConstraint('P', 'Q'),
    )

    const_id = Column(ForeignKey('constant.const_id'), primary_key=True)
    P = Column(ARRAY(Numeric()), nullable=False)
    Q = Column(ARRAY(Numeric()), nullable=False)
    last_matrix = Column(Text())
    depth = Column(Integer)
    convergence = Column(Integer)
    
    base = relationship('Constant', lazy='subquery')


class ScanHistory(Base):
    __tablename__ = 'scan_history'

    const_id = Column(ForeignKey('constant.const_id'), primary_key=True)
    algorithm = Column(String, nullable=False)
    time_scanned = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    details = Column(String)
    
    base = relationship('Constant')


constant_in_relation_table = Table(
    "constant_in_relation",
    Base.metadata,
    Column('const_id', ForeignKey('constant.const_id'), primary_key=True),
    Column('relation_id', ForeignKey('relation.relation_id'), primary_key=True),
)


class Relation(Base):
    __tablename__ = 'relation'

    relation_id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v1()"))
    relation_type = Column(String, nullable=False)
    # if this needs an order on the constants and cfs (and it probably will),
    # it is determined by ascending order on the const_ids
    details = Column(ARRAY(Integer()), nullable=False)
    precision = Column(Integer)
    time_added = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    constants = relationship('Constant', secondary=constant_in_relation_table)


class RelationAudit(Base):
    __tablename__ = 'relation_audit'

    relation_id = Column(ForeignKey('relation.relation_id'), primary_key=True)
    operation = Column(CHAR(1), nullable=False)
    stamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    userid = Column(Text(), nullable=False)
