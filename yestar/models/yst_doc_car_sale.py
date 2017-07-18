# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class fal_document_car_sale(models.Model):
    _name = 'document.car.sale'
    _inherit = ['mail.thread']
    _description = "Document Car Sale"

    name = fields.Char(
        string="Number",
    )
    fal_sale_id = fields.Char()
    fal_product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain=[('sale_ok', '=', True)],
        change_default=True,
        ondelete='restrict',
        index=True
    )
    fal_origin = fields.Char(string="Origin Document")
    fal_sequence_item = fields.Char(string="Lot Sequence Product")
    fal_no_stnk = fields.Char(
        string="No STNK Document",
        track_visibility='always',
    )
    fal_no_bpkb = fields.Char(
        string="No BPKB Document",
        track_visibility='always',
    )
    fal_fleet = fields.Many2one(
        'fleet.vehicle',
        ondelete='set null',
        string="Vehicle",
        index=True
    )

    @api.model
    def create(self, vals):

        if vals.get('name', 'New') == 'New':
            seq = 'fal.document.car.sale.number'
            reg = self.env['ir.sequence'].next_by_code(seq)
            vals['name'] = reg or 'New'

        return super(fal_document_car_sale, self).create(vals)

    @api.multi
    def write(self, vals):
        stnk = [('fal_no_stnk', '=', vals.get('fal_no_stnk'))]
        fal_no_stnk_exist = self.env['document.car.sale'].search(stnk, limit=1)
        bpkb = [('fal_no_bpkb', '=', vals.get('fal_no_bpkb'))]
        fal_no_bpkb_exist = self.env['document.car.sale'].search(bpkb, limit=1)
        if fal_no_stnk_exist.fal_no_stnk == vals.get('fal_no_stnk'):
            raise ValidationError(_('STNK Document was exist.'))

        if fal_no_bpkb_exist.fal_no_bpkb == vals.get('fal_no_bpkb'):
            raise ValidationError(_('BPKB Document was exist.'))

        result = super(fal_document_car_sale, self).write(vals)
        return result


class fal_inherit_sales_order(models.Model):
    _inherit = 'sale.order'

    fal_payment = fields.Selection([
        ('cash', "Cash"),
        ('credit', "Credit"),
    ], string="Payment Method")

    @api.multi
    def fal_action_view_document(self):
        return {
            'name': _('Document Car Sale'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'document.car.sale',
            'type': 'ir.actions.act_window',
            'domain': [('fal_sale_id', '=', self.id)],
            'target': 'current',
        }


class fal_inherit_stock_pack_operation_lot(models.Model):
    _inherit = 'stock.pack.operation.lot'

    fal_fleet = fields.Many2one(
        'fleet.vehicle',
        ondelete='set null',
        string="Vehicle",
        index=True,
    )


class fal_inherit_stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_new_transfer(self):
        result = super(fal_inherit_stock_picking, self).do_new_transfer()
        for pick in self:
            # _logger.info(pick.picking_type_id.id)
            # Purchase
            if pick.picking_type_id.id == 1:
                for operation in pick.pack_operation_ids:
                    for lot in operation.pack_lot_ids:
                        search = [('license_plate', '=', lot.lot_name)]
                        fv = 'fleet.vehicle'
                        if self.env['fleet.vehicle'].search(search, limit=1):
                            fleet = self.env[fv].search(search, limit=1)
                            operation.pack_lot_ids.update(
                                {
                                    'fal_fleet': fleet.id,
                                }
                            )
                        else:
                            self.env['fleet.vehicle'].create(
                                {
                                    'license_plate': lot.lot_name,
                                    'model_id': '56',
                                }
                            )
                            fleet = self.env[fv].search(search, limit=1)
                            lot.update(
                                {
                                    'fal_fleet': fleet.id,
                                }
                            )
            # SO
            elif pick.picking_type_id.id == 4:
                for operation in pick.pack_operation_ids:
                    for lot in operation.pack_lot_ids:
                        lotval = lot.lot_id.id
                        se = [('lot_id', '=', lotval), ('qty_todo', '=', 0)]
                        spol = 'stock.pack.operation.lot'
                        fleet = self.env[spol].search(se, limit=1)
                        lot.update(
                            {
                                'fal_fleet': fleet.fal_fleet,
                            }
                        )
                        s = 'fal.document.car.sale.number'
                        ir = 'ir.sequence'
                        self.env['document.car.sale'].create(
                            {
                                'name': self.env[ir].next_by_code(s),
                                'fal_origin': pick.sale_id.name,
                                'fal_sale_id': pick.sale_id.id,
                                'fal_product_id': pick.product_id.id,
                                'fal_sequence_item': fleet.lot_name,
                                'fal_kind_document': '',
                                'fal_no_doc': '',
                                'fal_fleet': fleet.fal_fleet.id,
                            }
                        )
        return result
