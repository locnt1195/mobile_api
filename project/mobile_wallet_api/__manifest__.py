# -*- coding: utf-8 -*-
{
    'name': 'Mobile Wallet API',
    'version': '12.0.0.1',
    'category': '',
    'description': """.
    """,
    'author': '',
    'website': 'http://seaedtech.com',
    'depends': [
        'contacts',
        'website',
        'restful'
    ],
    'sequence': 0,
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        # 'security/',
        'security/ir.model.access.csv',

        # ============================================================
        # DATA
        # ============================================================
        # 'data/',

        # ============================================================
        # VIEWS
        # ============================================================
        # 'view/',
        'views/res_partner_view.xml'

        # ============================================================
        # MENU
        # ============================================================
        # 'menu/',

        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
    ],
    'test': [],
    'demo': [],
    'installable': True,
    'active': False,
    'application': True,
}
