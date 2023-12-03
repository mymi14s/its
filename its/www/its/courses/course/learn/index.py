import frappe
from its.utils import get_student

# @frappe.whitelist(allow_guest=1)
def get_context(context):
    doc = frappe.get_doc("Educational Content", frappe.form_dict.name)
    context.title = "Learn " + doc.content_name
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
    context.student = student
    return context

@frappe.whitelist()
def take_assessment():
    enrollment = frappe.get_doc("Course Enrollment", frappe.form_dict.enrollment)
    student = get_student()
    if frappe.db.exists("Assessment", {
        "student":student.name, 
        "educational_content":enrollment.educational_content,
        "category":"Assignment",
        "grade":"Pass",
        "course_enrollment":enrollment.name}
        ):
        return {
            "status":False, 
            "text":f"You have submitted and passed the assessment for <b>{enrollment.educational_content}</b>"
        }
    else:
        try:
            frappe.get_doc({
                "doctype":"Assessment",
                "student":student.name,
                "educational_content":enrollment.educational_content,
                "category":"Assignment",
                "grade":"Pass",
                "course_enrollment":enrollment.name
            }).insert(ignore_permissions=1)
            frappe.db.set_value("Course Enrollment", enrollment.name, "status", "Completed")
            return {
                "status": True,
                "link": f"/its/courses/{enrollment.educational_content}/learn"
            }
        except Exception as e:
            return {
            "status":False, 
            "text":e
        }

@frappe.whitelist()
def create_feedback():
    data = {
        'doctype':'Feedback',
        'course_enrollment':frappe.form_dict.enrollment,
        'type':frappe.form_dict.category,
        'comment':frappe.form_dict.comment
    }
    feedback = frappe.get_doc(data).insert(ignore_permissions=1)
    return {"status":True}