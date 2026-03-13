"""
数据库迁移脚本：持仓快照功能
- 增强 holding_changes 表
- 创建 holding_snapshots 表
"""

from sqlalchemy import create_engine, text
from app.config import config

def migrate_holding_snapshots():
    """持仓快照功能数据库迁移"""
    
    # 使用生产配置连接数据库
    DATABASE_URL = config['production'].SQLALCHEMY_DATABASE_URL
    engine = create_engine(DATABASE_URL)
    
    # SQL 脚本
    migration_sql = """
    -- 1. 增强 holding_changes 表（SQLite 不支持 IF NOT EXISTS，需要手动处理）
    ALTER TABLE holding_changes ADD COLUMN quantity_change DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN currency VARCHAR(10) DEFAULT 'CNY';
    ALTER TABLE holding_changes ADD COLUMN exchange_rate DECIMAL(10,6) DEFAULT 1.0;
    ALTER TABLE holding_changes ADD COLUMN fair_price DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN valuation_price DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN cost_price DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN weight DECIMAL(10,6);
    ALTER TABLE holding_changes ADD COLUMN dividend_date DATETIME;
    ALTER TABLE holding_changes ADD COLUMN reason VARCHAR(200);
    
    -- 2. 创建持仓快照表
    CREATE TABLE holding_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_id INTEGER NOT NULL,
        snapshot_date DATETIME NOT NULL,
        holdings_data TEXT NOT NULL,
        total_market_value DECIMAL(18, 2) NOT NULL,
        cash_balance DECIMAL(18, 2) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
    );
    
    -- 3. 创建索引
    CREATE INDEX idx_snapshots_portfolio_date ON holding_snapshots(portfolio_id, snapshot_date);
    CREATE INDEX idx_holding_changes_asset ON holding_changes(asset_id);
    """
    
    try:
        with engine.begin() as conn:
            # 执行迁移脚本（忽略已存在的错误）
            for statement in migration_sql.strip().split(';'):
                statement = statement.strip()
                if statement:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        # 忽略已存在的错误
                        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                            pass  # 表/索引已存在，跳过
                        else:
                            raise
        
        print("✅ 持仓快照功能数据库迁移成功！")
        print("\n完成内容：")
        print("1. 增强 holding_changes 表：")
        print("   - quantity_change: 变动数量")
        print("   - currency: 交易币种")
        print("   - exchange_rate: 汇率")
        print("   - fair_price: 公允价格")
        print("   - valuation_price: 估值净价")
        print("   - cost_price: 成本价格")
        print("   - weight: 权重")
        print("   - dividend_date: 收息日期")
        print("   - reason: 变动原因")
        print("\n2. 创建 holding_snapshots 表：")
        print("   - 存储持仓快照（JSON 格式）")
        print("   - 包含总市值和现金余额")
        print("   - 支持快速历史查询")
        print("\n3. 创建索引：")
        print("   - idx_snapshots_portfolio_date: 优化快照查询")
        print("   - idx_holding_changes_asset: 优化变动查询")
        
    except Exception as e:
        print(f"❌ 迁移失败：{e}")
        raise

if __name__ == "__main__":
    migrate_holding_snapshots()