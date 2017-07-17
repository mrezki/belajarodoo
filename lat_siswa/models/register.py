# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)


class register(models.Model):
    _name = 'lat.siswa.register'

    name = fields.Char(
        string='Number',
        required=True,
        copy=False
    )
    lat_siswa = fields.Char(string="Name", required=True)
    lat_regiterdate = fields.Date(
        string='Register Date',
        default=fields.Date.today
    )
    lat_birthdate = fields.Date(
        string='Birth Date',
    )
    lat_sex = fields.Selection([
        ('male', "Male"),
        ('female', "Female"),
    ], string="Sex")
    lat_create_receipt = fields.Boolean(string='Create Status')
    lat_state = fields.Selection(
        [('new', 'New'), ('paid', 'Paid')],
        string='Status',
        required=True,
        readonly=True,
        copy=False, default='new')

    @api.model
    def create(self, vals):

        if vals.get('name', 'New') == 'New':
            reg = self.env['ir.sequence'].next_by_code('register.number')
            vals['name'] = reg or 'New'

        return super(register, self).create(vals)

    @api.multi
    def lat_action_create_receipt(self):
        reg = [('lat_register_id', '=', self.id)]
        lat_register_id = self.env['lat.siswa.receipt'].search(reg, limit=1)

        if not lat_register_id:

            receipt = self.env['lat.siswa.receipt'].create(
                {
                    'name': 'New',
                    'lat_register_id': self.id,
                    'lat_siswa': self.lat_siswa,
                    'lat_paiddate': fields.Date.today(),
                }
            )

            return {
                'name': _('Document Receipt'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'lat.siswa.receipt',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': receipt.id,
            }
        else:
            return {
                'name': _('Document Receipt'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'lat.siswa.receipt',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': lat_register_id.id,
            }

    @api.multi
    def lat_action_generate_student(self):
        reg = [('lat_register_id', '=', self.id)]
        lat_register_id = self.env['lat.siswa.student'].search(reg, limit=1)

        if not lat_register_id:

            receipt = self.env['lat.siswa.student'].create(
                {
                    'name': 'New',
                    'lat_register_id': self.id,
                    'lat_siswa': self.lat_siswa,
                    'lat_paiddate': fields.Date.today(),
                    'lat_birthdate': self.lat_birthdate,
                    'lat_sex': self.lat_sex,
                }
            )

            return {
                'name': _('Document Student'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'lat.siswa.student',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': receipt.id,
            }
        else:
            return {
                'name': _('Document Receipt'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'lat.siswa.student',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': lat_register_id.id,
            }
