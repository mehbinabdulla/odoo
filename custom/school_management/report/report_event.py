# -*- coding: utf-8 -*-
from odoo import api, models
from datetime import date, timedelta
import calendar
from odoo.exceptions import ValidationError
from odoo.tools import SQL


class ReportEvent(models.AbstractModel):
    """Report generation of events"""
    _name = 'report.school_management.report_event'
    _description = 'Event Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Pass values to the PDF template"""
        duration = data.get('duration')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        club_ids = tuple(data.get('club_ids')) if len(data.get('club_ids')) != 1 else tuple(data.get('club_ids')) + (0, )
        today = date.today()
        month_start = today.replace(day = 1)
        month_end = today.replace(day = calendar.monthrange(today.year, today.month)[1])
        week_start = today - timedelta(days = today.weekday())
        week_end = today + timedelta(days = 6 - today.weekday())

        self.env.cr.execute(SQL(f"""
            SELECT id, club_id, date_begin, date_end
            FROM event_event
            WHERE ({
                    '%(today)s BETWEEN date_begin AND date_end' if duration == 'today'
                    else """(date_begin BETWEEN %(week_start)s AND %(week_end)s) 
                        OR (date_end BETWEEN %(week_start)s AND %(week_end)s)""" if duration == 'week'
                    else """(date_begin BETWEEN %(month_start)s AND %(month_end)s) 
                        OR (date_end BETWEEN %(month_start)s AND %(month_end)s)""" if duration == 'month'
                    else 'TRUE' if duration == 'custom' and not start_date and not end_date
                    else """(date_from <= %(end_date)s) 
                        OR (date_to <= %(end_date)s)""" if duration == 'custom' and not start_date
                    else """(date_from >= %(start_date)s) 
                        OR (date_to >= %(start_date)s)""" if duration == 'custom' and not end_date
                    else """(date_begin BETWEEN %(start_date)s AND %(end_date)s) 
                        OR (date_end BETWEEN %(start_date)s AND %(end_date)s)""" if duration == 'custom'
                    else 'TRUE' if duration == 'all'
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

        events = self.env.cr.dictfetchall()
        for event in events:
            docids.append(event.get('id'))

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
            'doc_model': 'event.event',
            'docs': self.env['event.event'].browse(docids),
            'data': data
            }
        else:
            raise ValidationError('No Record Found')
