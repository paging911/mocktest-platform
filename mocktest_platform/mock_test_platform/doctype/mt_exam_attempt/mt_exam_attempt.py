import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import add_to_date, now_datetime


class MTExamAttempt(Document):
    def autoname(self):
        self.name = make_autoname("MT-ATT-.#####")

    def validate(self):
        if self.status == "In Progress" and self.started_at and self.duration_minutes:
            ends_at = add_to_date(self.started_at, minutes=self.duration_minutes)
            if now_datetime() > ends_at:
                self.status = "Time Expired"

        if self.status == "Submitted" and self.max_score:
            self.percentage = (self.total_score / self.max_score) * 100

    def before_save(self):
        if self.status == "Submitted" and not self.submitted_at:
            self.submitted_at = now_datetime()
