from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    benchmark = Column(String(50), nullable=False)
    risk_level = Column(String(20), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship('User', back_populates='portfolios')
    holdings = relationship('Holding', back_populates='portfolio', cascade='all, delete-orphan')
    transactions = relationship('Transaction', back_populates='portfolio', cascade='all, delete-orphan')
    cash_flows = relationship('CashFlow', back_populates='portfolio', cascade='all, delete-orphan')
    finance = relationship('PortfolioFinance', back_populates='portfolio', uselist=False, cascade='all, delete-orphan')
    holding_snapshots = relationship('HoldingSnapshot', back_populates='portfolio', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}', user_id={self.user_id}, is_default={self.is_default})>"