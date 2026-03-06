from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class CashFlow(Base):
    __tablename__ = 'cash_flows'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    type = Column(String(20), nullable=False)  # 存入/取出/分红/利息等
    amount = Column(Numeric(18, 2), nullable=False)
    description = Column(Text)
    transaction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 关系
    portfolio = relationship('Portfolio', back_populates='cash_flows')

    def __repr__(self):
        return f"<CashFlow(id={self.id}, type='{self.type}', amount={self.amount})>"