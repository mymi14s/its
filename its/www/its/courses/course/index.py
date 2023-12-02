import frappe
from its.utils import get_student

# @frappe.whitelist(allow_guest=1)
def get_context(context):
    doc = frappe.get_doc("Educational Content", frappe.form_dict.name)
    context.title = frappe.form_dict.name
    context.course = doc
    student = get_student()
    enrollment = frappe.db.get_value("Course Enrollment", {
        "student":student.name,
        "educational_content":doc.name,
        },
        ["name", "status", "educational_content"],
        as_dict=1
    )
    context.enrollment = enrollment
    return context

@frappe.whitelist()
def enroll():
    educational_content = frappe.form_dict.educational_content
    student = get_student()
    if frappe.db.exists("Course Enrollment", {
        "student":student.name, 
        "educational_content":educational_content}
        ):
        return {
            "status":False, 
            "text":f"You have already enrolled for this course <b>{educational_content}</b>"
        }
    else:
        try:
            frappe.get_doc({
                "doctype":"Course Enrollment",
                "student":student.name,
                "educational_content":educational_content,
                "status":"In Progress"
            }).insert(ignore_permissions=1)
            return {
                "status": True,
                "link": f"/its/courses/{educational_content}/learn"
            }
        except Exception as e:
            return {
            "status":False, 
            "text":e
        }