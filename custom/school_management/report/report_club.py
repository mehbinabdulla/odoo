# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools import SQL


class ReportClub(models.AbstractModel):
    """Report generation of clubs"""
    _name = 'report.school_management.report_club'
    _description = 'CLub Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Pass values to the PDF template"""
        student_ids = tuple(data.get('student_ids')) if len(data.get('student_ids')) != 1 else tuple(data.get('student_ids')) + (0, )
        club_ids = tuple(data.get('club_ids')) if len(data.get('club_ids')) != 1 else tuple(data.get('club_ids')) + (0, )

        self.env.cr.execute(SQL(f"""
            SELECT club.id as id, club.name as name
            FROM school_club as club
            WHERE {  
                    f'club.id IN { club_ids }' if club_ids
                    else f'club.id IN (SELECT school_club_id FROM school_club_student_rel WHERE student_id IN { student_ids })' if student_ids
                    else 'TRUE'
                }
            """))

        clubs = self.env.cr.dictfetchall()
        for club in clubs:
            docids.append(club.get('id'))

        if len(docids) > 0:
            return {
                'doc_ids': docids,
                'doc_model': 'school.club',
                'docs': self.env['school.club'].browse(docids),
                'data': data
            }
        else:
            raise ValidationError('No Record Found')
