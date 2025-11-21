from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# --- MANY TO MANY TABLES ---

event_session = db.Table(
    'event_session',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), nullable=False),
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), nullable=False)
)

session_speaker = db.Table(
    'session_speaker',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), nullable=False),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), nullable=False)
)

# --- MODELS ---

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Relationships
    sessions = db.relationship("Session", secondary=event_session, back_populates="events")

    # Validations
    @validates("title")
    def validate_title(self, key, value):
        if not value or len(value) < 3:
            raise ValueError("Event title must be at least 3 characters long.")
        return value

    @validates("location")
    def validate_location(self, key, value):
        if not value:
            raise ValueError("Location cannot be empty.")
        return value

    def __repr__(self):
        return f"<Event {self.id}: {self.title}, {self.location}>"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "location": self.location}


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

    # Relationships
    events = db.relationship("Event", secondary=event_session, back_populates="sessions")
    speakers = db.relationship("Speaker", secondary=session_speaker, back_populates="sessions")

    # Validations
    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Session name is required.")
        return value

    @validates("time")
    def validate_time(self, key, value):
        if not value:
            raise ValueError("Session time is required.")
        return value

    def __repr__(self):
        return f"<Session {self.id}: {self.name} at {self.time}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "time": self.time}


class Speaker(db.Model):
    __tablename__ = "speakers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationships
    bio = db.relationship("Bio", uselist=False, back_populates="speaker", cascade="all, delete-orphan")
    sessions = db.relationship("Session", secondary=session_speaker, back_populates="speakers")

    # Validations
    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) < 2:
            raise ValueError("Speaker name must be at least 2 characters.")
        return value

    def __repr__(self):
        return f"<Speaker {self.id}: {self.name}>"

    def to_dict(self):
        data = {"id": self.id, "name": self.name}
        data["bio"] = self.bio.bio_text if self.bio else "No bio available"
        return data


class Bio(db.Model):
    __tablename__ = "bios"

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.String, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey("speakers.id"), nullable=False, unique=True)

    # Relationship
    speaker = db.relationship("Speaker", back_populates="bio")

    def __repr__(self):
        return f"<Bio {self.id}: {self.bio_text[:30]}...>"
