# 投资组合管理系统 (PMS) 后端技术架构设计

## 1. 技术栈选择

### 1.1 核心技术
- **语言**：Python 3.9+
- **Web框架**：Flask 2.0+
- **数据库**：SQLite 3.35+
- **ORM**：SQLAlchemy 2.0+
- **认证**：Flask-JWT-Extended 4.6+
- **API文档**：Flask-RESTx 0.5+
- **数据验证**：Flask-Marshmallow 0.15+
- **CORS**：Flask-CORS 4.0+

### 1.2 辅助工具
- **环境管理**：Pipenv 2023+
- **代码规范**：Black 23.0+
- **类型检查**：Mypy 1.0+
- **测试框架**：Pytest 7.0+
- **日志管理**：Python标准日志模块
- **数据采集**：Requests 2.31+
- **HTML解析**：BeautifulSoup4 4.12+

## 2. 目录结构设计

```
├── app/                  # 应用主目录
│   ├── api/              # API路由
│   │   ├── auth.py       # 认证相关API
│   │   ├── portfolio.py  # 投资组合相关API
│   │   ├── asset.py      # 资产相关API
│   │   ├── holding.py    # 持仓相关API
│   │   ├── transaction.py # 交易记录相关API
│   │   ├── cash_flow.py  # 现金流水相关API
│   │   ├── performance.py # 业绩分析相关API
│   │   ├── market.py     # 市场数据相关API
│   │   ├── report.py     # 报告相关API
│   │   └── __init__.py   # API初始化
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── portfolio.py  # 投资组合模型
│   │   ├── asset.py      # 资产模型
│   │   ├── holding.py    # 持仓模型
│   │   ├── transaction.py # 交易记录模型
│   │   ├── cash_flow.py  # 现金流水模型
│   │   ├── market_data.py # 市场数据模型
│   │   └── __init__.py   # 模型初始化
│   ├── schemas/          # 数据验证和序列化
│   │   ├── user.py       # 用户相关schema
│   │   ├── portfolio.py  # 投资组合相关schema
│   │   ├── asset.py      # 资产相关schema
│   │   ├── holding.py    # 持仓相关schema
│   │   ├── transaction.py # 交易记录相关schema
│   │   ├── cash_flow.py  # 现金流水相关schema
│   │   ├── performance.py # 业绩分析相关schema
│   │   ├── market.py     # 市场数据相关schema
│   │   ├── report.py     # 报告相关schema
│   │   └── __init__.py   # schema初始化
│   ├── services/         # 业务逻辑
│   │   ├── auth.py       # 认证服务
│   │   ├── portfolio.py  # 投资组合服务
│   │   ├── asset.py      # 资产服务
│   │   ├── holding.py    # 持仓服务
│   │   ├── transaction.py # 交易记录服务
│   │   ├── cash_flow.py  # 现金流水服务
│   │   ├── performance.py # 业绩分析服务
│   │   ├── market.py     # 市场数据服务
│   │   ├── report.py     # 报告服务
│   │   └── __init__.py   # 服务初始化
│   ├── utils/            # 工具函数
│   │   ├── auth.py       # 认证工具
│   │   ├── database.py   # 数据库工具
│   │   ├── market.py     # 市场数据工具
│   │   ├── performance.py # 业绩计算工具
│   │   ├── report.py     # 报告生成工具
│   │   └── __init__.py   # 工具初始化
│   ├── config/           # 配置
│   │   ├── __init__.py   # 配置初始化
│   │   ├── development.py # 开发环境配置
│   │   ├── testing.py    # 测试环境配置
│   │   └── production.py # 生产环境配置
│   └── __init__.py       # 应用初始化
├── migrations/           # 数据库迁移
├── tests/                # 测试文件
│   ├── test_auth.py      # 认证测试
│   ├── test_portfolio.py # 投资组合测试
│   ├── test_asset.py     # 资产测试
│   ├── test_holding.py   # 持仓测试
│   ├── test_transaction.py # 交易记录测试
│   ├── test_cash_flow.py # 现金流水测试
│   ├── test_performance.py # 业绩分析测试
│   ├── test_market.py    # 市场数据测试
│   ├── test_report.py    # 报告测试
│   └── conftest.py       # 测试配置
├── app.py                # 应用入口
├── requirements.txt      # 依赖文件
├── Pipfile               # Pipenv配置文件
├── Pipfile.lock          # Pipenv锁文件
├── .env                  # 环境变量
├── .env.example          # 环境变量示例
├── .gitignore            # Git忽略文件
└── README.md             # 项目说明
```

