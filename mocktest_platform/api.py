import frappe
from frappe import _
from frappe.utils import now_datetime


def _get_exam_or_throw(exam_name):
    exam = frappe.get_doc("MT Exam", exam_name)
    if exam.status != "Published":
        frappe.throw(_("This exam is not published yet."))
    return exam


def _get_attempt_or_throw(attempt_name):
    attempt = frappe.get_doc("MT Exam Attempt", attempt_name)
    if attempt.student != frappe.session.user:
        frappe.throw(_("You are not allowed to access this attempt."))
    return attempt


@frappe.whitelist()
def start_attempt(exam):
    """Create a new attempt for the logged-in user."""
    exam_doc = _get_exam_or_throw(exam)

    existing_count = frappe.db.count(
        "MT Exam Attempt",
        {
            "exam": exam_doc.name,
            "student": frappe.session.user,
            "status": ["in", ["In Progress", "Submitted"]],
        },
    )

    if exam_doc.max_attempts and existing_count >= exam_doc.max_attempts:
        frappe.throw(_("Maximum attempt limit reached."))

    attempt = frappe.new_doc("MT Exam Attempt")
    attempt.exam = exam_doc.name
    attempt.student = frappe.session.user
    attempt.started_at = now_datetime()
    attempt.status = "In Progress"
    attempt.duration_minutes = exam_doc.duration_minutes

    for exam_question in exam_doc.questions:
        question = frappe.get_doc("MT Question", exam_question.question)
        attempt.append(
            "answers",
            {
                "question": question.name,
                "section": exam_question.section,
                "marks": exam_question.marks or question.default_marks,
                "negative_marks": exam_question.negative_marks or question.negative_marks,
                "status": "Not Answered",
            },
        )

    attempt.insert(ignore_permissions=False)
    return attempt.name


@frappe.whitelist()
def get_attempt(attempt):
    """Return attempt data for rendering the test screen."""
    attempt_doc = _get_attempt_or_throw(attempt)
    exam_doc = frappe.get_doc("MT Exam", attempt_doc.exam)

    questions = []
    for answer in attempt_doc.answers:
        question = frappe.get_doc("MT Question", answer.question)
        questions.append(
            {
                "answer_row": answer.name,
                "question": question.name,
                "section": answer.section,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "selected_option": answer.selected_option,
                "marked_for_review": answer.marked_for_review,
                "status": answer.status,
                "options": [
                    {
                        "option_id": option.name,
                        "label": option.option_label,
                        "text": option.option_text,
                    }
                    for option in question.options
                ],
            }
        )

    return {
        "attempt": attempt_doc.name,
        "exam": exam_doc.name,
        "title": exam_doc.exam_title,
        "duration_minutes": attempt_doc.duration_minutes,
        "started_at": attempt_doc.started_at,
        "status": attempt_doc.status,
        "questions": questions,
    }


@frappe.whitelist()
def save_answer(attempt, answer_row, selected_option=None, marked_for_review=0):
    """Save one answer row while the exam is in progress."""
    attempt_doc = _get_attempt_or_throw(attempt)
    if attempt_doc.status != "In Progress":
        frappe.throw(_("This attempt is already submitted."))

    row = next((item for item in attempt_doc.answers if item.name == answer_row), None)
    if not row:
        frappe.throw(_("Answer row not found."))

    row.selected_option = selected_option
    row.marked_for_review = int(marked_for_review or 0)

    if selected_option:
        row.status = "Marked for Review" if row.marked_for_review else "Answered"
    else:
        row.status = "Marked for Review" if row.marked_for_review else "Not Answered"

    attempt_doc.save(ignore_permissions=False)
    return {"ok": True, "status": row.status}


@frappe.whitelist()
def submit_attempt(attempt):
    """Evaluate and submit an attempt."""
    attempt_doc = _get_attempt_or_throw(attempt)
    if attempt_doc.status == "Submitted":
        return _result_payload(attempt_doc)

    if attempt_doc.status != "In Progress":
        frappe.throw(_("Attempt cannot be submitted."))

    total_score = 0
    max_score = 0
    correct_count = 0
    wrong_count = 0
    skipped_count = 0

    for answer in attempt_doc.answers:
        question = frappe.get_doc("MT Question", answer.question)
        correct_option = next((option for option in question.options if option.is_correct), None)

        marks = answer.marks or question.default_marks or 0
        negative_marks = answer.negative_marks or question.negative_marks or 0
        max_score += marks

        if not answer.selected_option:
            answer.is_correct = 0
            answer.score = 0
            answer.status = "Skipped"
            skipped_count += 1
            continue

        if correct_option and answer.selected_option == correct_option.name:
            answer.is_correct = 1
            answer.score = marks
            answer.status = "Correct"
            total_score += marks
            correct_count += 1
        else:
            answer.is_correct = 0
            answer.score = -negative_marks
            answer.status = "Wrong"
            total_score -= negative_marks
            wrong_count += 1

    attempt_doc.total_score = total_score
    attempt_doc.max_score = max_score
    attempt_doc.percentage = (total_score / max_score * 100) if max_score else 0
    attempt_doc.correct_count = correct_count
    attempt_doc.wrong_count = wrong_count
    attempt_doc.skipped_count = skipped_count
    attempt_doc.submitted_at = now_datetime()
    attempt_doc.status = "Submitted"
    attempt_doc.save(ignore_permissions=False)

    return _result_payload(attempt_doc)


@frappe.whitelist()
def get_result(attempt):
    attempt_doc = _get_attempt_or_throw(attempt)
    if attempt_doc.status != "Submitted":
        frappe.throw(_("Result is available after submission."))
    return _result_payload(attempt_doc)


def _result_payload(attempt_doc):
    return {
        "attempt": attempt_doc.name,
        "exam": attempt_doc.exam,
        "student": attempt_doc.student,
        "total_score": attempt_doc.total_score,
        "max_score": attempt_doc.max_score,
        "percentage": attempt_doc.percentage,
        "correct_count": attempt_doc.correct_count,
        "wrong_count": attempt_doc.wrong_count,
        "skipped_count": attempt_doc.skipped_count,
        "status": attempt_doc.status,
    }

