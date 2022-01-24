# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import  flt

def update_wallet(doc,method =None):
    parent_doc = frappe.get_doc("Wallet",doc.parent)
    parent_doc.save(ignore_permissions=True)


	


    

    







