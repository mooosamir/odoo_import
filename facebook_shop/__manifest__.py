# Copyright © 2020 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

# flake8: noqa: E501

{
    'name': 'Facebook Catalog Product Data Feed',
    'version': '16.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'OPL-1',
    'summary': 'Product catalogue to advertise or sell items on Facebook and Instagram. Data Feed | Data Import | Data Source | FB Product Catalog',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/XW8',
    'depends': [
        'product_data_feed',
        'product_google_category',
        'product_facebook_category',
        'product_data_feed_brand',
        'product_data_feed_extra',
        'product_data_feed_number',
        'product_data_feed_feature',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data_feed_recipient_data.xml',
        'data/product_data_feed_data.xml',
        'data/product_data_feed_column_data.xml',
        'data/product_data_feed_column_value_data.xml',
        'data/product_data_feed_fb_capability_data.xml',
        'data/product_data_feed_feature_data.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
        'demo/product_data_feed_demo.xml',
    ],
    'external_dependencies': {
    },
    'price': 33.75,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
