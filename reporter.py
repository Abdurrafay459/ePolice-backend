from datetime import datetime
from flask import Blueprint
from peewee import Model, CharField, TextField, DateTimeField, AutoField
from db_config import db
from flask import request, jsonify

reporters_blueprint = Blueprint('reporters', __name__)

class BaseModel(Model):
    class Meta:
        database = db

class Reporter(BaseModel):
    reporter_id = AutoField()
    email = CharField(unique=True)
    name = CharField()
    pinCode = CharField()
    agoraUsername = CharField()
    firebaseToken = TextField()
    createdAt = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'Reporters'

with db.connection_context():
    
    db.create_tables([Reporter])

    @reporters_blueprint.route('/register_reporter', methods=['POST'])
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
            return jsonify({"error": str(e)}), 400

    @reporters_blueprint.route('/reporter_login', methods=['POST'])
    def reporter_login():
        data = request.get_json()
        try:
            pin_code = data.get('pinCode')
            if not pin_code:
                return jsonify({"error": "pinCode is required"}), 400

            reporter = Reporter.get_or_none(Reporter.pinCode == pin_code)
            if reporter:
                return jsonify({"message": "Login successful", "reporter": {
                    "reporter_id": reporter.reporter_id,
                    "email": reporter.email,
                    "name": reporter.name,
                    "pinCode": reporter.pinCode,
                    "agoraUsername": reporter.agoraUsername,
                    "firebaseToken": reporter.firebaseToken,
                    "createdAt": reporter.createdAt
                }}), 200
            else:
                return jsonify({"error": "Invalid pinCode"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500