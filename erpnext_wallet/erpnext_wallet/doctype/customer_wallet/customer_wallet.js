// Copyright (c) 2022, Ahmed and contributors
// For license information, please see license.txt


frappe.ui.form.on('Customer Wallet', {
	add_amount: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.amount && d.mode_of_payment){
			return frappe.call({
				method: "customizer.customizer.doctype.customer_wallet.customer_wallet.add_amount",
				args: {
					data: frm.doc
				},
				callback: function(r) {
					if(r.message) {
						console.log(r.message)

					}
				}
			});
		}
		else {
			frappe.throw(__("Please Add Amount and Mode of Payment to Continue" ));
		}
	},
	refresh: function(frm) {
			frm.disable_save();
			frm.add_custom_button(__('Clear'), () => {
				return frm.trigger('clear');
			});
		},
	clear: function(frm){
			frm.clear_table("wallet_entry");
			frm.doc.wallet = '';
			frm.doc.total_amount = 0;
			frm.doc.total_allocated = 0;
			frm.doc.total_remaining = 0;
			frm.doc.amount = 0;
			frm.doc.mode_of_payment = '';
			frm.refresh_fields();
					
	},
	wallet: function(frm) {
			frm.doc.wallet_entry = [];
			frappe.model.with_doc("Wallet", frm.doc.wallet, function() {
		    var tabletransfer= frappe.model.get_doc("Wallet", frm.doc.wallet)
		    $.each(tabletransfer.wallet_entry, function(index, row){
			var d = frm.add_child("wallet_entry");
			d.posting_date = row.posting_date;
			d.posting_time = row.posting_time;
			d.amount = row.amount;
			d.allocated = row.allocated;
			d.mode_of_payment = row.mode_of_payment;
			frm.set_df_property("wallet_entry", "read_only", 1);
			frm.refresh_field("wallet_entry");
		    });
		});
	}
})



