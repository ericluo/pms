from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.report import ReportService
from app.services.portfolio import PortfolioService
from app.schemas.report import ReportCreate, ReportResponse

api = Namespace('reports', description='报告相关操作')

# 模型定义
report_model = api.model('Report', {
    'id': fields.Integer(readonly=True),
    'portfolio_id': fields.Integer(required=True),
    'portfolio_name': fields.String(readonly=True),
    'type': fields.String(required=True),
    'title': fields.String(required=True),
    'generated_at': fields.DateTime(readonly=True),
    'url': fields.String(readonly=True)
})

@api.route('')
class ReportList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [report_model])
    @api.response(401, '未授权')
    def get(self):
        """获取报告列表"""
        db: Session = next(get_db())
        report_service = ReportService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        reports = report_service.get_reports(int(user_id))
        
        result = []
        for report in reports:
            portfolio = portfolio_service.get_portfolio(report.portfolio_id, int(user_id))
            if portfolio:
                result.append({
                    'id': report.id,
                    'portfolio_id': report.portfolio_id,
                    'portfolio_name': portfolio.name,
                    'type': report.type,
                    'title': report.title,
                    'generated_at': report.generated_at,
                    'url': f'/api/reports/{report.id}/export'
                })
        
        return result
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(report_model)
    @api.response(201, '创建成功', report_model)
    @api.response(401, '未授权')
    @api.response(400, '投资组合不存在或不属于该用户')
    def post(self):
        """创建报告"""
        db: Session = next(get_db())
        report_service = ReportService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        data = request.json
        
        try:
            report = report_service.create_report(ReportCreate(**data), int(user_id))
        except ValueError as e:
            api.abort(400, str(e))
        
        portfolio = portfolio_service.get_portfolio(report.portfolio_id, int(user_id))
        
        return {
            'id': report.id,
            'portfolio_id': report.portfolio_id,
            'portfolio_name': portfolio.name if portfolio else '',
            'type': report.type,
            'title': report.title,
            'generated_at': report.generated_at,
            'url': f'/api/reports/{report.id}/export'
        }, 201

@api.route('/<int:report_id>')
class ReportDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', report_model)
    @api.response(401, '未授权')
    @api.response(404, '报告不存在')
    def get(self, report_id):
        """获取报告详情"""
        db: Session = next(get_db())
        report_service = ReportService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        report = report_service.get_report(report_id, int(user_id))
        
        if not report:
            api.abort(404, '报告不存在')
        
        portfolio = portfolio_service.get_portfolio(report.portfolio_id, int(user_id))
        
        return {
            'id': report.id,
            'portfolio_id': report.portfolio_id,
            'portfolio_name': portfolio.name if portfolio else '',
            'type': report.type,
            'title': report.title,
            'generated_at': report.generated_at,
            'url': f'/api/reports/{report.id}/export'
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '报告不存在')
    def delete(self, report_id):
        """删除报告"""
        db: Session = next(get_db())
        report_service = ReportService(db)
        
        user_id = get_jwt_identity()
        success = report_service.delete_report(report_id, int(user_id))
        
        if not success:
            api.abort(404, '报告不存在')
        
        return {'message': '报告删除成功'}

@api.route('/<int:report_id>/export')
class ReportExport(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '导出成功')
    @api.response(401, '未授权')
    @api.response(404, '报告不存在')
    def get(self, report_id):
        """导出报告"""
        db: Session = next(get_db())
        report_service = ReportService(db)
        
        user_id = get_jwt_identity()
        content = report_service.generate_report_content(report_id, int(user_id))
        
        if not content:
            api.abort(404, '报告不存在')
        
        # 这里可以根据需要返回不同格式的报告，例如PDF、Excel等
        # 目前返回文本内容
        return content