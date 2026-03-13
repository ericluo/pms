"""
投资组合管理系统 (PMS)

一个现代化的投资组合管理系统，为个人和机构投资者提供全面的投资管理工具。
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
import logging
from app.config import config
from app.utils.database import engine, Base

# 导入所有模型，确保它们被注册到 Base.metadata
from app.models import user, portfolio, asset, holding, transaction, cash_flow, market_data, report, portfolio_finance

# 创建数据库表
Base.metadata.create_all(bind=engine)


def create_app(config_name: str = None) -> Flask:
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称 (development/production/testing)
        
    Returns:
        Flask 应用实例
    """
    if config_name is None:
        config_name = "default"
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 配置日志
    _setup_logging(app)
    
    # 初始化扩展
    _init_extensions(app)
    
    # 注册 API 路由
    _register_api(app)
    
    app.logger.info(f"应用启动成功，环境：{config_name}")
    
    return app


def _setup_logging(app: Flask) -> None:
    """配置应用日志"""
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def _init_extensions(app: Flask) -> None:
    """初始化 Flask 扩展"""
    # 配置 CORS
    CORS(app, origins=app.config.get("CORS_ORIGINS", ["*"]))
    
    # 配置 JWT
    JWTManager(app)


def _register_api(app: Flask) -> None:
    """注册 API 路由"""
    api = Api(
        app,
        version="1.0.0",
        title="PMS API",
        description="投资组合管理系统 RESTful API",
        prefix="/api",
        doc="/docs"  # Swagger 文档路径
    )

    # 导入并注册各个模块的 API
    from app.api import auth, portfolio, asset, holding, transaction, cash_flow, performance, market, report, market_query

    api.add_namespace(auth.api, path="/auth")
    api.add_namespace(portfolio.api, path="/portfolios")
    api.add_namespace(asset.api, path="/assets")
    api.add_namespace(holding.api, path="/portfolios/<int:portfolio_id>/holdings")
    api.add_namespace(transaction.api, path="/portfolios/<int:portfolio_id>/transactions")
    api.add_namespace(cash_flow.api, path="/portfolios/<int:portfolio_id>/cash-flows")
    api.add_namespace(performance.api, path="/portfolios/<int:portfolio_id>/performance")
    api.add_namespace(market.api, path="/market")
    api.add_namespace(report.api, path="/reports")
    api.add_namespace(market_query.api, path="/market_query")
    
    # 注册持仓快照 API
    from app.api.holding import snapshot_api
    api.add_namespace(snapshot_api, path="/portfolios")
