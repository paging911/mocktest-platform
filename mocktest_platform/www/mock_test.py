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
    exam_name = _route_value("exam")
    if not exam_name:
        frappe.throw("Exam is required.")

    context.exam = frappe.get_doc("MT Exam", exam_name)
    if context.exam.status != "Published":
        frappe.throw("This exam is not published yet.")

    context.question_count = len(context.exam.questions)
    context.max_score = sum((row.marks or 0) for row in context.exam.questions)
    context.previous_attempts = frappe.get_all(
        "MT Exam Attempt",
        filters={
            "exam": context.exam.name,
            "student": frappe.session.user,
        },
        fields=["name", "status", "total_score", "max_score", "percentage", "modified"],
        order_by="creation desc",
    )

    return context

