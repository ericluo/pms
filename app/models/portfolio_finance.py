from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base

class PortfolioFinance(Base):
    __tablename__ = 'portfolio_finances'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True, unique=True)
    cash_balance = Column(Numeric(18, 2), nullable=False, default=0)
    total_asset = Column(Numeric(18, 2), nullable=False, default=0)
    liability = Column(Numeric(18, 2), nullable=False, default=0)
    net_asset = Column(Numeric(18, 2), nullable=False, default=0)
    cost_basis = Column(Numeric(18, 2), nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio = relationship('Portfolio', back_populates='finance')
    history = relationship('PortfolioFinanceHistory', back_populates='finance', cascade='all, delete-orphan')
    holding_changes = relationship('HoldingChange', back_populates='finance', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<PortfolioFinance(portfolio_id={self.portfolio_id}, net_asset={self.net_asset})>"

    def calculate_from_holdings(self, holdings: list, cash_balance: Decimal = None):
        total_asset = cash_balance if cash_balance is not None else self.cash_balance
        total_cost = Decimal('0')

        for holding in holdings:
            if holding.quantity > 0:
                asset_value = holding.quantity * holding.current_price
                total_asset += asset_value
                total_cost += holding.quantity * holding.cost_price

        self.total_asset = total_asset
        self.cost_basis = total_cost

        if total_asset < 0:
            self.liability = abs(total_asset)
            self.net_asset = Decimal('0')
        else:
            self.liability = Decimal('0')
            self.net_asset = total_asset

    def apply_cash_flow(self, amount: Decimal, cash_balance: Decimal):
        new_cash_balance = cash_balance + amount
        self.cash_balance = new_cash_balance

        if new_cash_balance < 0:
            self.liability = abs(new_cash_balance)
            self.net_asset = Decimal('0')
        else:
            self.liability = Decimal('0')


class PortfolioFinanceHistory(Base):
    __tablename__ = 'portfolio_finance_history'

    id = Column(Integer, primary_key=True, index=True)
    finance_id = Column(Integer, ForeignKey('portfolio_finances.id'), nullable=False, index=True)
    record_date = Column(DateTime, nullable=False, index=True)
    cash_balance = Column(Numeric(18, 2), nullable=False)
    total_asset = Column(Numeric(18, 2), nullable=False)
    liability = Column(Numeric(18, 2), nullable=False)
    net_asset = Column(Numeric(18, 2), nullable=False)
    cost_basis = Column(Numeric(18, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    finance = relationship('PortfolioFinance', back_populates='history')

    def __repr__(self):
        return f"<PortfolioFinanceHistory(finance_id={self.finance_id}, record_date={self.record_date}, net_asset={self.net_asset})>"


class HoldingChange(Base):
    __tablename__ = 'holding_changes'

    id = Column(Integer, primary_key=True, index=True)
    finance_id = Column(Integer, ForeignKey('portfolio_finances.id'), nullable=False, index=True)
    holding_id = Column(Integer, ForeignKey('holdings.id'), nullable=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False, index=True)
    asset_code = Column(String(20), nullable=False)
    asset_name = Column(String(100), nullable=False)
    change_type = Column(String(20), nullable=False)  # buy/sell/adjust/cash_dividend/etc.
    quantity_before = Column(Numeric(18, 4), nullable=False)
    quantity_after = Column(Numeric(18, 4), nullable=False)
    quantity_change = Column(Numeric(18, 4), nullable=True)  # 变动数量（正负值）
    price = Column(Numeric(18, 4), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=True, default='CNY')  # 交易币种
    exchange_rate = Column(Numeric(10, 6), nullable=True, default=1.0)  # 汇率
    fair_price = Column(Numeric(18, 4), nullable=True)  # 公允价格
    valuation_price = Column(Numeric(18, 4), nullable=True)  # 估值净价
    cost_price = Column(Numeric(18, 4), nullable=True)  # 成本价格（全价）
    weight = Column(Numeric(10, 6), nullable=True)  # 权重%
    dividend_date = Column(DateTime, nullable=True)  # 收息日期
    reason = Column(String(200), nullable=True)  # 变动原因
    total_asset_before = Column(Numeric(18, 2), nullable=False)
    total_asset_after = Column(Numeric(18, 2), nullable=False)
    net_asset_before = Column(Numeric(18, 2), nullable=False)
    net_asset_after = Column(Numeric(18, 2), nullable=False)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    finance = relationship('PortfolioFinance', back_populates='holding_changes')

    def __repr__(self):
        return f"<HoldingChange(id={self.id}, asset_code={self.asset_code}, change_type={self.change_type})>"


class HoldingSnapshot(Base):
    """每日持仓快照表 - 记录每个交易日的完整持仓"""
    __tablename__ = 'holding_snapshots'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    snapshot_date = Column(DateTime, nullable=False, index=True)  # 快照日期
    holdings_data = Column(String, nullable=False)  # JSON 格式的持仓数据
    total_market_value = Column(Numeric(18, 2), nullable=False)  # 总市值
    cash_balance = Column(Numeric(18, 2), nullable=True, default=0)  # 现金余额
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    portfolio = relationship('Portfolio', back_populates='holding_snapshots')

    def __repr__(self):
        return f"<HoldingSnapshot(portfolio_id={self.portfolio_id}, date={self.snapshot_date})>"
