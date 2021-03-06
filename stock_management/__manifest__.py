# -*- encoding: utf-8 -*-

{
    'name': 'Gestion de stock',
    'category': 'Extras tool',
    'author': 'Pricemou Claude, Willof-God Bassanti',
    'version': '2.0',
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
        'views/assets.xml',
        'views/report_invoice.xml',
        'views/inherit.xml',
        'views/views.xml',
        'views/program.xml',
        'views/actions.xml',
        'menu/menu.xml',
        'reports/report.xml',
        'reports/technical_sheet.xml',
        'reports/mail_template.xml',
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
        "static/src/xml/account_payment.xml",
    ],
    'application': True,
    'installable': True,
}
