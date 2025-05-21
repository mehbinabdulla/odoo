from odoo import api, models
from datetime import date, timedelta
import calendar
from odoo.tools import SQL


class ReportLeave(models.AbstractModel):
    _name = 'report.school_management.report_leave'
    _description = 'Leave Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """ Endpoint for PDF display. """
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

        print(class_ids)
        print(student_ids)

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
                    else """(date_from BETWEEN %(start_date)s AND %(end_date)s) 
                        OR (date_to BETWEEN %(start_date)s AND %(end_date)s)""" if duration == 'custom'
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
            print(leave)
            docids.append(leave.get('id'))

        if duration == 'today':
            data.update({'duration': today})
        elif duration == 'week':
            data.update({'duration': f'{week_start} to {week_end}'})
        elif duration == 'month':
            data.update({'duration': f'{month_start} to {month_end}'})
        elif duration == 'custom':
            data.update({'duration': f'{start_date} to {end_date}'})

        return {
            'doc_ids': docids,
            'doc_model': 'student.leave',
            'docs': self.env['student.leave'].browse(docids),
            'data': data
        }
