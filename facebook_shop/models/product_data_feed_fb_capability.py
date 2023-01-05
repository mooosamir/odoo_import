# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import fields, models


class ProductDataFeedBrand(models.Model):
    _name = "product.data.feed.fb_capability"
    _description = 'Facebook Capabilities of Product Feeds'

    name = fields.Char(required=True)
    value = fields.Char(required=True)

    _sql_constraints = [('product_data_feed_fb_capability_uniq',
                         'UNIQUE (value)',
                         'Facebook Capability Value must be unique.')]
