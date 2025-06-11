# -*- coding: utf-8 -*-
{
    'name': "Letter Writer",

    'summary': "Creates custom letter templates that is able to be exported as Word or PDF",

    'description': """
        Design mode allows you to customize the letters using a word editor. (with font styling
        like bold, italic, underline, etc.) There are placeholders for partner & employee. 
        This allows automation, as well as saving multiple templates and using them at will.
    """,

    'author': "Mohamed Emad",
    # 'website': "https://www.github.com/mohamedemad2251/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    'installable' : True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'actions/actions.xml',
        'views/menu_items.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

