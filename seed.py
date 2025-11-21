#!/usr/bin/env python3

from app import app
from models import db, Event, Session, Speaker, Bio

with app.app_context():

    print("Clearing database...")
    Event.query.delete()
    Session.query.delete()
    Speaker.query.delete()
    Bio.query.delete()

    print("Creating records...")

    e1 = Event(title="Tech Conference", location="New York")
    e2 = Event(title="Developer Summit", location="San Francisco")

    s1 = Session(name="AI Workshop", time="10:00 AM")
    s2 = Session(name="Cybersecurity Panel", time="2:00 PM")

    sp1 = Speaker(name="John Doe")
    sp1.bio = Bio(bio_text="Machine learning engineer with 10 years experience.")

    sp2 = Speaker(name="Sarah Lee")
    sp2.bio = Bio(bio_text="Cybersecurity expert specializing in network defense.")

    e1.sessions.append(s1)
    e2.sessions.append(s2)

    s1.speakers.append(sp1)
    s2.speakers.append(sp2)

    db.session.add_all([e1, e2, s1, s2, sp1, sp2])
    db.session.commit()

    print("Database seeded!")
