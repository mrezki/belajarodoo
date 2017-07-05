# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    lat_sex = fields.Selection([
        ('male', "Male"),
        ('female', "Female"),
    ], string="Sex")

    lat_name = fields.Char(string="Name")
    lat_description = fields.Text(string="Description")

    _sql_constraints = [
        ('name_parent_uniq', 'unique(name)', 'The name and the company must be unique !')
    ]
 
