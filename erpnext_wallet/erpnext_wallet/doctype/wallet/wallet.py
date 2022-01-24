# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import cstr, flt, fmt_money, formatdate
from frappe.utils import add_days, add_months, comma_sep, getdate, today
from frappe.model.document import Document
from frappe.utils.csvutils import getlink
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from erpnext.accounts.party import get_party_account

from erpnext.controllers.accounts_controller import get_advance_payment_entries


class Wallet(Document):
	
	def validate(self):
		self.validate_amount()
		self.get_total()
		self.create_refernces()



	def validate_amount(self):
		for d in self.get("wallet_entry"):
			if flt(d.amount) and flt(d.allocated):
				frappe.throw(_("You cannot set Amount and Allocated  at the same time"))
			if flt(d.amount) < 0:
				frappe.throw(_("Not Allowed, Negative Value"))
				

		
	def get_total(self):
		total_amount = 0
		total_allocated = 0
		total_remaining = 0
		
		for d in self.get("wallet_entry"):
			total_amount +=abs(flt(d.amount))
			total_allocated +=abs(flt(d.allocated))
		self.total_amount = total_amount
		self.total_allocated = total_allocated
		self.total_remaining = total_amount - total_allocated

	
	def create_refernces(self, submit= True):
		"""create payment entry"""
		frappe.flags.ignore_account_permission = True
		ref_doc = None
		for d in self.get("wallet_entry"):
			company = frappe.defaults.get_user_default("company")
			payment_account = get_bank_cash_account(d.mode_of_payment, company).get("account")
			party_account = get_party_account('Customer', self.customer, company)
			if not d.customer_account:
				d.customer_account = party_account
			
			if flt(d.amount) > 0 and not d.reference_name : 
				ref_doc = frappe.get_doc({
					"doctype" : "Payment Entry",
					"company": company,
					"posting_date": today(),
					"reference_no": self.name,
					"party_type" : "Customer",
					"party" :  self.customer_name,
					"party_name": self.customer_name,
					"paid_from":  d.customer_account,
					"paid_from_account_currency": "SAR",
					"source_exchange_rate": 1,
					"paid_to": payment_account,
					"paid_to_account_currency": "SAR",
					"target_exchange_rate": 1,
					"mode_of_payment": d.mode_of_payment, 
					"received_amount": d.amount,
					"base_received_amount": d.amount,
					"base_paid_amount": d.amount,
					"paid_amount": d.amount,
					"remarks": "Amount  SAR {0} against from customer {1}".format(flt(d.amount), self.customer_name)
				})
				ref_doc.insert(ignore_permissions=True)
				ref_doc.submit()
				d.reference_name = ref_doc.name
				d.reference_type = "Payment Entry"
				frappe.msgprint(_("Payment Entry {0} created").format(getlink("Payment Entry", ref_doc.name)))
																	
				
			
			
			
			# ~ elif flt(d.allocated) > 0 and not d.reference_name:
				# ~ frappe.throw(_("Not Allowed, Add Sales Invoice to the referance")) 
			if flt(d.allocated) > 0 and d.reference_name and not d.assigned:
				si_doc = frappe.get_doc("Sales Invoice", d.reference_name)
				if si_doc.customer != self.customer:
					frappe.throw(_("Not Allowed, Wrong Customer"))
					
				payment_entries = self.get_payment_entries() 
				print(len(payment_entries))
				total_payment = 0.0 
				for p in payment_entries :
					print(p)
					total_payment += p.amount
				
				print(d.allocated)
				print(total_payment)
				if d.allocated > total_payment:
					frappe.throw(_("Not Allowed, allocated Value bigger than the Wallet"))
				
				total_alocated = d.allocated
				pe_list = []
				for p in payment_entries :
					if total_alocated <= 0 :
						break
					if total_alocated - p.amount >0 :
						pe_list.append({"reference_name":p.reference_name,"amount":p.amount})
					
					if total_alocated - p.amount <=0 :
						pe_list.append({"reference_name":p.reference_name,"amount":total_alocated})
					
					total_alocated -= p.amount
					
				
				for pe in pe_list :
					print(pe)
					print(pe["amount"])
					pe_doc = frappe.get_doc("Payment Entry", pe["reference_name"])
					pe_doc.make_gl_entries(cancel=1, adv_adj=1)
					
					
					data = {
						"reference_doctype": "Sales Invoice",
						"reference_name": si_doc.name,
						"total_amount": si_doc.grand_total,
						"outstanding_amount": si_doc.outstanding_amount,
						"allocated_amount": pe["amount"],
						"exchange_rate": 1
					}
					
					update_reference_in_payment_entry(data, pe_doc)
					pe_doc = frappe.get_doc("Payment Entry", p.reference_name)
					print(pe_doc.make_gl_entries(cancel=0, adv_adj=1))
					pe_doc.update_expense_claim()
					pe_doc.set_status()
					pe_doc.save(ignore_permissions=True)
				d.assigned =1


		return ref_doc



		# ~ # cancel advance entry
		# ~ doc = frappe.get_doc(d.voucher_type, d.voucher_no)

		# ~ doc.make_gl_entries(cancel=1, adv_adj=1)

		# ~ # update ref in advance entry
		# ~ if d.voucher_type == "Journal Entry":
			# ~ update_reference_in_journal_entry(d, doc)
		# ~ else:
			# ~ update_reference_in_payment_entry(d, doc)

		# ~ # re-submit advance entry
		# ~ doc = frappe.get_doc(d.voucher_type, d.voucher_no)
		# ~ doc.make_gl_entries(cancel = 0, adv_adj =1)

		# ~ if d.voucher_type in ('Payment Entry', 'Journal Entry'):
			# ~ doc.update_expense_claim()
			
			
					

	
	def get_payment_entries(self):
		order_doctype = "Sales Order"
		company = frappe.defaults.get_user_default("company")
		party_account = get_party_account('Customer', self.customer, company)
		
		payment_entries = get_advance_payment_entries("Customer", self.customer,
			party_account, order_doctype, against_all_orders=True, limit=None)

		return payment_entries



def update_reference_in_payment_entry(d, payment_entry, do_not_save=False):
	print("Payment ENtry")
	print(payment_entry.name)
	print("Payment ENtry")
	reference_details = {
		"reference_doctype": d["reference_doctype"],
		"reference_name": d["reference_name"],
		"total_amount": d["total_amount"],
		"outstanding_amount": d["outstanding_amount"],
		"allocated_amount": d["allocated_amount"],
		"exchange_rate": d["exchange_rate"]
	}


	new_row = payment_entry.append("references")
	new_row.docstatus = 1
	new_row.update(reference_details)

	payment_entry.flags.ignore_validate_update_after_submit = True
	payment_entry.setup_party_account_field()
	payment_entry.set_missing_values()
	payment_entry.set_amounts()
	print(new_row)
	# ~ if d.difference_amount and d.difference_account:
		# ~ payment_entry.set_gain_or_loss(account_details={
			# ~ 'account': d.difference_account,
			# ~ 'cost_center': payment_entry.cost_center or frappe.get_cached_value('Company',
				# ~ payment_entry.company, "cost_center"),
			# ~ 'amount': d.difference_amount
		# ~ })

	if not do_not_save:
		payment_entry.save(ignore_permissions=True)
