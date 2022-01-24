# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_wallet"
app_title = "Erpnext Wallet"
app_publisher = "PET Oasis"
app_description = "Wallet"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "alaa@petoasis.com.sa "
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_wallet/css/erpnext_wallet.css"
# app_include_js = "/assets/erpnext_wallet/js/erpnext_wallet.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_wallet/css/erpnext_wallet.css"
# web_include_js = "/assets/erpnext_wallet/js/erpnext_wallet.js"

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

# Website user home page (by function)
# get_website_user_home_page = "erpnext_wallet.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_wallet.install.before_install"
# after_install = "erpnext_wallet.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_wallet.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Wallet Entry":{	
		"after_insert": "erpnext_wallet.tool.update_wallet"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_wallet.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_wallet.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_wallet.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_wallet.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_wallet.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_wallet.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_wallet.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpnext_wallet.task.get_dashboard_data"
# }

