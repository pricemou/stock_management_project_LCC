from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


# class SMAccountingReport(models.TransientModel):
#     _inherit = "accounting.report"

#     @api.multi
#     def check_report(self):
#         self.ensure_one()
#         data = {}
#         data['ids'] = self.env.context.get('active_ids', [])
#         data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
#         data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
#         used_context = self._build_contexts(data)
#         data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
#         return self.with_context(discard_logo_check=True)._preview_report(data)


# class SMAccountPrintJournal(models.TransientModel):
#     _name = "account.print.journal"

#     @api.multi
#     def print_technical_sheet(self):
#         return self.env.ref('stock_management.print_report').report_action(self)