## 3. 数据模型设计

### 3.1 用户模型 (User)

```python
# app/models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default='user')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    portfolios = relationship('Portfolio', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
```

### 3.2 投资组合模型 (Portfolio)

```python
# app/models/portfolio.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
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
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship('User', back_populates='portfolios')
    holdings = relationship('Holding', back_populates='portfolio', cascade='all, delete-orphan')
    transactions = relationship('Transaction', back_populates='portfolio', cascade='all, delete-orphan')
    cash_flows = relationship('CashFlow', back_populates='portfolio', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}', user_id={self.user_id})>"
```

### 3.3 资产模型 (Asset)

```python
# app/models/asset.py
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
```

### 3.4 持仓模型 (Holding)

```python
# app/models/holding.py
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
```

### 3.5 交易记录模型 (Transaction)

```python
# app/models/transaction.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False, index=True)
    type = Column(String(10), nullable=False)  # 买入/卖出
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
        return f"<Transaction(id={self.id}, type='{self.type}', asset_id={self.asset_id})>"
```

### 3.6 现金流水模型 (CashFlow)

```python
# app/models/cash_flow.py
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
```

### 3.7 市场数据模型 (MarketData)

```python
# app/models/market_data.py
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
```

## 4. API接口设计

### 4.1 认证接口

#### 4.1.1 登录
- **URL**：`POST /api/auth/login`
- **请求体**：
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **响应**：
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "user": {
      "id": 1,
      "username": "user1",
      "email": "user@example.com",
      "name": "User One",
      "role": "user"
    }
  }
  ```

#### 4.1.2 注册
- **URL**：`POST /api/auth/register`
- **请求体**：
  ```json
  {
    "username": "user1",
    "email": "user@example.com",
    "password": "password123",
    "name": "User One"
  }
  ```
- **响应**：
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "username": "user1",
      "email": "user@example.com",
      "name": "User One",
      "role": "user"
    }
  }
  ```

#### 4.1.3 获取当前用户信息
- **URL**：`GET /api/auth/me`
- **响应**：
  ```json
  {
    "id": 1,
    "username": "user1",
    "email": "user@example.com",
    "name": "User One",
    "role": "user"
  }
  ```

### 4.2 投资组合接口

#### 4.2.1 获取投资组合列表
- **URL**：`GET /api/portfolios`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "name": "我的投资组合",
      "description": "个人投资组合",
      "benchmark": "沪深300",
      "risk_level": "medium",
      "created_at": "2026-03-01T00:00:00Z",
      "updated_at": "2026-03-01T00:00:00Z"
    }
  ]
  ```

#### 4.2.2 获取单个投资组合详情
- **URL**：`GET /api/portfolios/{id}`
- **响应**：
  ```json
  {
    "id": 1,
    "name": "我的投资组合",
    "description": "个人投资组合",
    "benchmark": "沪深300",
    "risk_level": "medium",
    "created_at": "2026-03-01T00:00:00Z",
    "updated_at": "2026-03-01T00:00:00Z",
    "holdings": [
      {
        "id": 1,
        "asset_id": 1,
        "asset_code": "600519.SH",
        "asset_name": "贵州茅台",
        "quantity": 10,
        "cost_price": 1800.00,
        "current_price": 1850.00,
        "value": 18500.00,
        "profit": 500.00,
        "profit_percent": 2.78
      }
    ]
  }
  ```

#### 4.2.3 创建投资组合
- **URL**：`POST /api/portfolios`
- **请求体**：
  ```json
  {
    "name": "我的投资组合",
    "description": "个人投资组合",
    "benchmark": "沪深300",
    "risk_level": "medium"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "name": "我的投资组合",
    "description": "个人投资组合",
    "benchmark": "沪深300",
    "risk_level": "medium",
    "created_at": "2026-03-01T00:00:00Z",
    "updated_at": "2026-03-01T00:00:00Z"
  }
  ```

### 4.3 资产接口

#### 4.3.1 获取资产列表
- **URL**：`GET /api/assets`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "code": "600519.SH",
      "name": "贵州茅台",
      "type": "股票",
      "market": "A股",
      "industry": "白酒"
    }
  ]
  ```

