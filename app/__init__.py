from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.config import config
from app.utils.database import engine, Base

# 导入所有模型，确保它们被注册到Base.metadata
from app.models import user, portfolio, asset, holding, transaction, cash_flow, market_data, report

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