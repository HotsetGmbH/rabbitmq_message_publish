import requests
import base64
import json
import uuid
import socket
import datetime
import frappe

def doctype_changed(doc, event):
        settings = frappe.get_single('RabbitMQ Settings')
        global_id = doc.name
        if hasattr(doc,'global_id'):
                global_id = doc.global_id
                
        payload = {}
        payload['transaction_id'] = str(uuid.uuid4())
        payload['system'] = 'erpnext'
        payload['datapool'] = settings.datapool_name
        payload['language'] = '' #TODO:  -> externen fragen
        payload['hostname'] = socket.gethostname().upper()
        payload['user'] = doc.modified_by
        payload['session_id'] = '' #TODO: Web-Session auslesen? -> externen fragen
        payload['operation'] = event
        payload['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        payload['business_object'] = doc.doctype
        payload['primary_key'] = doc.name
        payload['global_id'] = global_id
        payload['content'] = doc.as_dict()

        body = {}
        body['properties'] = {}
        body['routing_key'] = f"erpnext.{settings.datapool_id}.{doc.doctype}"
        #ensure_ascii=false -> for formatting special characters correctly
        #indent=4 -> beautifies json in message
        #default=str -> enables converting of complex objects to string
        body['payload'] = json.dumps(payload,ensure_ascii=False,indent=4,default=str)
        body['payload_encoding'] = "string"
        body_json = json.loads(json.dumps(body,ensure_ascii=False,indent=4))

        session = requests.Session()

        session.auth = (settings.username, settings.get_password('password'))#TODO: Passwort decrypten

        response = session.post(settings.url, json=body_json )
        response = response