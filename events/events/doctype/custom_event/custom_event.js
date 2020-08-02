// Copyright (c) 2020, Mohamed Abdultawab and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Event', {
	send_invitations: function(frm) {
		if (frm.doc.status==="Planned") {
			frappe.call({
				method: "events.api.send_invitation_emails",
				args: {
					event: frm.doc.name
				}
			});
		}
	},
});


frappe.ui.form.on("Event Invitee", {
	invitee: function(frm, cdt, cdn) {
		var invitee = frappe.model.get_doc(cdt, cdn);
		if (invitee.invitee) {
			// if invitee, get full name
			frappe.call({
				method: "events.events.doctype.custom_event.custom_event.get_full_name",
				args: {
					invitee: invitee.invitee
				},
				callback: function(r) {
					frappe.model.set_value(cdt, cdn, "full_name", r.message);
				}
			});

		} else {
			// if no invitee, clear full name
			frappe.model.set_value(cdt, cdn, "full_name", null);
		}
 	},
});