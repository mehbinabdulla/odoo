from odoo import models, fields


class SurveyContact(models.Model):
    _name = 'survey.contact'
    _description = 'Survey Contact'

    question_id = fields.Many2one('survey.question', 'Question')
    partner_field = fields.Selection('_get_partner_fields', 'Contact')
    survey_id = fields.Many2one('survey.survey')

    def _get_partner_fields(self):
        _fields = self.env['res.partner'].fields_get()
        return [(k, v['string']) for k, v in _fields.items()]