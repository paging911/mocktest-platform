import frappe
from frappe.model.document import Document


class MTQuestion(Document):
    def validate(self):
        if self.question_type == "Single Choice":
            correct_count = len([option for option in self.options if option.is_correct])
            if correct_count != 1:
                frappe.throw("Single choice questions must have exactly one correct option.")

