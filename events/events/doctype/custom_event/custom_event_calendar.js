frappe.views.calendar["Custom Event"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "title",
        "status": "status",
        "allDay": "all_day"
	},
	get_events_method: "events.api.get_events"
}