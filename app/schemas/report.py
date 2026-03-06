from marshmallow import Schema, fields, validate

class ReportCreate(Schema):
    portfolio_id = fields.Integer(required=True)
    type = fields.String(required=True, validate=validate.Length(max=50))
    title = fields.String(required=True, validate=validate.Length(max=200))

class ReportResponse(Schema):
    id = fields.Integer()
    portfolio_id = fields.Integer()
    portfolio_name = fields.String()
    type = fields.String()
    title = fields.String()
    generated_at = fields.DateTime()
    url = fields.String()

    class Meta:
        fields = ["id", "portfolio_id", "portfolio_name", "type", "title", "generated_at", "url"]