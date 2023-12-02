import frappe


def get_student():
    if frappe.db.exists("Student", {'user':frappe.session.user}):
        return frappe.get_doc('Student',{'user':frappe.session.user})
    return None