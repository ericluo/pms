from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.report import Report
from app.models.portfolio import Portfolio
from app.schemas.report import ReportCreate

class ReportService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_reports(self, user_id: int) -> List[Report]:
        # 获取用户的所有报告
        portfolios = self.db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
        portfolio_ids = [p.id for p in portfolios]
        return self.db.query(Report).filter(Report.portfolio_id.in_(portfolio_ids)).order_by(Report.generated_at.desc()).all()
    
    def get_report(self, report_id: int, user_id: int) -> Optional[Report]:
        # 获取单个报告
        report = self.db.query(Report).filter(Report.id == report_id).first()
        if not report:
            return None
        
        # 验证报告所属的投资组合是否属于该用户
        portfolio = self.db.query(Portfolio).filter(
            Portfolio.id == report.portfolio_id,
            Portfolio.user_id == user_id
        ).first()
        
        return report if portfolio else None
    
    def create_report(self, report_create: ReportCreate, user_id: int) -> Report:
        # 验证投资组合是否属于该用户
        portfolio = self.db.query(Portfolio).filter(
            Portfolio.id == report_create.portfolio_id,
            Portfolio.user_id == user_id
        ).first()
        
        if not portfolio:
            raise ValueError("投资组合不存在或不属于该用户")
        
        # 创建报告
        db_report = Report(
            portfolio_id=report_create.portfolio_id,
            type=report_create.type,
            title=report_create.title
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report
    
    def delete_report(self, report_id: int, user_id: int) -> bool:
        report = self.get_report(report_id, user_id)
        if not report:
            return False
        
        self.db.delete(report)
        self.db.commit()
        return True
    
    def generate_report_content(self, report_id: int, user_id: int) -> Optional[str]:
        # 生成报告内容
        report = self.get_report(report_id, user_id)
        if not report:
            return None
        
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == report.portfolio_id).first()
        if not portfolio:
            return None
        
        # 这里可以根据需要生成详细的报告内容
        # 包括持仓分析、业绩分析、风险分析等
        content = f"# {report.title}\n\n"
        content += f"**报告类型**: {report.type}\n"
        content += f"**投资组合**: {portfolio.name}\n"
        content += f"**生成时间**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "## 报告内容\n\n"
        content += "这里是报告的详细内容..."
        
        return content