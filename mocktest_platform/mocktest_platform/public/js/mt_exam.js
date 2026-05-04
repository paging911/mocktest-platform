frappe.ui.form.on("MT Exam", {
  refresh(frm) {
    if (!frm.is_new() && frm.doc.status !== "Published") {
      frm.add_custom_button(__("Publish"), () => {
        frm.set_value("status", "Published");
        frm.save();
      });
    }
  },
});