#### 4.3.2 获取单个资产详情
- **URL**：`GET /api/assets/{id}`
- **响应**：
  ```json
  {
    "id": 1,
    "code": "600519.SH",
    "name": "贵州茅台",
    "type": "股票",
    "market": "A股",
    "industry": "白酒",
    "latest_price": 1850.00,
    "change": 50.00,
    "change_percent": 2.78
  }
  ```

### 4.4 持仓接口

#### 4.4.1 获取投资组合持仓
- **URL**：`GET /api/portfolios/{portfolioId}/holdings`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "asset_id": 1,
      "asset_code": "600519.SH",
      "asset_name": "贵州茅台",
      "quantity": 10,
      "cost_price": 1800.00,
      "current_price": 1850.00,
      "value": 18500.00,
      "cost": 18000.00,
      "profit": 500.00,
      "profit_percent": 2.78,
      "weight": 100.0
    }
  ]
  ```

#### 4.4.2 添加持仓
- **URL**：`POST /api/portfolios/{portfolioId}/holdings`
- **请求体**：
  ```json
  {
    "asset_id": 1,
    "quantity": 10,
    "cost_price": 1800.00,
    "current_price": 1850.00
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "asset_id": 1,
    "asset_code": "600519.SH",
    "asset_name": "贵州茅台",
    "quantity": 10,
    "cost_price": 1800.00,
    "current_price": 1850.00,
    "value": 18500.00,
    "cost": 18000.00,
    "profit": 500.00,
    "profit_percent": 2.78,
    "weight": 100.0
  }
  ```

### 4.5 交易记录接口

#### 4.5.1 获取交易记录
- **URL**：`GET /api/portfolios/{portfolioId}/transactions`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "asset_id": 1,
      "asset_code": "600519.SH",
      "asset_name": "贵州茅台",
      "type": "买入",
      "quantity": 10,
      "price": 1800.00,
      "amount": 18000.00,
      "fee": 18.00,
      "transaction_date": "2026-03-01T00:00:00Z"
    }
  ]
  ```

#### 4.5.2 添加交易记录
- **URL**：`POST /api/portfolios/{portfolioId}/transactions`
- **请求体**：
  ```json
  {
    "asset_id": 1,
    "type": "买入",
    "quantity": 10,
    "price": 1800.00,
    "amount": 18000.00,
    "fee": 18.00,
    "transaction_date": "2026-03-01T00:00:00Z"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "asset_id": 1,
    "asset_code": "600519.SH",
    "asset_name": "贵州茅台",
    "type": "买入",
    "quantity": 10,
    "price": 1800.00,
    "amount": 18000.00,
    "fee": 18.00,
    "transaction_date": "2026-03-01T00:00:00Z"
  }
  ```

### 4.6 现金流水接口

