import frappe


def _route_value(key):
    if frappe.form_dict.get(key):
        return frappe.form_dict.get(key)

    path = frappe.local.request.path.strip("/").split("/")
    if len(path) >= 2:
        return path[1]

    return None


def get_context(context):
    context.no_cache = 1
    context.attempt = _route_value("attempt")
    if not context.attempt:
        frappe.throw("Attempt is required.")
    return context
