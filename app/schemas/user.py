from marshmallow import Schema, fields, validate

class UserCreate(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    password = fields.String(required=True, validate=validate.Length(min=6))
    name = fields.String(required=True, validate=validate.Length(max=100))

class UserLogin(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserResponse(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    name = fields.String()
    role = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ["id", "username", "email", "name", "role", "created_at", "updated_at"]