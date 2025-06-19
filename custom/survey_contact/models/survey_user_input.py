# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SurveyUserInput(models.Model):
    """ Metadata for a set of one user's answers to a particular survey """
    _inherit = 'survey.user_input'

    contact_creation_id = fields.Many2one('res.partner')

class SurveyUserInputLine(models.Model):
    """ Metadata for a set of one user's answers to a particular survey """
    _inherit = 'survey.user_input.line'

    @api.model_create_multi
    def create(self, vals_list):
        new_lines = []
        for vals in vals_list:
            print(vals_list)
            user_input = self.env['survey.user_input'].browse(vals.get('user_input_id'))
            survey = user_input.survey_id
            survey_contact_ids = survey.survey_contact_ids
            contact = user_input.contact_creation_id

            question_id = vals.get('question_id')
            answer_type = vals.get('answer_type')
            answer_field = f'value_{answer_type}'
            answer = vals.get(answer_field)

            for survey_contact_id in survey_contact_ids:
                if survey_contact_id.question_id.id == question_id:
                    if contact:
                        contact.write({survey_contact_id.partner_field: answer})
                    else:
                        if survey_contact_id.partner_field == 'name' and answer:
                            new_contact = self.env['res.partner'].create({'name': answer})
                            user_input.contact_creation_id = new_contact.id
        return super(SurveyUserInputLine, self).create(vals_list)