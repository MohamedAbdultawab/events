from __future__ import unicode_literals
from frappe import _


def get_data():
	"""
		Add evetns module to desk home screen."""
	return [
		{
			"label": _("Events"),
			"icon": "octicon octicon-briefcase",
			"items": [
				{
					"type": "doctype",
					"name": "Custom Event",
					"label": _("Custom Event"),
					"description": _("Custom Events Module Description."),
				},
			]
		}
	]
