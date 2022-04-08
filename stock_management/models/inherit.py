from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class SMAcountingReport(models.TransientModel):
    _inherit = "account.common.report"

    def preview_report(self):
        res = super(SMAcountingReport, self).check_report()
        return self.with_context(discard_logo_check=True)._preview_report(res['data'])


class SMAccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    def _preview_report(self, data):
        data['form'].update(self.read(['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp',
                            'account_report_id', 'enable_filter', 'label_filter', 'target_move'])[0])
        return self.env.ref('stock_management.action_report_financial_preview').report_action(self, data=data, config=False)


class SMAcountReportGeneralLedger(models.TransientModel):
    _inherit = "account.report.general.ledger"

    def _preview_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['initial_balance', 'sortby'])[0])
        if data['form'].get('initial_balance') and not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('stock_management.action_report_general_ledger_preview').with_context(landscape=True).report_action(records, data=data)


class SMAcountPrintJournal(models.TransientModel):
    _inherit = "account.print.journal"

    def _preview_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'sort_selection': self.sort_selection})
        return self.env.ref('stock_management.action_report_journal_preview').with_context(landscape=True).report_action(self, data=data)


class SMAcountPartnerLedger(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    def _preview_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'reconciled': self.reconciled,
                            'amount_currency': self.amount_currency})
        return self.env.ref('stock_management.action_report_partnerledger_preview').report_action(self, data=data)


class SMAcountTaxReport(models.TransientModel):
    _inherit = 'account.tax.report'

    def _preview_report(self, data):
        return self.env.ref('stock_management.action_report_account_tax_preview').report_action(self, data=data)


class SMAcountBalanceReport(models.TransientModel):
    _inherit = 'account.balance.report'

    def _preview_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('stock_management.action_report_trial_balance_preview').report_action(records, data=data)


class SMAcountAgedTrialBalance(models.TransientModel):
    _inherit = 'account.aged.trial.balance'

    def _preview_report(self, data):
        res = {}
        data = self.pre_print_report(data)
        data['form'].update(self.read(['period_length'])[0])
        period_length = data['form']['period_length']
        if period_length <= 0:
            raise UserError(_('You must set a period length greater than 0.'))
        if not data['form']['date_from']:
            raise UserError(_('You must set a start date.'))

        start = data['form']['date_from']

        for i in range(5)[::-1]:
            stop = start - relativedelta(days=period_length - 1)
            res[str(i)] = {
                'name': (i != 0 and (str((5-(i+1)) * period_length) + '-' + str((5-i) * period_length)) or ('+'+str(4 * period_length))),
                'stop': start.strftime('%Y-%m-%d'),
                'start': (i != 0 and stop.strftime('%Y-%m-%d') or False),
            }
            start = stop - relativedelta(days=1)
        data['form'].update(res)
        return self.env.ref('stock_management.action_report_aged_partner_balance_preview').with_context(landscape=True).report_action(self, data=data)


class SMAccountPayment(models.Model):
    _inherit = 'account.payment'

    check_num = fields.Char(string='Numéro du chèque')


class SMAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_payments_vals(self):
        _logger.info('*** _get_payments_vals ***')
        res = super(SMAccountInvoice, self)._get_payments_vals()
        _logger.info('res')

        for payment in res:
            _logger.info('*** payment ***')
            payment_id = self.env['account.payment'].browse(
                payment['account_payment_id'])
            _logger.info(payment_id)
            payment['payment_method'] = payment_id.payment_method_id.name
            payment['check_num'] = payment_id.check_num
            _logger.info(payment['payment_method'])

        return res
