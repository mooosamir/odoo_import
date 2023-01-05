# Copyright © 2020 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

{
    'name': 'Product Data Feed',
    'version': '16.0.1.0.0',
    'category': 'Hidden',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'OPL-1',
    'summary': 'Product Data Feed',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/5yZ',
    'depends': [
        'website_sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_data_feed_views.xml',
        'views/product_data_feed_column_views.xml',
        'views/product_data_feed_column_value_views.xml',
        'views/product_data_feed_recipient_views.xml',
        'views/product_template_views.xml',
    ],
    'external_dependencies': {
    },
    'price': 50.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
