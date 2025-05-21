from odoo import api, models
from odoo.tools import SQL


class ReportStudent(models.AbstractModel):
    _name = 'report.school_management.report_student'
    _description = 'Student Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """ Endpoint for PDF display. """
        department_ids = tuple(data.get('department_ids')) if len(data.get('department_ids')) != 1 else tuple(data.get('department_ids')) + (0, )
        class_ids = tuple(data.get('class_ids')) if len(data.get('class_ids')) != 1 else tuple(data.get('class_ids')) + (0, )

        print(data)

        self.env.cr.execute(SQL(f"""
        SELECT student.id as id, student.name as name, student.email as email,
                student.mobile as mobile, student.reg_id as reg_id,
                student.class_id as class_id, student.dept_id as dept_id
            FROM student
            WHERE 
                {f'dept_id IN { department_ids } AND  class_id IN { class_ids }' if class_ids and department_ids 
                    else f'dept_id IN { department_ids }' if department_ids
                    else f'class_id IN { class_ids }' if class_ids 
                    else 'TRUE'
                }
        """, class_id = class_ids, department_id = department_ids))
        students = self.env.cr.dictfetchall()
        for student in students:
            print(student)
            docids.append(student.get('id'))

        return {
            'doc_ids': docids,
            'doc_model': 'student',
            'docs': self.env['student'].browse(docids),
            'data': data
        }
