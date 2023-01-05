# Copyright © 2022 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

# flake8: noqa: E501

{
    'name': 'Product Data Feed XML',
    'version': '16.0.1.0.0',
    'category': 'Hidden',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'OPL-1',
    'summary': 'XML format support for product data feeds',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'depends': [
        'product_data_feed',
    ],
    'data': [
        'views/product_data_feed_column_views.xml',
    ],
    'external_dependencies': {
    },
    'price': 49.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
