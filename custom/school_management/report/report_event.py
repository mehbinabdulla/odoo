from odoo import api, models
from datetime import date, timedelta
import calendar
from odoo.tools import SQL


class ReportEvent(models.AbstractModel):
    _name = 'report.school_management.report_event'
    _description = 'Leave Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """ Endpoint for PDF display. """
        duration = data.get('duration')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        club_ids = tuple(data.get('club_ids')) if len(data.get('club_ids')) != 1 else tuple(data.get('club_ids')) + (0, )
        today = date.today()
        month_start = today.replace(day = 1)
        month_end = today.replace(day = calendar.monthrange(today.year, today.month)[1])
        week_start = today - timedelta(days = today.weekday())
        week_end = today + timedelta(days = 6 - today.weekday())

        print(club_ids)

        self.env.cr.execute(SQL(f"""
            SELECT id, club_id, # need more field.....
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
                    f'club_id IN { club_ids }' if club_ids
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
