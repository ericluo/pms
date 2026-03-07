from marshmallow import Schema, fields, validate

class PortfolioCreate(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))
    benchmark = fields.String(required=True, validate=validate.Length(max=50))
    risk_level = fields.String(required=True, validate=validate.Length(max=20))
    is_default = fields.Boolean(load_default=False)

class PortfolioUpdate(Schema):
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))
    benchmark = fields.String(validate=validate.Length(max=50))
    risk_level = fields.String(validate=validate.Length(max=20))
    is_default = fields.Boolean()

class PortfolioResponse(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    name = fields.String()
    description = fields.String()
    benchmark = fields.String()
    risk_level = fields.String()
    is_default = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ["id", "user_id", "name", "description", "benchmark", "risk_level", "is_default", "created_at", "updated_at"]