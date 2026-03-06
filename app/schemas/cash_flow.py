from marshmallow import Schema, fields, validate

class CashFlowCreate(Schema):
    flow_type = fields.String(required=True, validate=validate.Length(max=20))
    amount = fields.Float(required=True)
    description = fields.String(validate=validate.Length(max=500))
    flow_date = fields.DateTime(required=True)

class CashFlowUpdate(Schema):
    flow_type = fields.String(validate=validate.Length(max=20))
    amount = fields.Float()
    description = fields.String(validate=validate.Length(max=500))
    flow_date = fields.DateTime()

class CashFlowResponse(Schema):
    id = fields.Integer()
    portfolio_id = fields.Integer()
    flow_type = fields.String()
    amount = fields.Float()
    description = fields.String()
    flow_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ["id", "portfolio_id", "flow_type", "amount", "description", "flow_date", "created_at", "updated_at"]