from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.utils.database import Base

class MarketData(Base):
    __tablename__ = 'market_data'

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False, index=True)
    date = Column(Date, nullable=False)
    open = Column(Numeric(18, 4), nullable=False)
    high = Column(Numeric(18, 4), nullable=False)
    low = Column(Numeric(18, 4), nullable=False)
    close = Column(Numeric(18, 4), nullable=False)
    volume = Column(Numeric(20, 2), nullable=False)
    amount = Column(Numeric(20, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 关系
    asset = relationship('Asset', back_populates='market_data')

    # 唯一约束：每个资产每天只有一条数据
    __table_args__ = (
        UniqueConstraint('asset_id', 'date', name='_asset_date_uc'),
    )

    def __repr__(self):
        return f"<MarketData(id={self.id}, asset_id={self.asset_id}, date={self.date})>"