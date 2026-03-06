from marshmallow import Schema, fields, validate

class MarketDataResponse(Schema):
    id = fields.Integer()
    asset_id = fields.Integer()
    date = fields.Date()
    open = fields.Float()
    high = fields.Float()
    low = fields.Float()
    close = fields.Float()
    volume = fields.Float()
    amount = fields.Float()
    created_at = fields.DateTime()

    class Meta:
        fields = ["id", "asset_id", "date", "open", "high", "low", "close", "volume", "amount", "created_at"]