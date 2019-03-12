# -*- coding: utf-8 -*-
{
    'name': "Contact Plugin",

    'summary': """Add fields to contact""",

    'description': """This module adds some fields to the Contact module""",

    'author': "AtomX System",

    'website': "http://atomxsystem.eu",

    'category': 'Tools',

    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'views/form_view.xml',
        'views/tree_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}