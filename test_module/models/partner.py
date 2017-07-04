# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    hai = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('test_module.session', string="Attended Sessions", readonly=True)
