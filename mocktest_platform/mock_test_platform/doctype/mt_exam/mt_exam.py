import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class MTExam(Document):
    def autoname(self):
        self.name = make_autoname("MT-EXAM-.#####")

    def validate(self):
        if self.duration_minutes <= 0:
            frappe.throw("Duration must be greater than zero.")
        if self.max_attempts <= 0:
            frappe.throw("Maximum attempts must be greater than zero.")
