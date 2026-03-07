from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False, index=True)
    transaction_type = Column(String(10), nullable=False)  # 买入/卖出
    quantity = Column(Numeric(18, 4), nullable=False)
    price = Column(Numeric(18, 4), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    fee = Column(Numeric(18, 2), default=0)
    transaction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 关系
    portfolio = relationship('Portfolio', back_populates='transactions')
    asset = relationship('Asset', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_type='{self.transaction_type}', asset_id={self.asset_id})>"