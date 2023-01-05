# Copyright © 2022 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Product Features',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'LGPL-3',
    'summary': 'Product Features for Data Feeds',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/Ixa',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_data_feed_feature_views.xml',
        'views/product_data_feed_feature_value_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
