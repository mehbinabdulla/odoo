# -*- coding: utf-8 -*-
import io
from datetime import datetime
import xlsxwriter
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

        sheet.merge_range(f'A6:{'E7' if len(data.get('class_name')) != 1 else 'D7'}', 'EXAM REPORT', head)

        sheet.write('A1', self.env.company.name, txt)
        sheet.write('A2', self.env.company.street, txt)
        sheet.write('A3', self.env.company.city, txt)
        sheet.write('A4', self.env.company.state_id.name, txt)
        sheet.write('A5', self.env.company.country_id.name, txt)

        sheet.write('A9', 'Printing Date:', sub_head)
        sheet.write('B9', datetime.now().strftime('%Y-%m-%d'), txt)
        if len(data.get('class_name')) > 0:
            sheet.write('A10', 'Class:', sub_head)
            sheet.write('B10', ', '.join(data.get('class_name')), txt)
        if len(data.get('student_name')) > 0:
            sheet.write('A11', 'Students:', sub_head)
            sheet.write('B11', ', '.join(data.get('student_name')), txt)

        sheet.write('A13', 'Sl. No.', col_head)
        sheet.write('B13', 'Exam', col_head)
        if len(data.get('class_name')) != 1:
            sheet.write('C13', 'Class', col_head)
        sheet.write(f'{'D' if len(data.get('class_name')) != 1 else 'C'}13', 'Created On', col_head)
        sheet.write(f'{'E' if len(data.get('class_name')) != 1 else 'D'}13', 'State', col_head)

        for index, exam in enumerate(docs, start=14):
            order+=1
            sheet.write(f'A{index}',order, row_even if index % 2 == 0 else row_odd)
            sheet.write(f'B{index}', exam.name, row_even if index % 2 == 0 else row_odd)
            if len(data.get('class_name')) != 1:
                sheet.write(f'C{index}', exam.class_id.name, row_even if index % 2 == 0 else row_odd)
            sheet.write(f'{'D' if len(data.get('class_name')) != 1 else 'C'}{index}', exam.create_date.strftime('%Y-%m-%d'), row_even if index % 2 == 0 else row_odd)
            sheet.write(f'{'E' if len(data.get('class_name')) != 1 else 'D'}{index}', exam.state, row_even if index % 2 == 0 else row_odd)

        sheet.autofit()
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

