from datetime import datetime
from flask import Blueprint
from peewee import Model, CharField, TextField, DateTimeField, AutoField
from db_config import db
from flask import request, jsonify

incidents_blueprint = Blueprint('incidents', __name__)

class BaseModel(Model):
    class Meta:
        database = db

class Incident(BaseModel):
    incidentID = AutoField()
    incidentName = CharField(max_length=255)
    incidentCategory = CharField(max_length=255)
    lat = CharField(max_length=50)
    lng = CharField(max_length=50)
    reportingType = CharField(max_length=255)
    reporterName = CharField(max_length=255)
    agoraUsername = CharField(max_length=255)
    agoraToken = TextField()
    status = CharField(max_length=50, default='unattended')
    channelName = CharField(max_length=255)
    createdAt = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'Incidents'

# Create the table if it doesn't exist
with db.connection_context():
    
    db.create_tables([Incident])

    @incidents_blueprint.route('/register_incident', methods=['POST'])
    def register_incident():
        try:
            data = request.json
            incident = Incident.create(
                incidentName=data['incidentName'],
                incidentCategory=data['incidentCategory'],
                lat=data['lat'],
                lng=data['lng'],
                reportingType=data['reportingType'],
                reporterName=data['reporterName'],
                agoraUsername=data['agoraUsername'],
                agoraToken=data['agoraToken'],
                channelName=data['channelName']
            )
            return jsonify({'message': 'Incident registered successfully', 'incidentID': incident.incidentID}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    @incidents_blueprint.route('/get_unattended_incidents', methods=['POST'])
    def get_unattended_incidents():
        try:
            incidents = Incident.select().where(Incident.status == 'unattended')
            incident_list = []
            for incident in incidents:
                incident_list.append({
                    'incidentID': incident.incidentID,
                    'incidentName': incident.incidentName,
                    'incidentCategory': incident.incidentCategory,
                    'lat': incident.lat,
                    'lng': incident.lng,
                    'reportingType': incident.reportingType,
                    'reporterName': incident.reporterName,
                    'agoraUsername': incident.agoraUsername,
                    'agoraToken': incident.agoraToken,
                    'status': incident.status,
                    'channelName': incident.channelName,
                    'createdAt': incident.createdAt
                })
            return jsonify(incident_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    @incidents_blueprint.route('/get_incident', methods=['POST'])
    def get_incident():
        """
        Get incident details by incident ID.
        """
        try:
            data = request.json
            incident = Incident.get(Incident.incidentID == data['incidentID'])
            return jsonify({
                'incidentID': incident.incidentID,
                'incidentName': incident.incidentName,
                'incidentCategory': incident.incidentCategory,
                'lat': incident.lat,
                'lng': incident.lng,
                'reportingType': incident.reportingType,
                'reporterName': incident.reporterName,
                'agoraUsername': incident.agoraUsername,
                'agoraToken': incident.agoraToken,
                'status': incident.status,
                'channelName': incident.channelName,
                'createdAt': incident.createdAt
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400