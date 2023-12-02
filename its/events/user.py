import frappe

def before_insert(doc, event):
    doc.role_profile_name = "Student"

def after_insert(doc, event):
    """
        Create student account on user creation
    """
    student = frappe.get_doc({
        "doctype":"Student",
        "user":doc.name
    }).insert(ignore_permissions=1)