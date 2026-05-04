import frappe
from frappe.model.document import Document


class MTExam(Document):
    def validate(self):
        if self.duration_minutes <= 0:
            frappe.throw("Duration must be greater than zero.")
        if self.max_attempts <= 0:
            frappe.throw("Maximum attempts must be greater than zero.")

