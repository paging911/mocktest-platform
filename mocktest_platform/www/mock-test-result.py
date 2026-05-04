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
    attempt = _route_value("attempt")
    if not attempt:
        frappe.throw("Attempt is required.")

    context.result = frappe.call("mocktest_platform.api.get_result", attempt=attempt)
    return context
