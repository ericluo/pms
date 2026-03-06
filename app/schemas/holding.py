from marshmallow import Schema, fields, validate

class HoldingCreate(Schema):
    asset_id = fields.Integer(required=True)
    quantity = fields.Float(required=True, validate=validate.Range(min=0))
    cost_price = fields.Float(required=True, validate=validate.Range(min=0))
    current_price = fields.Float(required=True, validate=validate.Range(min=0))

class HoldingUpdate(Schema):
    asset_id = fields.Integer()
    quantity = fields.Float(validate=validate.Range(min=0))
    cost_price = fields.Float(validate=validate.Range(min=0))
    current_price = fields.Float(validate=validate.Range(min=0))

class HoldingResponse(Schema):
    id = fields.Integer()
    portfolio_id = fields.Integer()
    asset_id = fields.Integer()
    quantity = fields.Float()
    cost_price = fields.Float()
    current_price = fields.Float()
    value = fields.Float()
    profit = fields.Float()
    profit_percent = fields.Float()
    weight = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ["id", "portfolio_id", "asset_id", "quantity", "cost_price", "current_price", "value", "profit", "profit_percent", "weight", "created_at", "updated_at"]