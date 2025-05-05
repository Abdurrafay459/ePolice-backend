from datetime import datetime
from flask import Blueprint
from peewee import Model, CharField, TextField, DateTimeField, AutoField
from db_config import db
from flask import request, jsonify

responder_blueprint = Blueprint('responder', __name__)

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
    lat = CharField(null=True)
    lng = CharField(null=True)
    createdAt = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'Responders'

with db.connection_context():
    db.create_tables([Responder])

    @responder_blueprint.route('/register_responder', methods=['POST'])
    def register_responder():
        data = request.get_json()
        try:
            reporter = Responder.create(
                email=data['email'],
                name=data['name'],
                pinCode=data['pinCode'],
                agoraUsername=data['agoraUsername'],
                firebaseToken=data['firebaseToken']
            )
            return jsonify({"message": "Reporter registered successfully", "reporter_id": reporter.reporter_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @responder_blueprint.route('/responder_login', methods=['POST'])
    def reporter_login():
        data = request.get_json()
        try:
            pin_code = data.get('pinCode')
            if not pin_code:
                return jsonify({"error": "pinCode is required"}), 400

            reporter = Responder.get_or_none(Responder.pinCode == pin_code)
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
            print(e)
            return jsonify({"error": str(e)}), 400
        
    @responder_blueprint.route('/get_all_responders', methods=['POST'])
    def get_all_responders():
        try:
            responders = Responder.select()
            responders_list = [{
                "reporter_id": responder.reporter_id,
                "email": responder.email,
                "name": responder.name,
                "pinCode": responder.pinCode,
                "agoraUsername": responder.agoraUsername,
                "firebaseToken": responder.firebaseToken,
                "createdAt": responder.createdAt.strftime('%Y-%m-%d %H:%M:%S')
            } for responder in responders]

            return jsonify(responders_list), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @responder_blueprint.route('/update_responder_location', methods=['POST'])
    def update_responder_location():
        data = request.get_json()
        try:
            email = data.get('email')
            lat = data.get('lat')
            lng = data.get('lng')

            if not all([email, lat, lng]):
                return jsonify({"error": "email, lat, and lng are required"}), 400

            responder = Responder.get_or_none(Responder.email == email)
            if not responder:
                return jsonify({"error": "Responder not found"}), 404

            responder.lat = lat
            responder.lng = lng
            responder.save()

            return jsonify({"message": "Location updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500