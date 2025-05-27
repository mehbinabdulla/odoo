# -*- coding: utf-8 -*-
import io
import xlsxwriter
from odoo import api, models
from datetime import date, timedelta, datetime
import calendar
from odoo.exceptions import ValidationError
from odoo.tools import SQL


class ReportLeave(models.AbstractModel):
    """Report generation of leave"""
    _name = 'report.school_management.report_leave'
    _description = 'Leave Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Pass values to the PDF template"""
        duration = data.get('duration')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        student_ids = tuple(data.get('student_ids')) if len(data.get('student_ids')) != 1 else tuple(data.get('student_ids')) + (0, )
        class_ids = tuple(data.get('class_ids')) if len(data.get('class_ids')) != 1 else tuple(data.get('class_ids')) + (0, )
        today = date.today()
        month_start = today.replace(day = 1)
        month_end = today.replace(day = calendar.monthrange(today.year, today.month)[1])
        week_start = today - timedelta(days = today.weekday())
        week_end = today + timedelta(days = 6 - today.weekday())

        self.env.cr.execute(SQL(f"""
            SELECT id, student_id, class_id,
                date_from, date_to, is_half_day, half_day
            FROM student_leave
            WHERE ({
                    '%(today)s BETWEEN date_from AND date_to' if duration == 'today'
                    else """(date_from BETWEEN %(week_start)s AND %(week_end)s) 
                        OR (date_to BETWEEN %(week_start)s AND %(week_end)s)""" if duration == 'week'
                    else """(date_from BETWEEN %(month_start)s AND %(month_end)s) 
                        OR (date_to BETWEEN %(month_start)s AND %(month_end)s)""" if duration == 'month'
                    else 'TRUE' if duration == 'custom' and not start_date and not end_date
                    else """(date_from <= %(end_date)s) 
                        OR (date_to <= %(end_date)s)""" if duration == 'custom' and not start_date
                    else """(date_from >= %(start_date)s) 
                        OR (date_to >= %(start_date)s)""" if duration == 'custom' and not end_date
                    else """(date_from BETWEEN %(start_date)s AND %(end_date)s) 
                        OR (date_to BETWEEN %(start_date)s AND %(end_date)s)""" if duration == 'custom'
                    else 'TRUE' if duration == 'all'
                    else 'FALSE'
                }) AND ({   
                    f'student_id IN { student_ids } AND  class_id IN { class_ids }' if class_ids and student_ids
                    else f'class_id IN { class_ids }' if class_ids
                    else f'student_id IN { student_ids }' if student_ids
                    else 'TRUE'
                })
            """, today=today,
                 month_start=month_start, month_end=month_end,
                 week_start=week_start, week_end=week_end,
                 start_date=start_date, end_date=end_date
        ))

        leaves = self.env.cr.dictfetchall()
        for leave in leaves:
            docids.append(leave.get('id'))

        if duration == 'today':
            data.update({'duration': today})
        elif duration == 'week':
            data.update({'duration': f'{week_start} to {week_end}'})
        elif duration == 'month':
            data.update({'duration': f'{month_start} to {month_end}'})
        elif duration == 'custom':
            data.update({'duration': f'{start_date if start_date else 'All'} to {end_date if end_date else 'All'}'})
        elif duration == 'all':
            data.update({'duration': 'All'})

        if len(docids) > 0:
            return {
                'doc_ids': docids,
                'doc_model': 'student.leave',
                'docs': self.env['student.leave'].browse(docids),
                'data': data
            }
        else:
            raise ValidationError('No Record Found')

    def  get_xlsx_report(self, data, response):
        """To pass values to the XLSX sheet"""
        record = self._get_report_values([], data)
        docs = record.get('docs')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px', 'color': '#714B67'})
        sub_head = workbook.add_format(
            {'font_size': '11px', 'align': 'vcenter', 'color': '#987000'})
        col_head = workbook.add_format(
            {'font_size': '11px', 'bold': True, 'align': 'vcenter', 'bg_color': '#e4d7e1'})
        txt = workbook.add_format(
            {'font_size': '11px', 'align': 'vcenter'})
        row_even = workbook.add_format(
            {'font_size': '11px', 'bg_color': '#f4eef2', 'align': 'left'})
        row_odd = workbook.add_format(
            {'font_size': '11px', 'bg_color': '#ffffff', 'align': 'left'})
        class_head = workbook.add_format(
            {'font_size': '12px', 'bold': True, 'align': 'vcenter', 'color': '#987000'})

        sheet.merge_range(f'A6:{'G7' if len(data.get('class_name')) != 1 else 'E7'}', 'LEAVE REPORT', head)

        sheet.write('A1', self.env.company.name, txt)
        sheet.write('A2', self.env.company.street, txt)
        sheet.write('A3', self.env.company.city, txt)
        sheet.write('A4', self.env.company.state_id.name, txt)
        sheet.write('A5', self.env.company.country_id.name, txt)

        sheet.write('A9', 'Printing Date:', sub_head)
        sheet.write('B9', datetime.now().strftime('%Y-%m-%d'), txt)
        if len(set(docs.student_id)) == 1:
            sheet.write('A10', 'Student', sub_head)
            sheet.write('B10', docs.student_id.name, txt)
            sheet.write('A11', 'Registration ID', sub_head)
            sheet.write('B11', docs.student_id.reg_id, txt)
            sheet.write('A12', 'Class', sub_head)
            sheet.write('B12', docs.class_id.name, txt)
        index = 12 if len(set(docs.student_id)) == 1 else 9
        for class_id in set(docs.class_id):
            order = 0
            index += 3
            if len(set(docs.student_id)) != 1:
                sheet.write(f'A{index}', class_id.name, class_head)
                index += 1
            sheet.write(f'A{index}', 'Sl. No.', col_head)
            if len(set(docs.student_id)) != 1:
                sheet.write(f'B{index}', 'Registration ID', col_head)
                sheet.write(f'C{index}', 'Name', col_head)
            sheet.write(f'{'D' if len(set(docs.student_id)) != 1 else 'B'}{index}', 'No. of Days', col_head)
            sheet.write(f'{'E' if len(set(docs.student_id)) != 1 else 'C'}{index}', 'Start Date', col_head)
            sheet.write(f'{'F' if len(set(docs.student_id)) != 1 else 'D'}{index}', 'End Date', col_head)
            sheet.write(f'{'G' if len(set(docs.student_id)) != 1 else 'E'}{index}', 'Type', col_head)
            for leave in docs:
                if leave.class_id == class_id:
                    index+=1
                    order+=1
                    sheet.write(f'A{index}', order, row_even if index % 2 == 0 else row_odd)
                    if len(set(docs.student_id)) != 1:
                        sheet.write(f'B{index}', leave.student_id.reg_id, row_even if index % 2 == 0 else row_odd)
                        sheet.write(f'C{index}', leave.student_id.name, row_even if index % 2 == 0 else row_odd)
                    sheet.write(f'{'D' if len(set(docs.student_id)) != 1 else 'B'}{index}',
                                leave.number_of_days, row_even if index % 2 == 0 else row_odd)
                    sheet.write(f'{'E' if len(set(docs.student_id)) != 1 else 'C'}{index}',
                                leave.date_from.strftime('%Y-%m-%d'), row_even if index % 2 == 0 else row_odd)
                    sheet.write(f'{'F' if len(set(docs.student_id)) != 1 else 'D'}{index}',
                                leave.date_to.strftime('%Y-%m-%d'), row_even if index % 2 == 0 else row_odd)
                    if leave.is_half_day:
                        sheet.write(f'{'G' if len(set(docs.student_id)) != 1 else 'E'}{index}',
                                    f'Half Day ({leave.half_day})', row_even if index % 2 == 0 else row_odd)
                    else:
                        sheet.write(f'{'G' if len(set(docs.student_id)) != 1 else 'E'}{index}',
                                    'Full Day', row_even if index % 2 == 0 else row_odd)
        sheet.autofit()
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
