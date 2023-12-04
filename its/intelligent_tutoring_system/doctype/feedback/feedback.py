# Copyright (c) 2023, Anthony Emmanuel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Feedback(Document):
	def before_insert(self):
		if not self.student:
			student = frappe.get_doc("Student", frappe.db.get_value("Course Enrollment", {
				'name':self.course_enrollment
			}, field="student"))
			self.student = student
