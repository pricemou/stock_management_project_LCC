# -*- encoding: utf-8 -*-

{
    'name': 'Gestion de stock',
    'category': 'Extras tool',
    'author': 'Pricemou Claude, Willof-God Bassanti',
    'version': '1.0',
    'depends': [
        'base',
        'account',
        'stock',
        'contacts',
        'mail',
        'accounting_pdf_reports',
        'om_account_accountant',
        'om_account_asset',
        'om_account_budget'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'views/templates.xml',
        'views/inherit.xml',
        'menu/menu.xml',
        'views/views.xml',
        'reports/report.xml',
        'reports/technical_sheet.xml',
        'reports/trial_balance_inherit.xml',
        'reports/aged_partner_inherit.xml',
        'reports/financail_inherit.xml',
        'reports/general_ledger_inherit.xml',
        'reports/journal_audit_inherit.xml',
        'reports/parnet_ledger_inherit.xml',
        'reports/raport_invoice_inherit.xml',
        'reports/tax_inherit.xml',
    ],
    'qweb': [
        'static/src/xml/templates.xml',
    ],
    'application': True,
    'installable': True,
}
