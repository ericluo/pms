from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

ASSET_TYPES = ['stock', 'fund', 'bond', 'cash']
ASSET_TYPE_NAMES = {
    'stock': '股票',
    'fund': '基金',
    'bond': '债券',
    'cash': '现金'
}

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    market = Column(String(50))
    industry = Column(String(50))
    interest_rate = Column(Numeric(10, 4))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    holdings = relationship('Holding', back_populates='asset')
    transactions = relationship('Transaction', back_populates='asset')
    market_data = relationship('MarketData', back_populates='asset', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Asset(id={self.id}, code='{self.code}', name='{self.name}', type='{self.type}')>"