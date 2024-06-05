// Copyright (c) 2023, Hotset and contributors
// For license information, please see license.txt

frappe.ui.form.on('RabbitMQ Settings', {
    refresh: function(frm) {
        frm.add_custom_button(__('Send Test Message'), function() {
            frappe.call({
                method: 'rabbitmq_message_publish.rabbitmq_message_publish.doctype.rabbitmq_settings.rabbitmq_settings.send_test_message',
                args: {
                },
                callback: function(r) {
                    frappe.msgprint(r.message);
                }
            });
        });
    }
});
