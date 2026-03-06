from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # 股票/基金/债券等
    market = Column(String(50), nullable=False)  # A股/港股/美股等
    industry = Column(String(50))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    holdings = relationship('Holding', back_populates='asset')
    transactions = relationship('Transaction', back_populates='asset')
    market_data = relationship('MarketData', back_populates='asset', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Asset(id={self.id}, code='{self.code}', name='{self.name}')>"