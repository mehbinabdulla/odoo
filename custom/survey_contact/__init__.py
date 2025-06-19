from . import models

def create_partner_fields(env):
    env['res.partner.field.helper'].create_records()