# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class receipt(models.Model):
    _name = 'lat.siswa.receipt'

    name = fields.Char(string="Receipt ID", required=True)
    lat_register_id = fields.Many2one(
        'lat.siswa.register',
        string='Register ID',
        required=True
    )
    lat_siswa = fields.Char(string="Name", required=True)
    lat_paiddate = fields.Date(
        string="Paid Date",
        default=fields.Date.today
    )
    lat_paidstatus = fields.Boolean()

    @api.model
    def create(self, vals):

        if vals.get('name', 'New') == 'New':
            reg = self.env['ir.sequence'].next_by_code('receipt.number')
            vals['name'] = reg or 'New'

        return super(receipt, self).create(vals)

    @api.multi
    def lat_action_paid_receipt(self):
        self.lat_register_id.lat_state = 'paid'
        self.lat_paidstatus = True
