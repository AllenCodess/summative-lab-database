from marshmallow import Schema, fields, validate

class BioSchema(Schema):
    id = fields.Int(dump_only=True)
    bio_text = fields.Str(required=True, validate=validate.Length(min=5))

class SpeakerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    bio = fields.Nested(BioSchema, dump_only=True)

class SessionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    time = fields.Str(required=True)
    speakers = fields.Nested(SpeakerSchema, many=True, dump_only=True)

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3))
    location = fields.Str(required=True)
    sessions = fields.Nested(SessionSchema, many=True, dump_only=True)
