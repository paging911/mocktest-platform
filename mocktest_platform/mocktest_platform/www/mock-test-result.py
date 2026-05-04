import frappe


def get_context(context):
    context.no_cache = 1
    attempt = frappe.form_dict.get("attempt")
    if not attempt:
        frappe.throw("Attempt is required.")

    context.result = frappe.call("mocktest_platform.api.get_result", attempt=attempt)
    return context

