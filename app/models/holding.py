from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Holding(Base):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False, index=True)
    quantity = Column(Numeric(18, 4), nullable=False)
    cost_price = Column(Numeric(18, 4), nullable=False)
    current_price = Column(Numeric(18, 4), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    portfolio = relationship('Portfolio', back_populates='holdings')
    asset = relationship('Asset', back_populates='holdings')

    def __repr__(self):
        return f"<Holding(id={self.id}, portfolio_id={self.portfolio_id}, asset_id={self.asset_id})>"