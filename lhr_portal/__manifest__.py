# -*- coding: utf-8 -*-
{
    'name': "LHR Portal",

    'summary': """
        This module is a plugin for website module""",

    'description': """
        This module provides a contact form to the website module.
    """,

    'author': "AtomX System",
    'website': "http://www.atomxsystem.eu",
    'category': 'Tools',
    'version': '1.0',

    'depends': ['base', 'website', 'website_form', 'contact_plugin', 'operation'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        #'views/accueil_template.xml',
        'views/create_operation_template.xml',
        'views/footer.xml',
        'views/header.xml',
    ],
    'images': [
        'static/src/img/man_1.png',
        'static/src/img/man_2.png', 
        'static/src/img/man_3.png',
        'static/src/img/man_4.png',
        'static/src/img/woman_1.png',
        'static/src/img/woman_2.png',
        'static/src/img/woman_3.png',
        'static/src/img/woman_4.png',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}