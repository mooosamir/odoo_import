# Copyright © 2022 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

# flake8: noqa: E501

{
    'name': 'Odoo Google Merchant Center Product Data Feeds',
    'version': '16.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'OPL-1',
    'summary': 'Product Data Feed for Google Merchant Center | Free listings | Shopping ad',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/k78',
    'depends': [
        'product_google_category',
        'product_data_feed_brand',
        'product_data_feed_xml',
        'product_data_feed_number',
    ],
    'data': [
        'data/product_data_feed_recipient_data.xml',
        'data/product_data_feed_data.xml',
        'data/product_data_feed_column_data.xml',
        'data/product_data_feed_column_value_data.xml',
        'views/product_data_feed_views.xml',
        'views/product_template_views.xml',
    ],
    'external_dependencies': {
    },
    'price': -5.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
