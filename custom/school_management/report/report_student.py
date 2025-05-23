import io
from datetime import datetime

import xlsxwriter
from odoo import api, models
from odoo.exceptions import ValidationError
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

        if len(docids) > 0:
            return {
                'doc_ids': docids,
                'doc_model': 'student',
                'docs': self.env['student'].browse(docids),
                'data': data
            }
        else:
            raise ValidationError('No Record Found')

    def get_xlsx_report(self, data, response):
        record = self._get_report_values([], data)
        print(record)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        print(sheet)
        cell_format = workbook.add_format(
            {'font_size': '12px', 'bold': True, 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px', 'color':'#714B67'})
        txt = workbook.add_format({'font_size': '12px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'STUDENT REPORT', head)
        sheet.merge_range('B4:C4', 'Printing Date:', cell_format)
        sheet.merge_range('B5:C5', datetime.now().strftime('%Y-%m-%d'), txt)
        if len(data.get('department_name')) > 0:
            sheet.merge_range('D4:E4', 'Departments', cell_format)
            sheet.merge_range('D5:E5', ', '.join(data.get('department_name')), txt)
        if len(data.get('class_name')) > 0:
            sheet.merge_range('F4:G4', 'Classes', cell_format)
            sheet.merge_range('F5:G5', ', '.join(data.get('class_name')), txt)
        workbook.close()
        print('close')
        output.seek(0)
        response.stream.write(output.read())
        output.close()