#### 4.6.1 获取现金流水
- **URL**：`GET /api/portfolios/{portfolioId}/cash-flows`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "type": "存入",
      "amount": 100000.00,
      "description": "初始投资",
      "transaction_date": "2026-03-01T00:00:00Z"
    }
  ]
  ```

#### 4.6.2 添加现金流水
- **URL**：`POST /api/portfolios/{portfolioId}/cash-flows`
- **请求体**：
  ```json
  {
    "type": "存入",
    "amount": 100000.00,
    "description": "初始投资",
    "transaction_date": "2026-03-01T00:00:00Z"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "type": "存入",
    "amount": 100000.00,
    "description": "初始投资",
    "transaction_date": "2026-03-01T00:00:00Z"
  }
  ```

### 4.7 业绩分析接口

#### 4.7.1 获取业绩分析
- **URL**：`GET /api/portfolios/{portfolioId}/performance`
- **响应**：
  ```json
  {
    "total_return": 2.78,
    "annualized_return": 15.47,
    "daily_return": 0.09,
    "weekly_return": 0.63,
    "monthly_return": 2.78,
    "yearly_return": 15.47,
    "sharpe_ratio": 0.85,
    "max_drawdown": 5.23,
    "alpha": 2.15,
    "beta": 0.85,
    "volatility": 18.50
  }
  ```

### 4.8 市场数据接口

#### 4.8.1 获取股票市场数据
- **URL**：`GET /api/market/stocks`
- **响应**：
  ```json
  [
    {
      "code": "600519.SH",
      "name": "贵州茅台",
      "price": 1850.00,
      "change": 50.00,
      "change_percent": 2.78,
      "open": 1800.00,
      "high": 1860.00,
      "low": 1790.00,
      "volume": 1000000,
      "amount": 1850000000
    }
  ]
  ```

#### 4.8.2 获取市场指数数据
- **URL**：`GET /api/market/indices`
- **响应**：
  ```json
  [
    {
      "code": "000300.SH",
      "name": "沪深300",
      "price": 4500.00,
      "change": 90.00,
      "change_percent": 2.04,
      "open": 4410.00,
      "high": 4510.00,
      "low": 4400.00,
      "volume": 1000000000,
      "amount": 450000000000
    }
  ]
  ```

### 4.9 报告接口

#### 4.9.1 获取报告列表
- **URL**：`GET /api/reports`
- **响应**：
  ```json
  [
    {
      "id": 1,
      "portfolio_id": 1,
      "portfolio_name": "我的投资组合",
      "type": "月度报告",
      "title": "2026年3月月度报告",
      "generated_at": "2026-04-01T00:00:00Z"
    }
  ]
  ```

#### 4.9.2 创建报告
- **URL**：`POST /api/reports`
- **请求体**：
  ```json
  {
    "portfolio_id": 1,
    "type": "月度报告",
    "title": "2026年3月月度报告"
  }
  ```
- **响应**：
  ```json
  {
    "id": 1,
    "portfolio_id": 1,
    "portfolio_name": "我的投资组合",
    "type": "月度报告",
    "title": "2026年3月月度报告",
    "generated_at": "2026-04-01T00:00:00Z",
    "url": "/api/reports/1/export"
  }
  ```

## 5. 业务逻辑实现

### 5.1 认证服务

```python
# app/services/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "your-secret-key", algorithm="HS256")
        return encoded_jwt
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def create_user(self, user_create: UserCreate) -> User:
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=self.get_password_hash(user_create.password),
            name=user_create.name
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
```

### 5.2 投资组合服务

```python
# app/services/portfolio.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate

