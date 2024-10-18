import requests
import json
import uuid
import socket
from datetime import datetime, timezone
import inspect
import frappe
import urllib.parse

def prepare_message_header (settings,user,event):
        language = frappe.session.data.lang
        if not language:
                language = "en"

        session = frappe.session.data.csrf_token
        if not session:
                session = "n.a."
                
        return {
                "transaction_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": session,
                "operation": event,
                "language": language,
                "system": settings.system,
                "datapool": settings.datapool_name,
                "hostname": socket.gethostname().upper(),
                "user": user
        }

def send_message (settings, message):

        virtual_host = urllib.parse.quote(settings.virtual_host,safe='')
        if message['routing_key'] == settings.logging_queue:
                # logging messages always go to default exchange
                exchange = ""
        else:
                exchange = settings.message_exchange

        url = settings.url + "/api/exchanges/" +  virtual_host + "/" + exchange + "/publish"
        if settings.dont_check_ssl_certificates:
                response = requests.post(url, auth=(settings.username, settings.get_password("password")), 
                                         json=message, verify=False)
        else:
                response = requests.post(url, auth=(settings.username, settings.get_password("password")), 
                                         json=message)

        if response.status_code != 200:
                raise Exception (f"Failed to send log entry: {response.status_code} {response.text}")


def log_to_kibana(loglevel, message, offset = 0):
        """
        loglevel: "debug" / "info" / "warning" / "error"
        message: Message to log
        offset: optional offset to identify code position on call-stack
        """

        settings = frappe.get_single('RabbitMQ Settings')
        if not settings.password:
                # this is only logging - if RabbitMQ is not configured yet we silently ignore it
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
        if settings.disabled:
                return

        if not settings.get_password:
             raise Exception ("RabbitMQ Settings missing!") 

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
        body['routing_key'] = settings.system_id + "." + settings.datapool_id + "." + doc.doctype

        # json.dumps():
        #   ensure_ascii=false -> for formatting special characters correctly
        #   indent=4 -> beautifies json in message
        #   default=str -> enables converting of complex objects to string
        body['payload'] = json.dumps(payload,ensure_ascii=False,indent=4,default=str)
        body['payload_encoding'] = "string"
        body_json = json.loads(json.dumps(body,ensure_ascii=False,indent=4))

        send_message(settings,body_json)
