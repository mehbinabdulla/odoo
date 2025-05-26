import io
from datetime import datetime

import xlsxwriter
from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools import SQL


class ReportStudent(models.AbstractModel):
    """Pass data to the report template"""
    _name = 'report.school_management.report_student'
    _description = 'Student Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get report values from Query."""
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
        """Pass values to XLSX sheet"""
        record = self._get_report_values([], data)
        docs = record.get('docs')
        order = 0
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px', 'color':'#714B67'})
        sub_head = workbook.add_format(
            {'font_size': '11px', 'align': 'vcenter', 'color': '#987000'})
        col_head = workbook.add_format(
            {'font_size': '11px', 'bold': True, 'align': 'vcenter', 'bg_color':'#e4d7e1'})
        txt = workbook.add_format(
            {'font_size': '11px', 'align': 'vcenter'})
        row_even = workbook.add_format(
            {'font_size': '11px', 'bg_color':'#f4eef2', 'align': 'left'})
        row_odd = workbook.add_format(
            {'font_size': '11px', 'bg_color':'#ffffff', 'align': 'left'})

        sheet.merge_range(f'A6:{'F7' if len(data.get('class_name')) != 1 else 'E7'}', 'STUDENT REPORT', head)

        sheet.write('A1', self.env.company.name, txt)
        sheet.write('A2', self.env.company.street, txt)
        sheet.write('A3', self.env.company.city, txt)
        sheet.write('A4', self.env.company.state_id.name, txt)
        sheet.write('A5', self.env.company.country_id.name, txt)

        sheet.write('A9', 'Printing Date:', sub_head)
        sheet.write('B9', datetime.now().strftime('%Y-%m-%d'), txt)
        if len(data.get('department_name')) > 0:
            sheet.write('A10', 'Departments:', sub_head)
            sheet.write('B10', ', '.join(data.get('department_name')), txt)
        if len(data.get('class_name')) > 0:
            sheet.write('A11', 'Class:', sub_head)
            sheet.write('B11', ', '.join(data.get('class_name')), txt)

        sheet.write('A13', 'Sl. No.', col_head)
        sheet.write('B13', 'Registration ID', col_head)
        sheet.write('C13', 'Name', col_head)
        if len(data.get('class_name')) != 1:
            sheet.write('D13', 'Class', col_head)
        sheet.write(f'{'E' if len(data.get('class_name')) != 1 else 'D'}13', 'Email', col_head)
        sheet.write(f'{'F' if len(data.get('class_name')) != 1 else 'E'}13', 'Mobile', col_head)

        for index, student in enumerate(docs, start=14):
            order+=1
            sheet.write(f'A{index}',order, row_even if index % 2 == 0 else row_odd)
            sheet.write(f'B{index}', student.reg_id, row_even if index % 2 == 0 else row_odd)
            sheet.write(f'C{index}', student.name, row_even if index % 2 == 0 else row_odd)
            if len(data.get('class_name')) != 1:
                sheet.write(f'D{index}', student.class_id.name, row_even if index % 2 == 0 else row_odd)
            sheet.write(f'{'E' if len(data.get('class_name')) != 1 else 'D'}{index}', student.email, row_even if index % 2 == 0 else row_odd)
            sheet.write(f'{'F' if len(data.get('class_name')) != 1 else 'E'}{index}', student.mobile, row_even if index % 2 == 0 else row_odd)

        sheet.autofit()
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
