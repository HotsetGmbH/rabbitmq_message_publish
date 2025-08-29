from . import __version__ as app_version

app_name = "rabbitmq_message_publish"
app_title = "RabbitMQ Message Publish"
app_publisher = "Hotset"
app_description = "App for publishing doctype insert/update/delete messages to Rabbit MQ"
app_email = "jfinke@hotset.com"
app_license = "-"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rabbitmq_message_publish/css/rabbitmq_message_publish.css"
# app_include_js = "/assets/rabbitmq_message_publish/js/rabbitmq_message_publish.js"

# include js, css files in header of web template
# web_include_css = "/assets/rabbitmq_message_publish/css/rabbitmq_message_publish.css"
# web_include_js = "/assets/rabbitmq_message_publish/js/rabbitmq_message_publish.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rabbitmq_message_publish/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "rabbitmq_message_publish.utils.jinja_methods",
#	"filters": "rabbitmq_message_publish.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rabbitmq_message_publish.install.before_install"
# after_install = "rabbitmq_message_publish.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rabbitmq_message_publish.uninstall.before_uninstall"
# after_uninstall = "rabbitmq_message_publish.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "rabbitmq_message_publish.utils.before_app_install"
# after_app_install = "rabbitmq_message_publish.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "rabbitmq_message_publish.utils.before_app_uninstall"
# after_app_uninstall = "rabbitmq_message_publish.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rabbitmq_message_publish.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events, for available methods see: https://frappeframework.com/docs/user/en/guides/app-development/executing-code-on-doctype-events

#doc_events = {
#	("Customer","Address","Sales Order"):
#	{ 
#		"on_update":"rabbitmq_message_publish.events.doctype_changed",
#		"on_submit":"rabbitmq_message_publish.events.doctype_changed",
#		"on_cancel":"rabbitmq_message_publish.events.doctype_changed",
#		"on_trash":"rabbitmq_message_publish.events.doctype_changed"
#	}
#}

doc_events = {
	("Penta Job Card"):
	{ 
		"on_update":"rabbitmq_message_publish.events.doctype_changed",
		"on_submit":"rabbitmq_message_publish.events.doctype_changed",
		"on_cancel":"rabbitmq_message_publish.events.doctype_changed",
		"on_trash":"rabbitmq_message_publish.events.doctype_changed"
	},
	("Customer"):
	{
		"on_update":"rabbitmq_message_publish.events.doctype_changed",
		"on_submit":"rabbitmq_message_publish.events.doctype_changed",
		"on_cancel":"rabbitmq_message_publish.events.doctype_changed",
		"on_trash":"rabbitmq_message_publish.events.doctype_changed"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"rabbitmq_message_publish.tasks.all"
#	],
#	"daily": [
#		"rabbitmq_message_publish.tasks.daily"
#	],
#	"hourly": [
#		"rabbitmq_message_publish.tasks.hourly"
#	],
#	"weekly": [
#		"rabbitmq_message_publish.tasks.weekly"
#	],
#	"monthly": [
#		"rabbitmq_message_publish.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "rabbitmq_message_publish.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "rabbitmq_message_publish.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "rabbitmq_message_publish.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["rabbitmq_message_publish.utils.before_request"]
# after_request = ["rabbitmq_message_publish.utils.after_request"]

# Job Events
# ----------
# before_job = ["rabbitmq_message_publish.utils.before_job"]
# after_job = ["rabbitmq_message_publish.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"rabbitmq_message_publish.auth.validate"
# ]
