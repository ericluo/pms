from marshmallow import Schema, fields, validate

class AssetCreate(Schema):
    code = fields.String(required=True, validate=validate.Length(min=1, max=20))
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    type = fields.String(required=True, validate=validate.OneOf(['stock', 'fund', 'bond', 'cash']))
    market = fields.String(validate=validate.Length(max=50))
    industry = fields.String(validate=validate.Length(max=50))
    interest_rate = fields.Decimal(places=4)

class AssetUpdate(Schema):
    code = fields.String(validate=validate.Length(min=1, max=20))
    name = fields.String(validate=validate.Length(min=1, max=100))
    type = fields.String(validate=validate.OneOf(['stock', 'fund', 'bond', 'cash']))
    market = fields.String(validate=validate.Length(max=50))
    industry = fields.String(validate=validate.Length(max=50))
    interest_rate = fields.Decimal(places=4)

class AssetResponse(Schema):
    id = fields.Integer()
    code = fields.String()
    name = fields.String()
    type = fields.String()
    market = fields.String()
    industry = fields.String()
    interest_rate = fields.Decimal(places=4)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ["id", "code", "name", "type", "market", "industry", "interest_rate", "created_at", "updated_at"]