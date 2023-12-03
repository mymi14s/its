import frappe


def get_student():
    if frappe.db.exists("Student", {'user':frappe.session.user}):
        return frappe.get_doc('Student',{'user':frappe.session.user})
    return None

@frappe.whitelist(allow_guest=1)
def is_authenticated():
    if frappe.session.user=='Guest':
        return False
    else:
        return True