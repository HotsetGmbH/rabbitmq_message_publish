# Copyright (c) 2023, Hotset and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from rabbitmq_message_publish.events import log_to_kibana  # Importiere die Methode korrekt

@frappe.whitelist()
def send_test_message():
	try:
		log_to_kibana("info", "RabbitMQ settings are configured correctly.")

		return {
            "status": "success",
            "message": "Test message sent successfully."
        }
	
	except Exception as e:

		return {
			"status": "error",
			"message": str(e)
		}


class RabbitMQSettings(Document):
	pass

