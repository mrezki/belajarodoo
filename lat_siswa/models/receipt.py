# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class receipt(models.Model):
    _name = 'lat.siswa.receipt'

    name = fields.Char(string="Receipt ID", required=True)
    lat_register_id = fields.Many2one('lat.siswa.register',
        string="Register ID", required=True)
    lat_siswa = fields.Char(string="Name", required=True)
    lat_paiddate = fields.Date(
        string="Paid Date",
        default=fields.Date.today
    )
    lat_paidstatus = fields.Boolean()

    @api.multi
    def lat_action_paid_receipt(self):
        self.lat_register_id.lat_state = 'paid'
        self.lat_paidstatus = True
