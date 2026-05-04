import frappe


def get_context(context):
    context.no_cache = 1
    context.exams = frappe.get_all(
        "MT Exam",
        filters={"status": "Published"},
        fields=[
            "name",
            "exam_title",
            "duration_minutes",
            "max_attempts",
            "passing_percentage",
            "course",
            "batch",
        ],
        order_by="modified desc",
    )
    return context
