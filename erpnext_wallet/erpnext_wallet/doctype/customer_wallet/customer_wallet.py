# -*- coding: utf-8 -*-
# Copyright (c) 2022, Ahmed and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, now
import json
from frappe import _
from frappe.utils import now,today

class CustomerWallet(Document):
	pass

@frappe.whitelist()
def add_amount(data):
	doc = json.loads(data)
	if doc.get("wallet") : 
		wallet_doc = frappe.get_doc("Wallet",doc.get("wallet"))
		child = wallet_doc.append('wallet_entry')
		child.posting_date = today()
		child.posting_time = now()
		child.amount = doc.get("amount")
		child.mode_of_payment = doc.get("mode_of_payment")
		wallet_doc.save(ignore_permissions=True)
		frappe.msgprint(_("The Amount has been Added to the Wallet"))
		return True
	return False
	 
	
	
