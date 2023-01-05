# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from odoo import models


class ProductDataFeedColumn(models.Model):
    _inherit = "product.data.feed.column"

    def get_special_value(self, product):
        value = super(ProductDataFeedColumn, self).get_special_value(product)
        if self.recipient_id != self.env.ref('facebook_shop.recipient_facebook'):
            return value

        if self.special_type == 'product_attribute':
            value = ','.join([
                "%s:%s" % (av.attribute_line_id.attribute_id.name, av.name) for av in
                self._get_product_variant(product).product_template_attribute_value_ids])

        return value

    def _get_value(self, product):
        self.ensure_one()
        value = super(ProductDataFeedColumn, self)._get_value(product)
        if self.recipient_id != self.env.ref('facebook_shop.recipient_facebook'):
            return value

        if self.name == 'disabled_capabilities':
            value = "[%s]" % ','.join(['`%s`' % ds for ds in value])

        return value
