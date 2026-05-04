import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class MTQuestion(Document):
    def autoname(self):
        self.name = make_autoname("MT-Q-.#####")

    def validate(self):
        if self.question_type == "Single Choice":
            correct_count = len([option for option in self.options if option.is_correct])
            if correct_count != 1:
                frappe.throw("Single choice questions must have exactly one correct option.")
