# -*- coding: utf-8 -*-
# Copyright (c) 2020, Mohamed Abdultawab and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest

import frappe
from frappe.test_runner import make_test_objects


class TestCustomEvent(unittest.TestCase):
	def setUp(self):
		# Make Sure db is clean
		frappe.db.sql('delete from `tabCustom Event` where title like "_Test Event%"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for-event"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for-testfisrtname"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for--%"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for-test%"')

		frappe.db.sql('delete from `tabUser` where email like "test_%"')
		frappe.db.sql('delete from `tabEvent Invitee` where invitee like "test_%"')

		# Create User
		user = frappe.get_doc({
			"doctype": "User",
			"email": "test_manager@swira.design",
			"first_name": "Event",
			"last_name": "Manager"
		}).insert()
		frappe.db.sql('delete from `tabCustom Event` where title like "welcome-party-for-Event"')
		user.add_roles('Event Manager')
		frappe.set_user('test_manager@swira.design')

		# Create events
		make_test_objects('Custom Event', reset=True)

		self.test_records = frappe.get_test_records('Custom Event')

	def tearDown(self):
		frappe.db.sql('delete from `tabCustom Event` where title like "_Test Event%"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for-event"')
		frappe.db.sql('delete from `tabCustom Event` where name like "welcome-party-for--%"')
		frappe.db.sql('delete from `tabUser` where email like "test_%"')
		frappe.db.sql('delete from `tabEvent Invitee` where invitee like "test_%"')
		frappe.set_user("Administrator")

	def test_event_list(self):
		res = frappe.get_list("Custom Event", filters=[
			["Custom Event", "title", "like", "_Test Event%"]], fields=["name", "title"])
		self.assertEqual(len(res), 3)
		titles = [r.title for r in res]
		self.assertTrue("_Test Event 1" in titles)
		self.assertTrue("_Test Event 3" in titles)
		self.assertTrue("_Test Event 2" in titles)
		self.assertFalse("_Test Event 4" in titles)

		frappe.db.sql(
			'delete from `tabCustom Event` where title = "_Test Event 2"')
		frappe.db.commit()
		res = frappe.get_list("Custom Event", filters=[
			["Custom Event", "title", "like", "_Test Event%"]], fields=["name", "title"])
		self.assertEqual(len(res), 2)
		titles = [r.title for r in res]
		self.assertTrue("_Test Event 1" in titles)
		self.assertTrue("_Test Event 3" in titles)
		self.assertFalse("_Test Event 2" in titles)

	def test_create_events_in_the_past(self):
		with self.assertRaises(frappe.exceptions.ValidationError):
			doc = frappe.get_doc({
				"doctype": "Custom Event",
				"title": "_Test Event 4",
				"date": "2014-01-01",
				"start_time": "20:00:00",
				"end_time": "22:00:00",
			}).insert()
		res = frappe.get_list("Custom Event", filters=[
			["Custom Event", "title", "like", "_Test Event%"]], fields=["name", "title"])
		self.assertEqual(len(res), 3)
		titles = [r.title for r in res]
		self.assertFalse("_Test Event 4" in titles)

	def test_create_events_on_user_creation(self):
		doc = frappe.get_doc({
			"doctype": "User",
			"email": "test_1@swira.design",
			"first_name": "Test",
		}).insert()
		res = frappe.get_list("Custom Event", fields=["name", "title"])
		self.assertEqual(len(res), 5)
		titles = [r.title for r in res]
		self.assertTrue("Welcome Party for Test" in titles)

	def test_full_name_in_invitee(self):
		doc = frappe.get_doc({
			"doctype": "User",
			"email": "test_2@swira.design",
			"first_name": "TestFisrtName",
			"last_name": "TestLastName"
		}).insert()
		res = frappe.db.sql(
			'select full_name from `tabEvent Invitee` where parent = "welcome-party-for-testfisrtname"')
		self.assertEqual(len(res), 1)
		self.assertEqual(res[0][0], "TestFisrtName TestLastName")
