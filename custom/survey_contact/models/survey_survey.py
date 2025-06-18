
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    survey_contact_ids = fields.One2many('survey.contact', 'survey_id')
