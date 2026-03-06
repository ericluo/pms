from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.auth import AuthService
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse

api = Namespace('auth', description='认证相关操作')

# 模型定义
user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'role': fields.String(readonly=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

register_model = api.model('Register', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(required=True)
})

login_response = api.model('LoginResponse', {
    'access_token': fields.String(required=True),
    'token_type': fields.String(required=True),
    'user': fields.Nested(user_model)
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, '登录成功', login_response)
    @api.response(401, '用户名或密码错误')
    def post(self):
        """用户登录"""
        db: Session = next(get_db())
        auth_service = AuthService(db)
        
        data = request.json
        user = auth_service.authenticate_user(data['email'], data['password'])
        
        if not user:
            api.abort(401, '用户名或密码错误')
        
        access_token = auth_service.create_access_token(data={'sub': str(user.id)})
        
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
        }

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    @api.response(201, '注册成功', user_model)
    @api.response(400, '用户名或邮箱已存在')
    def post(self):
        """用户注册"""
        db: Session = next(get_db())
        auth_service = AuthService(db)
        
        data = request.json
        
        # 检查用户名是否已存在
        if auth_service.get_user_by_username(data['username']):
            api.abort(400, '用户名已存在')
        
        # 检查邮箱是否已存在
        if auth_service.get_user_by_email(data['email']):
            api.abort(400, '邮箱已存在')
        
        # 创建用户
        user = auth_service.create_user(data)
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }, 201

@api.route('/me')
class Me(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', user_model)
    @api.response(401, '未授权')
    def get(self):
        """获取当前用户信息"""
        db: Session = next(get_db())
        auth_service = AuthService(db)
        
        user_id = get_jwt_identity()
        user = db.query(User).filter_by(id=int(user_id)).first()
        
        if not user:
            api.abort(401, '用户不存在')
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }