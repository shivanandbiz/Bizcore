#testing task doctype
import frappe


def get_permission_query_conditions(user):
    """
    Restrict Task records based on user permissions.
    """
    if not user:
        user = frappe.session.user

    # System Manager should see all Tasks
    if "System Manager" in frappe.get_roles(user):
        return ""

    # Example: allow only tasks assigned to the user
    return f"""
        `tabTask`.name IN (
            SELECT reference_name
            FROM `tabToDo`
            WHERE owner = '{user}'
              AND reference_type = 'Task'
        )
    """


def has_permission(doc, user):
    """
    Row-level permission check for Task.
    """
    if not user:
        user = frappe.session.user

    # System Manager full access
    if "System Manager" in frappe.get_roles(user):
        return True

    # Allow if task is assigned to user
    assigned_users = frappe.get_all(
        "ToDo",
        filters={
            "reference_type": "Task",
            "reference_name": doc.name,
            "owner": user,
        },
        limit=1,
    )

    return bool(assigned_users)
