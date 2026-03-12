"""
测试环境初始化脚本
用于创建测试用户、资产、投资组合等测试数据
"""

from app import create_app
from app.utils.database import SessionLocal
from app.models.user import User
from app.models.asset import Asset
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from werkzeug.security import generate_password_hash

db = SessionLocal()

try:
    # 1. 创建测试用户
    print("=== 创建测试用户 ===")
    test_user = db.query(User).filter_by(username="testuser").first()
    if not test_user:
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("123456"),
            role="user"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✓ 创建测试用户：testuser (ID: {test_user.id})")
    else:
        print(f"✓ 测试用户已存在：testuser (ID: {test_user.id})")
    
    # 2. 创建测试资产
    print("\n=== 创建测试资产 ===")
    test_assets = [
        {"code": "000001", "name": "平安银行", "type": "股票", "market": "A 股"},
        {"code": "600036", "name": "招商银行", "type": "股票", "market": "A 股"},
        {"code": "000002", "name": "万科 A", "type": "股票", "market": "A 股"},
        {"code": "510300", "name": "沪深 300ETF", "type": "基金", "market": "A 股"},
    ]
    
    for asset_data in test_assets:
        asset = db.query(Asset).filter_by(code=asset_data["code"]).first()
        if not asset:
            asset = Asset(
                code=asset_data["code"],
                name=asset_data["name"],
                type=asset_data["type"],
                market=asset_data["market"]
            )
            db.add(asset)
            db.commit()
            print(f"✓ 创建资产：{asset_data['code']} - {asset_data['name']}")
        else:
            print(f"✓ 资产已存在：{asset_data['code']} - {asset_data['name']}")
    
    # 3. 创建测试投资组合
    print("\n=== 创建测试投资组合 ===")
    test_portfolio = db.query(Portfolio).filter_by(name="测试投资组合", user_id=test_user.id).first()
    if not test_portfolio:
        test_portfolio = Portfolio(
            user_id=test_user.id,
            name="测试投资组合",
            description="这是一个用于测试的投资组合",
            benchmark="沪深 300",
            risk_level="中风险",
            is_default=True
        )
        db.add(test_portfolio)
        db.commit()
        db.refresh(test_portfolio)
        print(f"✓ 创建测试投资组合：{test_portfolio.name} (ID: {test_portfolio.id})")
    else:
        print(f"✓ 测试投资组合已存在：{test_portfolio.name} (ID: {test_portfolio.id})")
    
    # 4. 创建测试持仓
    print("\n=== 创建测试持仓 ===")
    stock_asset = db.query(Asset).filter_by(code="000001").first()
    if stock_asset:
        existing_holding = db.query(Holding).filter_by(
            portfolio_id=test_portfolio.id,
            asset_id=stock_asset.id
        ).first()
        
        if not existing_holding:
            holding = Holding(
                portfolio_id=test_portfolio.id,
                asset_id=stock_asset.id,
                quantity=1000,
                cost_price=10.5,
                current_price=12.0
            )
            db.add(holding)
            db.commit()
            print(f"✓ 创建测试持仓：{stock_asset.name} (数量：1000, 成本价：10.5)")
        else:
            print(f"✓ 测试持仓已存在：{stock_asset.name}")
    
    print("\n=== 测试环境初始化完成 ===")
    print(f"\n测试账号信息：")
    print(f"  邮箱：test@example.com")
    print(f"  密码：123456")
    print(f"\n测试数据：")
    print(f"  - 用户：1 个")
    print(f"  - 资产：4 个")
    print(f"  - 投资组合：1 个")
    print(f"  - 持仓：1 个")
    
finally:
    db.close()
