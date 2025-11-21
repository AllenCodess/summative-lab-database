#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker
from schemas import EventSchema, SessionSchema, SpeakerSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

event_schema = EventSchema()
event_list_schema = EventSchema(many=True)

session_schema = SessionSchema()
session_list_schema = SessionSchema(many=True)

speaker_schema = SpeakerSchema()
speaker_list_schema = SpeakerSchema(many=True)

# ROUTES ------------------------------------------------------

@app.route('/events')
def get_events():
    all_events = Event.query.all()
    return event_list_schema.dump(all_events), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    return session_list_schema.dump(event.sessions), 200


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    return speaker_list_schema.dump(speakers), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.get(id)
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404

    return speaker_schema.dump(speaker), 200


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.get(id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    return speaker_list_schema.dump(session.speakers), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
