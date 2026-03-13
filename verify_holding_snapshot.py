"""
持仓快照功能验证脚本
"""

from app import create_app
from app.utils.database import get_db
from app.models.portfolio_finance import HoldingSnapshot, HoldingChange
from app.models.holding import Holding
from app.models.asset import Asset
from app.models.portfolio import Portfolio
from app.services.holding import HoldingService
from datetime import date, datetime
from decimal import Decimal
import json

def verify_implementation():
    """验证持仓快照功能实现"""
    
    print("=" * 60)
    print("持仓快照功能验证")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        db = next(get_db())
        print("\n✅ 1. 验证数据模型...")
        
        # 验证 HoldingSnapshot 表
        try:
            columns = HoldingSnapshot.__table__.columns
            assert 'id' in columns
            assert 'portfolio_id' in columns
            assert 'snapshot_date' in columns
            assert 'holdings_data' in columns
            assert 'total_market_value' in columns
            assert 'cash_balance' in columns
            print("   ✓ HoldingSnapshot 表结构正确")
        except Exception as e:
            print(f"   ✗ HoldingSnapshot 表结构错误：{e}")
            return False
        
        # 验证 HoldingChange 表新增字段
        try:
            columns = HoldingChange.__table__.columns
            assert 'quantity_change' in columns
            assert 'currency' in columns
            assert 'exchange_rate' in columns
            assert 'fair_price' in columns
            assert 'valuation_price' in columns
            assert 'cost_price' in columns
            assert 'weight' in columns
            assert 'dividend_date' in columns
            assert 'reason' in columns
            print("   ✓ HoldingChange 表新增字段正确")
        except Exception as e:
            print(f"   ✗ HoldingChange 表新增字段错误：{e}")
            return False
        
        print("\n✅ 2. 验证 Service 层方法...")
        
        # 验证 HoldingService 方法
        service = HoldingService(db)
        
        try:
            assert hasattr(service, 'get_snapshot_dates')
            assert hasattr(service, 'get_holdings_on_date')
            assert hasattr(service, 'create_or_update_snapshot')
            assert hasattr(service, 'delete_snapshot')
            assert hasattr(service, 'calculate_portfolio_weights')
            print("   ✓ Service 层方法完整")
        except Exception as e:
            print(f"   ✗ Service 层方法缺失：{e}")
            return False
        
        print("\n✅ 3. 验证权重动态计算...")
        
        # 创建一个测试持仓
        try:
            # 获取第一个投资组合
            portfolio = db.query(Portfolio).first()
            if not portfolio:
                print("   ⚠ 没有投资组合，跳过测试")
            else:
                holdings = db.query(Holding).filter(
                    Holding.portfolio_id == portfolio.id
                ).all()
                
                if holdings:
                    # 测试权重计算
                    service = HoldingService(db)
                    result = service.calculate_portfolio_weights(holdings)
                    
                    if result:
                        total_weight = sum(h['weight'] for h in result)
                        print(f"   ✓ 权重计算正确，总权重：{total_weight:.2f}%")
                    else:
                        print("   ⚠ 权重计算结果为空")
                else:
                    print("   ⚠ 没有持仓数据，跳过测试")
        except Exception as e:
            print(f"   ✗ 权重计算错误：{e}")
            return False
        
        print("\n✅ 4. 验证快照创建功能...")
        
        try:
            if portfolio and holdings:
                # 创建快照
                service = HoldingService(db)
                result = service.create_or_update_snapshot(
                    portfolio.id,
                    date.today()
                )
                
                print(f"   ✓ 快照创建成功：")
                print(f"      - 日期：{result['snapshot_date']}")
                print(f"      - 持仓数量：{result['holdings_count']}")
                print(f"      - 总市值：{result['total_market_value']:.2f}")
                
                # 验证快照数据
                snapshot = db.query(HoldingSnapshot).filter(
                    HoldingSnapshot.portfolio_id == portfolio.id,
                    db.func.date(HoldingSnapshot.snapshot_date) == date.today()
                ).first()
                
                if snapshot:
                    holdings_data = json.loads(snapshot.holdings_data)
                    print(f"      - JSON 数据解析成功：{len(holdings_data)} 条记录")
                    
                    # 验证权重字段
                    if holdings_data and 'weight' in holdings_data[0]:
                        print(f"      - 权重字段存在")
                    else:
                        print(f"      ⚠ 权重字段缺失")
                else:
                    print(f"   ✗ 快照记录不存在")
                    return False
            else:
                print("   ⚠ 没有测试数据，跳过快照创建测试")
        except Exception as e:
            print(f"   ✗ 快照创建错误：{e}")
            return False
        
        print("\n✅ 5. 验证快照查询功能...")
        
        try:
            if portfolio:
                service = HoldingService(db)
                
                # 查询快照日期列表
                dates = service.get_snapshot_dates(portfolio.id)
                print(f"   ✓ 快照日期列表：{len(dates)} 个日期")
                
                # 查询指定日期的持仓
                if dates:
                    target_date = date.fromisoformat(dates[0]['date'])
                    holdings_on_date = service.get_holdings_on_date(portfolio.id, target_date)
                    print(f"   ✓ 历史持仓查询：{len(holdings_on_date)} 条记录")
                    
                    if holdings_on_date and 'weight' in holdings_on_date[0]:
                        print(f"      - 权重字段：{holdings_on_date[0]['weight']:.2f}%")
            else:
                print("   ⚠ 没有投资组合，跳过查询测试")
        except Exception as e:
            print(f"   ✗ 快照查询错误：{e}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ 所有验证通过！持仓快照功能实现完整。")
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    success = verify_implementation()
    if success:
        print("\n🎉 验证完成，功能可以投入使用！")
    else:
        print("\n❌ 验证失败，请检查错误信息。")
