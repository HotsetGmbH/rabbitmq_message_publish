import requests
import json
import uuid
import socket
from datetime import datetime, timezone
import inspect
import frappe

def prepare_message_header (settings,user,event):
        language = frappe.session.data.lang
        if not language:
                language = "en"
                
        return {
                "transaction_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": "", #TODO: Web-Session auslesen? -> externen fragen
                "operation": event,
                "language": language,
                "system": "erpnext", # TODO datapool
                "datapool": settings.datapool_name,
                "hostname": socket.gethostname().upper(),
                "user": user
        }

def send_message (settings, message):
        try:

                url = settings.url + "/api/exchanges/" +  settings.virtual_host + "/" + settings.message_exchange + "/publish"

                response = requests.post(url, auth=(settings.username, settings.get_password("password")), json=message)
                if response.status_code != 200:
                        print(f"Failed to send log entry: {response.status_code} {response.text}")
        except Exception as err:
                print(f'An unexpected error occurred: {err}')

def log_to_kibana(loglevel, message, offset = 0):
        """
        loglevel: "debug" / "info" / "warning" / "error"
        message: Message to log
        offset: optional offset to identify code position on call-stack
        """

        settings = frappe.get_single('RabbitMQ Settings')
        if not settings.password:
                return
        
        username = frappe.session.user
        if not username:
                username = "n.a."

        caller_frame = inspect.stack()[offset+1]
        caller_module = inspect.getmodule(caller_frame[0])
        code_position = f"{caller_module.__name__}.{caller_frame.function} ({caller_frame.filename}, line {caller_frame.lineno})"

        payload = prepare_message_header(settings,username,"logging")
        payload['log_level'] = loglevel
        payload['code_position'] = code_position
        payload['message'] = message

        body = {}
        body['properties'] = {}
        body['routing_key'] = settings.logging_queue
        body['payload'] = json.dumps(payload,ensure_ascii=False,indent=4,default=str)
        body['payload_encoding'] = "string"

        send_message(settings,json.loads(json.dumps(body,ensure_ascii=False,indent=4)))
       

def doctype_changed(doc, event):
        settings = frappe.get_single('RabbitMQ Settings')

        global_id = doc.name
        if hasattr(doc,'global_id'):
                global_id = doc.global_id

        payload = prepare_message_header(settings,doc.modified_by,event)
        payload['business_object'] = doc.doctype
        payload['primary_key'] = doc.name
        payload['global_id'] = global_id
        payload['content'] = doc.as_dict()

        body = {}
        body['properties'] = {}
        body['routing_key'] = f"erpnext.{settings.datapool_id}.{doc.doctype}"

        # json.dumps():
        #   ensure_ascii=false -> for formatting special characters correctly
        #   indent=4 -> beautifies json in message
        #   default=str -> enables converting of complex objects to string
        body['payload'] = json.dumps(payload,ensure_ascii=False,indent=4,default=str)
        body['payload_encoding'] = "string"
        body_json = json.loads(json.dumps(body,ensure_ascii=False,indent=4))

        send_message(settings,body_json)