class PortfolioService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_portfolios(self, user_id: int) -> List[Portfolio]:
        return self.db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    
    def get_portfolio(self, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        return self.db.query(Portfolio).filter(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == user_id
        ).first()
    
    def create_portfolio(self, portfolio_create: PortfolioCreate, user_id: int) -> Portfolio:
        db_portfolio = Portfolio(
            user_id=user_id,
            name=portfolio_create.name,
            description=portfolio_create.description,
            benchmark=portfolio_create.benchmark,
            risk_level=portfolio_create.risk_level
        )
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def update_portfolio(self, portfolio_id: int, portfolio_update: PortfolioUpdate, user_id: int) -> Optional[Portfolio]:
        db_portfolio = self.get_portfolio(portfolio_id, user_id)
        if not db_portfolio:
            return None
        for key, value in portfolio_update.dict(exclude_unset=True).items():
            setattr(db_portfolio, key, value)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        db_portfolio = self.get_portfolio(portfolio_id, user_id)
        if not db_portfolio:
            return False
        self.db.delete(db_portfolio)
        self.db.commit()
        return True
    
    def get_portfolio_holdings(self, portfolio_id: int, user_id: int) -> List[Holding]:
        portfolio = self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            return []
        return portfolio.holdings
```

### 5.3 持仓服务

```python
# app/services/holding.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.holding import Holding
from app.models.asset import Asset
from app.schemas.holding import HoldingCreate, HoldingUpdate

class HoldingService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_holdings(self, portfolio_id: int) -> List[Holding]:
        return self.db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
    
    def get_holding(self, holding_id: int, portfolio_id: int) -> Optional[Holding]:
        return self.db.query(Holding).filter(
            Holding.id == holding_id,
            Holding.portfolio_id == portfolio_id
        ).first()
    
    def create_holding(self, holding_create: HoldingCreate, portfolio_id: int) -> Holding:
        db_holding = Holding(
            portfolio_id=portfolio_id,
            asset_id=holding_create.asset_id,
            quantity=holding_create.quantity,
            cost_price=holding_create.cost_price,
            current_price=holding_create.current_price
        )
        self.db.add(db_holding)
        self.db.commit()
        self.db.refresh(db_holding)
        return db_holding
    
    def update_holding(self, holding_id: int, holding_update: HoldingUpdate, portfolio_id: int) -> Optional[Holding]:
        db_holding = self.get_holding(holding_id, portfolio_id)
        if not db_holding:
            return None
        for key, value in holding_update.dict(exclude_unset=True).items():
            setattr(db_holding, key, value)
        self.db.commit()
        self.db.refresh(db_holding)
        return db_holding
    
    def delete_holding(self, holding_id: int, portfolio_id: int) -> bool:
        db_holding = self.get_holding(holding_id, portfolio_id)
        if not db_holding:
            return False
        self.db.delete(db_holding)
        self.db.commit()
        return True
    
    def calculate_holding_metrics(self, holding: Holding) -> dict:
        value = holding.quantity * holding.current_price
        cost = holding.quantity * holding.cost_price
        profit = value - cost
        profit_percent = (profit / cost) * 100 if cost > 0 else 0
        return {
            "value": value,
            "cost": cost,
            "profit": profit,
            "profit_percent": profit_percent
        }
    
    def calculate_portfolio_weights(self, holdings: List[Holding]) -> List[dict]:
        total_value = sum(holding.quantity * holding.current_price for holding in holdings)
        result = []
        for holding in holdings:
            asset = self.db.query(Asset).filter(Asset.id == holding.asset_id).first()
            metrics = self.calculate_holding_metrics(holding)
            weight = (metrics["value"] / total_value) * 100 if total_value > 0 else 0
            result.append({
                "id": holding.id,
                "asset_id": holding.asset_id,
                "asset_code": asset.code if asset else "",
                "asset_name": asset.name if asset else "",
                "quantity": holding.quantity,
                "cost_price": holding.cost_price,
                "current_price": holding.current_price,
                "value": metrics["value"],
                "cost": metrics["cost"],
                "profit": metrics["profit"],
                "profit_percent": metrics["profit_percent"],
                "weight": weight
            })
        return result
```

### 5.4 业绩分析服务

```python
# app/services/performance.py
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.models.transaction import Transaction
from app.models.cash_flow import CashFlow

class PerformanceService:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_total_return(self, portfolio_id: int) -> float:
        # 计算总回报率
        holdings = self.db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
        total_value = sum(holding.quantity * holding.current_price for holding in holdings)
        total_cost = sum(holding.quantity * holding.cost_price for holding in holdings)
        return ((total_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0
    
    def calculate_annualized_return(self, portfolio_id: int) -> float:
        # 计算年化收益率
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            return 0
        
        total_return = self.calculate_total_return(portfolio_id)
        days = (datetime.utcnow() - portfolio.created_at).days
        if days == 0:
            return 0
        
        # 简单年化计算
        return (pow(1 + total_return / 100, 365 / days) - 1) * 100
    
    def calculate_sharpe_ratio(self, portfolio_id: int) -> float:
        # 计算夏普比率
        # 这里使用简化计算，实际应该使用历史数据计算
        annualized_return = self.calculate_annualized_return(portfolio_id)
        risk_free_rate = 3.0  # 假设无风险利率为3%
        volatility = 15.0  # 假设波动率为15%
        return (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    def calculate_max_drawdown(self, portfolio_id: int) -> float:
        # 计算最大回撤
        # 这里使用简化计算，实际应该使用历史数据计算
        return 5.23  # 示例值
    
    def calculate_alpha_beta(self, portfolio_id: int) -> Dict[str, float]:
        # 计算Alpha和Beta
        # 这里使用简化计算，实际应该使用历史数据计算
        return {
            "alpha": 2.15,
            "beta": 0.85
        }
    
    def get_performance_metrics(self, portfolio_id: int) -> Dict[str, float]:
        total_return = self.calculate_total_return(portfolio_id)
        annualized_return = self.calculate_annualized_return(portfolio_id)
        sharpe_ratio = self.calculate_sharpe_ratio(portfolio_id)
        max_drawdown = self.calculate_max_drawdown(portfolio_id)
        alpha_beta = self.calculate_alpha_beta(portfolio_id)
        
        return {
            "total_return": round(total_return, 2),
            "annualized_return": round(annualized_return, 2),
            "daily_return": round(total_return / 30, 2),  # 简化计算
            "weekly_return": round(total_return / 4.3, 2),  # 简化计算
            "monthly_return": round(total_return, 2),
            "yearly_return": round(annualized_return, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown, 2),
            "alpha": round(alpha_beta["alpha"], 2),
            "beta": round(alpha_beta["beta"], 2),
            "volatility": 18.50  # 示例值
        }
```

### 5.5 市场数据服务

```python
# app/services/market.py
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.models.market_data import MarketData

class MarketDataService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_stock_data(self, code: str) -> Dict[str, float]:
        # 这里使用模拟数据，实际应该从API获取
        # 例如使用新浪财经、东方财富等API
        return {
            "price": 1850.00,
            "change": 50.00,
            "change_percent": 2.78,
            "open": 1800.00,
            "high": 1860.00,
            "low": 1790.00,
            "volume": 1000000,
            "amount": 1850000000
        }
    
    def get_index_data(self, code: str) -> Dict[str, float]:
        # 这里使用模拟数据，实际应该从API获取
        return {
            "price": 4500.00,
            "change": 90.00,
            "change_percent": 2.04,
            "open": 4410.00,
            "high": 4510.00,
            "low": 4400.00,
            "volume": 1000000000,
            "amount": 450000000000
        }
    
    def get_stocks_market_data(self) -> List[Dict]:
        # 获取股票市场数据
        assets = self.db.query(Asset).filter(Asset.type == "股票").limit(10).all()
        result = []
        for asset in assets:
            data = self.get_stock_data(asset.code)
            result.append({
                "code": asset.code,
                "name": asset.name,
                "price": data["price"],
                "change": data["change"],
                "change_percent": data["change_percent"],
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "volume": data["volume"],
                "amount": data["amount"]
            })
        return result
    
    def get_indices_market_data(self) -> List[Dict]:
        # 获取市场指数数据
        indices = [
            {"code": "000300.SH", "name": "沪深300"},
            {"code": "000001.SH", "name": "上证指数"},
            {"code": "399001.SZ", "name": "深证成指"},
            {"code": "399006.SZ", "name": "创业板指"}
        ]
        result = []
        for index in indices:
            data = self.get_index_data(index["code"])
            result.append({
                "code": index["code"],
                "name": index["name"],
                "price": data["price"],
                "change": data["change"],
                "change_percent": data["change_percent"],
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "volume": data["volume"],
                "amount": data["amount"]
            })
        return result
    
    def update_market_data(self, asset_id: int) -> bool:
        # 更新资产的市场数据
        asset = self.db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            return False
        
        try:
            data = self.get_stock_data(asset.code)
            # 更新持仓的当前价格
            holdings = self.db.query(Holding).filter(Holding.asset_id == asset_id).all()
            for holding in holdings:
                holding.current_price = data["price"]
            
            # 保存市场数据历史
            market_data = MarketData(
                asset_id=asset_id,
                date=datetime.utcnow().date(),
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["price"],
                volume=data["volume"],
                amount=data["amount"]
            )
            self.db.add(market_data)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
```

## 6. 数据库配置

### 6.1 数据库连接

```python
# app/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./pms.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite特定配置
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 6.2 数据库迁移

```python
# app.py
from app.utils.database import engine, Base
from app.models import user, portfolio, asset, holding, transaction, cash_flow, market_data

# 创建数据库表
Base.metadata.create_all(bind=engine)
```

## 7. 应用配置

### 7.1 配置文件

```python
# app/config/__init__.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时
    SQLALCHEMY_DATABASE_URL = "sqlite:///./pms.db"
    CORS_ORIGINS = ["*"]

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
```

### 7.2 应用初始化

```python
# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.config import config
from app.utils.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    CORS(app, origins=app.config["CORS_ORIGINS"])
    JWTManager(app)
    
    # 初始化API
    api = Api(
        app,
        version="1.0",
        title="投资组合管理系统 API",
        description="投资组合管理系统的RESTful API",
        prefix="/api"
    )
    
    # 注册API路由
    from app.api import auth, portfolio, asset, holding, transaction, cash_flow, performance, market, report
    api.add_namespace(auth.api, path="/auth")
    api.add_namespace(portfolio.api, path="/portfolios")
    api.add_namespace(asset.api, path="/assets")
    api.add_namespace(holding.api, path="/portfolios/<int:portfolio_id>/holdings")
    api.add_namespace(transaction.api, path="/portfolios/<int:portfolio_id>/transactions")
    api.add_namespace(cash_flow.api, path="/portfolios/<int:portfolio_id>/cash-flows")
    api.add_namespace(performance.api, path="/portfolios/<int:portfolio_id>/performance")
    api.add_namespace(market.api, path="/market")
    api.add_namespace(report.api, path="/reports")
    
    return app
```

## 8. 安全性设计

### 8.1 认证与授权
- **JWT认证**：使用JWT进行无状态认证
- **密码加密**：使用bcrypt加密存储密码
- **权限控制**：基于角色的访问控制
- **API保护**：使用装饰器保护需要认证的API

### 8.2 数据安全
- **输入验证**：使用Flask-Marshmallow进行数据验证
- **SQL注入防护**：使用SQLAlchemy ORM防止SQL注入
- **XSS防护**：设置适当的HTTP头
- **CSRF防护**：使用CSRF token

### 8.3 安全配置
- **HTTPS**：在生产环境中使用HTTPS
- **环境变量**：敏感配置使用环境变量
- **日志记录**：记录关键操作日志
- **定期备份**：定期备份数据库

## 9. 部署策略

### 9.1 开发环境
- **本地开发**：使用Flask开发服务器
- **调试模式**：开启调试模式
- **热重载**：支持代码热重载

### 9.2 测试环境
- **CI/CD**：配置持续集成和持续部署
- **自动化测试**：运行自动化测试
- **环境隔离**：使用独立的测试数据库

### 9.3 生产环境
- **WSGI服务器**：使用Gunicorn或uWSGI
- **反向代理**：使用Nginx作为反向代理
- **容器化**：使用Docker容器化部署
- **监控**：配置系统监控和告警
- **日志管理**：集中化日志管理

## 10. 性能优化

### 10.1 数据库优化
- **索引**：为频繁查询的字段添加索引
- **查询优化**：优化SQL查询，减少不必要的查询
- **批量操作**：使用批量操作减少数据库交互
- **缓存**：使用Redis缓存热点数据

### 10.2 API优化
- **分页**：对大数据量的API使用分页
- **压缩**：启用HTTP压缩
- **缓存**：缓存API响应
- **异步处理**：对耗时操作使用异步处理

### 10.3 代码优化
- **模块化**：模块化设计，提高代码复用性
- **异步IO**：使用异步IO处理并发请求
- **内存管理**：优化内存使用
- **代码审查**：定期进行代码审查

## 11. 测试策略

### 11.1 单元测试
- **模型测试**：测试数据模型的创建、更新、删除
- **服务测试**：测试业务逻辑的正确性
- **API测试**：测试API接口的响应
- **工具函数测试**：测试工具函数的功能

### 11.2 集成测试
- **数据库集成测试**：测试数据库操作的正确性
- **API集成测试**：测试API与数据库的交互
- **业务流程测试**：测试完整的业务流程

### 11.3 端到端测试
- **用户场景测试**：模拟用户操作场景
- **性能测试**：测试系统性能
- **安全测试**：测试系统安全性

## 12. 结论

本后端技术架构设计文档详细描述了投资组合管理系统的后端技术选型、目录结构、数据模型、API接口、业务逻辑实现、数据库配置、应用配置、安全性设计、部署策略、性能优化和测试策略。

该架构采用Python + Flask + SQLite技术栈，结合SQLAlchemy ORM和Flask-JWT-Extended，构建一个功能完备、安全可靠的投资组合管理系统后端。通过模块化设计和分层架构，确保系统的可扩展性和可维护性。

该架构设计将作为后端开发的指导文件，确保开发团队按照统一的标准进行开发，提高开发效率和代码质量。