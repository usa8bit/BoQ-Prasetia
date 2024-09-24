{
    "name": "Bill of Quantity Prasetia",
    "version": "16.0.1.0.0",
    "website": "https://github.com/usa8bit",
    "author": "Usamah",
    "license": "LGPL-3",
    "category": "Addons",
    "summary": """
        Bill of Quantity Prasetia Dwidharma 
    """,
    "installable": True,
    "depends": ['base', 'mail', 'product', 'sale', 'web'],
    "data": [
        'security/ir_module_category_data.xml',
        'security/res_group_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        'data/ir_sequence_data.xml',
        'menu.xml',
        'views/bill_of_quantity.xml',
        'views/product_template.xml',
        'views/project.xml',
        'views/project_template.xml',
        'report/report_paperformat.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
    ],
    "assets": {
        'web.assets_backend': [
            'bill_of_quantity_prasetia/static/src/css/custom.css',
            'bill_of_quantity_prasetia/static/src/js/custom.js',
        ],
    }
}
