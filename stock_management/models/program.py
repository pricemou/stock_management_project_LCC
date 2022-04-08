from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ConstructionProgram(models.Model):
    _name = "construction.program"
    _rec_name = "name"

    name = fields.Char(string='Libellé', required=True)
    city = fields.Char(string='Ville')
    commune = fields.Char(string='Commune')
    district = fields.Char(string='Quartier')
    description = fields.Text(string='Description')
    house_ids = fields.One2many(
        comodel_name='construction.house', inverse_name='program_id',
        string='Les maisons du programme')
    # client_ids = fields.Many2many(
    #     comodel_name='construction.client', string='Clients liés')
    warehouse_id = fields.Many2one('stock.warehouse', string="Entrepôt")
    out_type_id = fields.Many2one(
        comodel_name='stock.picking.type', string='Opération de sortie', related="warehouse_id.out_type_id")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Ce nom de programme est déjà utilisé !"),
    ]

    @api.model
    def create(self, vals):
        result = ''
        wrd_list = vals['name'].split(' ')
        if len(wrd_list) >= 2:
            for word in wrd_list:
                result += str(word[0])
        else:
            result = str(vals['name'][:3])

        new_warehouse = self.env['stock.warehouse'].sudo().create(
            {
                'name': vals['name'],
                'code': result.upper()
            })
        vals['warehouse_id'] = new_warehouse.id
        return super(ConstructionProgram, self).create(vals)

    @api.multi
    def _track_template(self, tracking):
        res = super(ConstructionProgram, self)._track_template(tracking)
        _logger.info('***** res *****')
        _logger.info(res)
        test_task = self[0]
        _logger.info('***** test_task *****')
        _logger.info(test_task)
        changes, tracking_value_ids = tracking[test_task.id]
        _logger.info('***** changes *****')
        _logger.info(changes)
        _logger.info('***** tracking_value_ids *****')
        _logger.info(tracking_value_ids)
        # if 'city' in changes and test_task.stage_id.mail_template_id:
        #     res['stage_id'] = (test_task.stage_id.mail_template_id, {
        #         'auto_delete_message': True,
        #         'subtype_id': self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'),
        #         'notif_layout': 'mail.mail_notification_light'
        #     })
        return res

    # @api.constrains('name')
    # def _check_name_unicity(self):
    #     if self.search_count([
    #         ('name', '=', self.name),
    #     ]) > 1:
    #         raise ValidationError(
    #             _(f"Le nom {self.name} ! Veuillez choisir un autre nom."))

    @api.multi
    def open_program_stock_quantities(self):
        return {
            'name': _("Stock actuel de l'entrepôt"),
            'domain': [('location_id', '=', self.warehouse_id.lot_stock_id.id)],
            'context': {
                'group_by': ['product_id']
            },
            'view_type': 'form',
            'res_model': 'stock.quant',
            'view_id': self.env.ref('stock_management.view_program_stock_quant_tree').id,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def open_program_stock_picking(self):
        return {
            'name': _('Sorties de matériaux'),
            'domain': [('location_id', '=', self.warehouse_id.lot_stock_id.id)],
            'context': {
                'default_picking_type_id': self.warehouse_id.out_type_id.id,
                'default_program_id': self.id
            },
            'view_type': 'form',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def open_program_stock_inventory(self):
        return {
            'name': _("Approvisionnement de l'entrepôt"),
            'domain': [('location_id', '=', self.warehouse_id.lot_stock_id.id)],
            'context': {
                'default_location_id': self.warehouse_id.lot_stock_id.id,
            },
            'view_type': 'form',
            'res_model': 'stock.inventory',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
