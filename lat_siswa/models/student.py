# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from odoo import models, fields, api, exceptions, _

import logging

_logger = logging.getLogger(__name__)


class student(models.Model):
    _name = 'lat.siswa.student'

    name = fields.Char(string="Student ID", required=True)
    lat_register_id = fields.Many2one('lat.siswa.register',
        string="Register ID", required=True)
    lat_siswa = fields.Char(string="Name", required=True)
    lat_regiterdate = fields.Date(
        string="Register Date",
        default=fields.Date.today
    )
    lat_birthdate = fields.Date(
        string="Birth Date"
    )
    lat_sex = fields.Selection([
        ('male', "Male"),
        ('female', "Female"),
    ], string="Sex")
    