# Copyright (c) 2023, Anthony Emmanuel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CourseEnrollment(Document):
	def validate(self):
		education_content = frappe.get_doc("Educational Content", self.educational_content)
		if education_content.prerequisite:
			# check if student had successfully enrolled and completed requirement
			completed_courses_enrolled = [i.educational_content for i in frappe.db.get_list("Course Enrollment", filters={
				'student':self.student, 'educational_content': ["!=", self.educational_content],
				"status": "Completed"},
				fields=["educational_content"]
			)]
			progress_courses_enrolled = [i.educational_content for i in frappe.db.get_list("Course Enrollment", filters={
				'student':self.student, 'educational_content': ["!=", self.educational_content],
				"status": "In Progress"},
				fields=["educational_content"]
			)]
			
			not_taken = []
			completed = []
			in_progress = []
			prerequisite_courses = """"""
			for i in education_content.prerequisite:
				prerequisite_courses += f"""{i.educational_content}</br>"""
				if i.educational_content in completed_courses_enrolled:
					completed.append(i.educational_content)
				elif i.educational_content in progress_courses_enrolled:
					in_progress.append(i.educational_content)
				else:
					not_taken.append(i.educational_content)
			message = """<b>The following prerequisite(s) are required before enrolling to this course.</b><hr>"""
			message += prerequisite_courses
			message += """<hr>"""
			
			if (not_taken or in_progress):
				if not_taken:
					message += """<b>You have not enrolled in the following:</b><br>"""
					for i in not_taken:
						message += f"""<a href="/its/courses/{i}">{i}<a></br>"""
				if in_progress:
					message += """<b><hr>You have enrolled in the following but yet to complete:<br></b>"""
					for i in in_progress:
						message += f"""<a href="/its/courses/{i}">{i}<a></br>"""
				if completed:
					message += """<b><hr>You have completed the following:</b><br>"""
					for i in completed:
						message += f"""<a href="/its/courses/{i}">{i}<a></br>"""

				frappe.throw(message)
				

