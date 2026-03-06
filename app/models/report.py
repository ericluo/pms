from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # 月度报告/季度报告/年度报告/自定义报告
    title = Column(String(200), nullable=False)
    content = Column(Text)
    generated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 关系
    portfolio = relationship('Portfolio')

    def __repr__(self):
        return f"<Report(id={self.id}, title='{self.title}', portfolio_id={self.portfolio_id})>"