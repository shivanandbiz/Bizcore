import frappe
 
def get_permission_query_conditions(user):
    if not user or user == "Administrator":
        return ""
 
    roles = frappe.get_roles(user)
    if "Projects Manager" in roles or "Delivery Manager" in roles:
        return ""  # Allow full access
 
    # Only show tasks assigned to the user
    return f"""EXISTS (
        SELECT 1 FROM `tabToDo`
        WHERE `tabToDo`.reference_type = 'Task'
        AND `tabToDo`.reference_name = `tabTask`.name
        AND `tabToDo`.allocated_to = '{user}'
    )"""
 
def has_permission(doc, ptype, user):
    if user == "Administrator":
        return True
 
    roles = frappe.get_roles(user)
    if "Projects Manager" in roles or "Delivery Manager" in roles:
        return True  # Full access
 
    # Only allow if task is assigned to the user
    return frappe.db.exists("ToDo", {
        "reference_type": "Task",
        "reference_name": doc.name,
        "allocated_to": user
    })
    