from datetime import datetime
from flask import Blueprint
from peewee import Model, CharField, TextField, DateTimeField, AutoField
from db_config import db
from flask import request, jsonify

reponder_blueprint = Blueprint('responder', __name__)

class BaseModel(Model):
    class Meta:
        database = db

class Responder(BaseModel):
    reporter_id = AutoField()
    email = CharField(unique=True)
    name = CharField()
    pinCode = CharField()
    agoraUsername = CharField()
    firebaseToken = TextField()
    createdAt = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'Responders'

with db.connection_context():
    
    db.create_tables([Responder])


    """ @reponder_blueprint.route('/register_reporter', methods=['POST'])
    def register_reporter():
        data = request.get_json()
        try:
            reporter = Reporter.create(
                email=data['email'],
                name=data['name'],
                pinCode=data['pinCode'],
                agoraUsername=data['agoraUsername'],
                firebaseToken=data['firebaseToken']
            )
            return jsonify({"message": "Reporter registered successfully", "reporter_id": reporter.reporter_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400 """