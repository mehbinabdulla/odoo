from odoo import models


class SchoolManagementReport(models.Model):
    _name = 'school.management.report'
    _description = 'School Management Report'

    def print_student_report(self, department_id, class_id):
        domain = [('class_id', '=', class_id.id)] if class_id else [('dept_id', '=', department_id.id)]
        docs = self.env['student'].search([])
        docids = docs.ids
        print(docids)
        return self.env.ref('school_management.action_report_student_template').report_action(docids)