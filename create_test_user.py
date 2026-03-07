"""
创建测试用户脚本
"""
from app.utils.database import SessionLocal
from app.services.auth import AuthService

def create_test_user():
    db = SessionLocal()
    auth_service = AuthService(db)
    
    # 检查用户是否已存在
    existing_user = auth_service.get_user_by_email("test123@example.com")
    if existing_user:
        print("测试用户已存在")
        db.close()
        return
    
    # 创建测试用户
    user_data = {
        "username": "test123",
        "email": "test123@example.com",
        "password": "123456",
        "name": "测试用户"
    }
    
    user = auth_service.create_user(user_data)
    print(f"测试用户创建成功：{user.email}")
    db.close()

if __name__ == "__main__":
    create_test_user()
