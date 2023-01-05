# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html).

from lxml import etree as ET  # nosec

from odoo import fields, models


class ProductDataFeedColumn(models.Model):
    _inherit = "product.data.feed.column"

    is_cdata = fields.Boolean('CDATA', help='Put a value in the CDATA format.')
    file_type = fields.Selection(
        related='feed_id.file_type',
        help='Technical field for view domains.'
    )

    def _get_value(self, product):
        value = super(ProductDataFeedColumn, self)._get_value(product)
        if self.is_cdata and value:
            value = ET.CDATA(value)
        return value
