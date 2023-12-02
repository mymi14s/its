import frappe
from its.utils import get_student

# @frappe.whitelist(allow_guest=1)
def get_context(context):
    context.title = "Courses"
    context.courses = frappe.get_all("Educational Content", fields="*")
    return context