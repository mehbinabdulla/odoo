# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SurveyUserInput(models.Model):
    """ Metadata for a set of one user's answers to a particular survey """
