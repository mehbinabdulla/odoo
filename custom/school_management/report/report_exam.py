# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools import SQL


class ReportExam(models.AbstractModel):
    """Report generation of exams"""
    _name = 'report.school_management.report_exam'
    _description = 'Leave Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Pass values to the PDF template"""
        student_ids = tuple(data.get('student_ids')) if len(data.get('student_ids')) != 1 else tuple(data.get('student_ids')) + (0, )
        class_ids = tuple(data.get('class_ids')) if len(data.get('class_ids')) != 1 else tuple(data.get('class_ids')) + (0, )

        print(class_ids)
        print(student_ids)

        self.env.cr.execute(SQL(f"""
            SELECT exam.id as id, exam.name as name, exam.class_id
            FROM school_exam as exam
            WHERE {  
                    f'exam.class_id IN (SELECT student.class_id FROM student WHERE student.id IN { student_ids })' if (student_ids and class_ids) or student_ids
                    else f'exam.class_id IN { class_ids }' if class_ids
                    else 'TRUE'
                }
            """))

        exams = self.env.cr.dictfetchall()
        for exam in exams:
            print(exam.get('name'))
            docids.append(exam.get('id'))

        if len(docids) > 0:
            return {
                'doc_ids': docids,
                'doc_model': 'school.exam',
                'docs': self.env['school.exam'].browse(docids),
                'data': data
            }
        else:
            raise ValidationError('No Record Found')
