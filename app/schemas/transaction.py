from marshmallow import Schema, fields, validate

class TransactionCreate(Schema):
    asset_id = fields.Integer(required=True)
    transaction_type = fields.String(required=True, validate=validate.OneOf(["买入", "卖出"]))
    quantity = fields.Float(required=True, validate=validate.Range(min=0))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    fee = fields.Float(validate=validate.Range(min=0))
    transaction_date = fields.DateTime(required=True)

class TransactionUpdate(Schema):
    asset_id = fields.Integer()
    transaction_type = fields.String(validate=validate.OneOf(["买入", "卖出"]))
    quantity = fields.Float(validate=validate.Range(min=0))
    price = fields.Float(validate=validate.Range(min=0))
    amount = fields.Float(validate=validate.Range(min=0))
    fee = fields.Float(validate=validate.Range(min=0))
    transaction_date = fields.DateTime()

class TransactionResponse(Schema):
    id = fields.Integer()
    portfolio_id = fields.Integer()
    asset_id = fields.Integer()
    transaction_type = fields.String()
    quantity = fields.Float()
    price = fields.Float()
    amount = fields.Float()
    fee = fields.Float()
    transaction_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        fields = ["id", "portfolio_id", "asset_id", "transaction_type", "quantity", "price", "amount", "fee", "transaction_date", "created_at", "updated_at"]