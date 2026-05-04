import frappe


def get_context(context):
    context.no_cache = 1
    context.attempt = frappe.form_dict.get("attempt")
    if not context.attempt:
        frappe.throw("Attempt is required.")
    return context

