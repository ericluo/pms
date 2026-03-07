"""
PMS 测试配置文件
用于配置 pytest 测试运行器
"""
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import Base, get_db

# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pms.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    # 先删除所有表，再重新创建（确保干净的测试环境）
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # 清理
        db.close()
        Base.metadata.drop_all(bind=engine)


# pytest 配置
def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# 设置测试环境变量
os.environ['TESTING'] = 'True'
os.environ['FLASK_ENV'] = 'testing'


@pytest.fixture
def test_user(db_session):
    """创建测试用户"""
    from app.models.user import User
    
    user = User(
        username='test_user',
        email='test@example.com'
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_asset(db_session):
    """创建测试资产"""
    from app.models.asset import Asset
    
    asset = Asset(
        code='000001',
        name='平安银行',
        type='stock',
        market='深圳证券交易所'
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)
    return asset


@pytest.fixture
def test_portfolio(db_session, test_user):
    """创建测试投资组合"""
    from app.models.portfolio import Portfolio
    
    portfolio = Portfolio(
        name='测试组合',
        user_id=test_user.id,
        initial_capital=100000.00
    )
    db_session.add(portfolio)
    db_session.commit()
    db_session.refresh(portfolio)
    return portfolio


@pytest.fixture
def auth_headers(client, db_session, test_user):
    """创建认证请求头"""
    from flask_jwt_extended import create_access_token
    
    access_token = create_access_token(identity=test_user.id)
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def client(db_session):
    """创建 Flask 测试客户端"""
    from app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test_pms.db'
    
    with app.test_client() as test_client:
        yield test_client
