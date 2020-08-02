import frappe
from frappe import _
from frappe.utils import add_days, nowdate


@frappe.whitelist()
def send_invitation_emails(event):
	"""
		Send Email Invitations to event invitees.
	"""

	event = frappe.get_doc("Custom Event", event)
	# event.check_permission("email")

	if event.status == "Planned":
		frappe.sendmail(
			recipients=[d.invitee for d in event.invitees],
			sender='mohamedtoba96@gmail.com',
			subject=event.invitation_subject or event.title,
			message=event.invitation_message,
			reference_doctype=event.doctype,
			reference_name=event.name,
		)

		event.status = "Invitations Sent"
		event.save()

		frappe.msgprint(_("Invitation Sent"))

	else:
		frappe.msgprint(_("Event Status must be 'Planned'"))


@frappe.whitelist()
def get_events(start, end):
	"""
		Return Event list.
	"""
	if not frappe.has_permission("Custom Event", "read"):
		raise frappe.PermissionError

	data = frappe.db.sql("""select
		timestamp(timestamp(`date`), start_time) as start,
		timestamp(timestamp(`date`), end_time) as end,
		name,
		title,
		status,
		0 as all_day
		from `tabCustom Event`
		where `date` between %(start)s and %(end)s""", {
		"start": start,
		"end": end
	}, as_dict=True)
	return data


def create_welcome_party_event(doc, method):
	"""
			Create a welcome party event when a new User is added.
	"""

	event = frappe.get_doc({
		"doctype": "Custom Event",
		"title": "Welcome Party for {0}".format(doc.first_name),
		"date": add_days(nowdate(), 7),
		"from_time": "09:00",
		"to_time": "09:30",
		"status": "Planned",
		"invitees": [{
			"invitee": doc.name
		}]
	})
	# the System Manager might not have permission to create a Meeting
	event.flags.ignore_permissions = True
	event.insert()

	frappe.msgprint(_("Welcome party event created"))
