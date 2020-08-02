# -*- coding: utf-8 -*-
# Copyright (c) 2020, Mohamed Abdultawab and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest

import frappe
from frappe.test_runner import make_test_objects


class TestCustomEvent(unittest.TestCase):
	def setUp(self):
		# GIVEN

		# Make Sure db is clean
		frappe.db.sql('delete from `tabCustom Event` where title like "_Test Event%"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for-test%"')

		frappe.db.sql('delete from `tabUser` where email like "test_%"')
		frappe.db.sql('delete from `tabEvent Invitee` where invitee like "test_%"')

		# Create User
		user = frappe.get_doc({
			"doctype": "User",
			"email": "test_manager@swira.design",
			"first_name": "Test Manager",
		}).insert()
		# Deleting new user automatic welcome party event to not interfere with the test logic.
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for-test-manager"')

		user.add_roles('Event Manager')
		frappe.set_user('test_manager@swira.design')

		# Create events
		make_test_objects('Custom Event', reset=True)

		self.test_records = frappe.get_test_records('Custom Event')

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_event_list(self):
		"""
			Test event listing
		"""
		# WHEN
		res = frappe.get_list("Custom Event", fields=["name", "title"])

		# THEN
		self.assertEqual(len(res), 3)
		titles = [r.title for r in res]
		self.assertTrue("_Test Event 1" in titles)
		self.assertTrue("_Test Event 3" in titles)
		self.assertTrue("_Test Event 2" in titles)
		self.assertFalse("_Test Event 4" in titles)

		# WHEN
		frappe.db.sql(
			'delete from `tabCustom Event` where title = "_Test Event 2"')
		frappe.db.commit()
		res = frappe.get_list("Custom Event", fields=["name", "title"])

		# THEN
		self.assertEqual(len(res), 2)
		titles = [r.title for r in res]
		self.assertTrue("_Test Event 1" in titles)
		self.assertTrue("_Test Event 3" in titles)
		self.assertFalse("_Test Event 2" in titles)

	def test_create_events_in_the_past(self):
		"""
			Test can't create events in the past.
		"""

		# WHEN, THEN
		with self.assertRaises(frappe.exceptions.ValidationError):
			doc = frappe.get_doc({
				"doctype": "Custom Event",
				"title": "_Test Event 4",
				"date": "2014-01-01",
				"start_time": "20:00:00",
				"end_time": "22:00:00",
			}).insert()
		# THEN
		res = frappe.get_list("Custom Event", fields=["name", "title"])
		self.assertEqual(len(res), 3)
		titles = [r.title for r in res]
		self.assertFalse("_Test Event 4" in titles)

	def test_create_events_on_user_creation(self):
		"""
			Test a welcome party event is created for every new user.
		"""
		# WHEN
		doc = frappe.get_doc({
			"doctype": "User",
			"email": "test_1@swira.design",
			"first_name": "Test",
		}).insert()

		# THEN
		res = frappe.get_list("Custom Event", fields=["name", "title"])
		self.assertEqual(len(res), 4)
		titles = [r.title for r in res]
		self.assertTrue("Welcome Party for Test" in titles)

	def test_full_name_in_invitee(self):
		"""
			Test invitee full name is present in invitee table.
		"""

		# WHEN
		doc = frappe.get_doc({
			"doctype": "User",
			"email": "test_2@swira.design",
			"first_name": "TestFisrtName",
			"last_name": "TestLastName"
		}).insert()

		# THEN
		res = frappe.db.sql(
			'select full_name from `tabEvent Invitee` where parent = "welcome-party-for-testfisrtname"')
		self.assertEqual(len(res), 1)
		self.assertEqual(res[0][0], "TestFisrtName TestLastName")
