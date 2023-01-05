# Copyright © 2020 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import models


class ProductDataFeed(models.Model):
    _inherit = "product.data.feed"

    def _get_availability_value(self, qty, column):
        res = super(ProductDataFeed, self)._get_availability_value(
            qty=qty, column=column)
        if self.recipient_id == \
                self.env.ref('facebook_shop.recipient_facebook'):
            if qty <= 0:
                if self.out_of_stock_mode == 'order':
                    res = 'available for order'
                else:
                    res = 'out of stock'
            else:
                res = 'in stock'
        return res
