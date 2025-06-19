from odoo import models, fields, api
from odoo.exceptions import UserError


class SurveyContact(models.Model):
    _name = 'survey.contact'
    _parent_name = 'survey_id'
    _description = 'Survey Contact'


    question_id = fields.Many2one('survey.question', 'Question',
                                  domain="[('survey_id', '=', survey_id), ('id', 'not in', available_question_ids)]", required=True)
    partner_field = fields.Selection('_get_partner_fields', 'Contact', required=True)
    survey_id = fields.Many2one('survey.survey')
    available_question_ids = fields.Many2many('survey.question', compute='_compute_available_questions')

    def _get_partner_fields(self, used_fields=None):
        partner_fields = self.env['res.partner'].fields_get()
        all_fields = [(key, value['string']) for key, value in partner_fields.items()]
        _fields = [pair for pair in all_fields if pair[0] not in used_fields] if used_fields else all_fields
        return sorted(_fields, key=lambda x: x[1])

    @api.onchange('survey_id')
    def _compute_available_questions(self):
        for rec in self:
            if rec.survey_id:
                used_question_ids = rec.survey_id.survey_contact_ids.filtered(lambda r: r.id != rec.id).mapped('question_id.id')
                rec.available_question_ids = used_question_ids
                used_fields = rec.survey_id.survey_contact_ids.mapped('partner_field')
                rec.partner_field = [pair for pair in self._get_partner_fields() if pair[0] not in used_fields]
                # rec._get_partner_fields(used_fields)
