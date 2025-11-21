Install dependencies

pipenv install


Seed the database

pipenv run python seed.py


Run the app

pipenv run python app.py


Access the API

Open your browser or use a tool like Postman:

List events: http://127.0.0.1:5555/events

Get sessions for an event: http://127.0.0.1:5555/events/1/sessions

List speakers: http://127.0.0.1:5555/speakers

Get a speaker: http://127.0.0.1:5555/speakers/1

Get speakers for a session: http://127.0.0.1:5555/sessions/1/speakers
