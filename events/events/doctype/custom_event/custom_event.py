# -*- coding: utf-8 -*-
# Copyright (c) 2020, Mohamed Abdultawab and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _
from frappe.utils import nowdate, nowtime


class CustomEvent(WebsiteGenerator):

    def validate(self):
        self.validate_invitees()
        self.validate_date_and_time()

    def validate_date_and_time(self):
        if self.date < nowdate() or (self.date == nowdate() and self.start_time < nowtime()):
            frappe.throw(_("Cannot create event on past date"))

    def validate_invitees(self):
        """Set missing names and warn if duplicate"""
        found = []
        for invitee in self.invitees:
            if invitee.invitee in found:
                frappe.throw(
                    _("Invitee {0} entered twice").format(invitee.invitee))

            if not invitee.full_name:
                invitee.full_name = get_full_name(invitee.invitee)

            found.append(invitee.invitee)


@frappe.whitelist()
def get_full_name(invitee):
    user = frappe.get_doc("User", invitee)

    return " ".join(filter(None, (user.first_name, user.middle_name, user.last_name)))
